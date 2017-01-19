"""
LLUV backend

author: Jacob Potter CSH:(jpotter)
"""
import subprocess
import configparser
import shlex
import math
import sys
import threading
from time import sleep
from lluv_classes import *


def get_path() -> str:
    """
    Function to parse the config file for the path to the ISO dir
    :return: String path to iso
    """
    config = configparser.ConfigParser()
    config.read('lluv.conf')
    return config['path_to_images']['path']


def fetch_usb() -> dict:
    """
    Function to gather data on the usb devices connected to the machine
    Also removes devices specified in config
    :return:
    """
    usb_dict = {}  # dict to hold data about usb devices
    ignore = []  # hold list of devices to be ignored
    usb_num = 1

    config = configparser.ConfigParser()  # parse the config for ignored devices
    config.read('lluv.conf')
    for key in config['dev_to_ignore']:
        ignore.append(str(key).upper())

    out = ((str(subprocess.run(["lsscsi"], stdout=subprocess.PIPE)))[57:]).split(' \\n')
    out.remove("')")

    for line in out:
        split = line.split()
        if len(split) == 7:  # If the device name is two words
            name = split[3] + " " + split[4]
            if name not in ignore:
                usb_dict[usb_num] = UsbStorageDevice(name, get_usb_size(split[6]), split[6], usb_num)
                usb_num += 1

        elif len(split) == 6:  # If the device name is one word
            name = split[3]
            if name not in ignore:
                usb_dict[usb_num] = UsbStorageDevice(name, get_usb_size(split[5]), split[5], usb_num)
                usb_num += 1

    return usb_dict


def generate_list(usb_dict: dict) -> list:
    """
    wrapper for list conversion
    :param usb_dict: usb dictionary
    :return: list of usb devices for tui print
    """
    devices = []
    for usb in usb_dict.values():
        devices.append(usb)
    return devices


def get_usb_size(path: str) -> int:
    """
    Function to get the storage size of the usb drive addressed by the path
    :param path: /dev/sda or whatever
    :return: size of the device
    """
    size = str(subprocess.run(["blockdev", "--getsize64", path], stdout=subprocess.PIPE)).split('\'')[7]
    return int(size[:len(size)-2])


def fetch_images(iso_dir: str) -> list:
    """
    Function to gather data about iso files in the specified directory
    Arranges them by Category and returns a list of categories in alphabetical order
    :return: categories
    """
    categories = []
    no_cat = {}
    has_no_cat = False
    image_num = 1

    dirs = str(subprocess.run(["ls", iso_dir], stdout=subprocess.PIPE)).split("'")[5].split("\\n")
    del dirs[len(dirs)-1]

    for file in dirs:
        if file[len(file)-4:] == '.iso':
            has_no_cat = True
            image = str(subprocess.run(["ls", "-l", "--block-siz=MB", iso_dir+"/"+file],
                                       stdout=subprocess.PIPE)).split("stdout=b'")[1].split()
            no_cat[image_num] = Image(image[8][:len(image[8])-4].split("/")[5], image[4], get_rec_size(image[4]), '',
                                      image_num)
            dirs.remove(file)
            image_num += 1

    if has_no_cat:
        categories.append(Category("No-Category", no_cat))

    for category in dirs:
        images_dict = {}

        images = str(subprocess.run(["ls", "-l", "--block-siz=MB", iso_dir+"/"+category], stdout=subprocess.PIPE))\
            .split("stdout=b'total")[1].split("\\n")[1:]
        del images[len(images)-1]

        for image in images:
            image = image.split()
            images_dict[image_num] = Image(image[8], image[4], get_rec_size(image[4]), category, image_num)
            image_num += 1

        categories.append(Category(category, images_dict))

    categories.sort(key=lambda x: x.get_name())
    return categories


def generate_image_master(categories: list) -> dict:
    """
    Takes in the list of categories and images
    and generate a master dictionary containing all of the images
    :param categories:
    :return:
    """
    master_dict = {}
    for category in categories:
        master_dict = {**master_dict, **category.get_images()}

    return master_dict


def get_rec_size(size: str) -> str:
    """
    Function to check to see if the specified usb storage device is large enough for the selected ISO
    :param size: name of selected usb FORMAT: ##...##MB
    :return: rec_size  the recommended size in GB
    """
    config = configparser.ConfigParser()  # parse the config for ignored devices
    config.read('lluv.conf')

    leeway = int(config['configuration']['leeway'])  # Mb  leeway in usb size

    iso_size = int(size[:(len(size)-2)]) + leeway

    if iso_size < 1500:
        rec_size = "2 GB"
    else:
        rec_size = str(math.ceil(iso_size/1000)) + " GB"

    return rec_size


def check_compatibility(selected_usb_size: int, iso_rec_size: str) -> bool:
    """
    Function to test whether or not the usb is large enough for selected ISO
    :param:string: selected_usb_size pointer to selected usb device size
    :param:int: iso_rec_size recommended size selected ISO needs
    :return: true if size is large enough
    """
    if selected_usb_size >= int((iso_rec_size.split())[0]) * 1000000000:
        return True
    else:
        return False


def calculate_block_size(usb_path: str) -> str:
    """
    function to calculate the optimal block size for selected device
    tests block sizes ranging from 512b - 64M
    device must have a mountable partition
    :param usb_path: path of usb with a mountable partition
    :return: optimal block size
    """
    size = ''

    config = configparser.ConfigParser()
    config.read('lluv.conf')

    mount_path = config['configuration']['mount']  # mount point

    check_mount = str(subprocess.run(shlex.split("awk -v needle=\""+usb_path+"1\" '$1==needle {print $2}' "
                                                 "/proc/mounts"), stdout=subprocess.PIPE)).split()[8]  # check kernel
    cur_mount_point = (check_mount.split("'")[1]).strip("\\n")
    if cur_mount_point != '':  # if the drive is already mounted
        init_umount = str(subprocess.run(["sudo", "umount", cur_mount_point], stderr=subprocess.PIPE)).split("'")
        if init_umount[7] != '':  # Could not un mount for some reason
            return size

    errmount = str(subprocess.run(["sudo", "mount", usb_path+"1", mount_path], stderr=subprocess.PIPE)).split("'")

    if errmount[9] == '':  # begin test if there are no errors
        test_file_size = 134217728  # 128 mb
        b_size = 65536
        count = test_file_size//b_size  # number of segment copies

        subprocess.run(["sudo", "dd", "if=/dev/urandom", "of="+mount_path+"/temp", "bs="+str(b_size), "count=" +
                        str(count)],
                       stderr=subprocess.PIPE)  # write a bunch of random bits to the mount path

        block_sizes = {512: "512b", 1024: "1K", 2048: "2K", 4096: "4k", 8192: "8K", 16384: "16K", 32768: "32K",
                       65536: "64K", 131072: "128K", 262144: "256K", 524288: "512K", 1048576: "1M", 2097152: "2M",
                       4194304: "4M", 8388608: "8M", 16777216: "16M", 33554432: "32M", 67108864: "64M"}
        best_speed = -1
        best_size = ""
        for block_size in block_sizes.keys():
            out = str(subprocess.run(["dd", "if="+mount_path+"/temp", "of=/dev/null", "bs="+str(block_size)],
                                     stderr=subprocess.PIPE)).split()  # write from the drive to dev null to test speed
            result = out[len(out)-2]
            if float(result) > best_speed:
                best_speed = float(result)
                best_size = block_size

        subprocess.run(["sudo", "rm", "-rf", mount_path+"/temp"], stderr=None)  # remove the created test file
        subprocess.run(["sudo", "umount", mount_path])  # and unmount
        size = block_sizes[best_size]

    return size


def write_to_device(image_name: str, usb_path: str, block: str, img_size: str, pbar: bool):
    """
    Function to take the gathered information and perform the write
    using dd
    :param image_name: name of image to write
    :param usb_path: path to usb device
    :param block block size
    :param img_size size of selected image
    :param pbar if true progressbar thread will run
    :return: None
    """

    full_iso_path = get_path()+"/"+image_name
    cmds = shlex.split("sudo dd if="+full_iso_path+" of="+usb_path+" bs="+block+" status=progress oflag=sync")

    if pbar:
        size = int(img_size)
        p1 = threading.Thread(name='dd_subprocess', target=dd, args=(cmds, ))
        p2 = threading.Thread(name='dd_progress_bar', target=dd_progress_bar, args=(size, ))

        p1.start()  # threads for dd and the progress bar
        p2.start()

        p1.join()
        p2.join()
    else:
        dd(cmds)

    subprocess.run(["sync"])


def dd(cmds):
    """
    dd command wrapper
    :param cmds: dd commands
    :return:
    """
    config = configparser.ConfigParser()
    config.read('lluv.conf')

    file = config['configuration']['dd_prog_location']  # log location

    log = open(file, 'w')
    d = subprocess.Popen(cmds, stderr=log, bufsize=1, universal_newlines=True)
    d.communicate()
    d.wait()
    log.close()
    subprocess.run(["sudo", "rm", "-rf", file]) # Leave the log


def dd_status(img_size: int) -> float:
    """
    function to read the output file of dd and convert it
    to a percent completion
    :param img_size: size of the image
    :return: percent completion of dd
    """
    config = configparser.ConfigParser()
    config.read('lluv.conf')

    con = config['configuration']['dd_prog_location']  # log location
    next_line = None
    try:
        file = open(con)
    except FileNotFoundError:
        return 0.0
    line_num = 0
    while True:
        if line_num != 0:
            line = next_line
        else:
            line = file.readline().strip("\n")
        next_line = file.readline().strip("\n")
        if "records" in line:  # done or process killed prematurely (pulling out the drive)
            file.close()
            return 100
        if line_num != 0:
            if next_line == '':
                last_line = line.split()
                break
        line_num += 1
    file.close()
    if len(last_line) > 1:
        current_write = last_line[2][1:]
        if last_line[3][:2] == "MB":
            percent_complete = (float(current_write)/img_size)*100
        elif last_line[3][:2] == "GB":
            percent_complete = (float(current_write)*1000 / img_size) * 100
        else:
            percent_complete = 0.0
        file.close()
        if percent_complete <= 100:
            return percent_complete
        else:
            return 100.0
    else:
        file.close()
        return 0.0


def generate_status_bar(percent: float, img_size: int):
    """
    take a percent and create a progress bar
    :param percent: percent complete
    :param img_size: size of the image MB
    :return: progress bar
    """
    bar_length = 50
    number_bars = round((int(str(percent).split(".")[0]))/(100/bar_length))  # calculate number of bars
    progress_bar = "["

    current_write = img_size*(percent/100)

    for i in range(number_bars):
        if i == number_bars-1:
            progress_bar += ">"
        else:
            progress_bar += "="
    for i in range(bar_length-number_bars):
        progress_bar += " "
    return progress_bar + "] " + \
        str(round(percent)) + "% - " + str(round(current_write)) + "/" + str(img_size) + " MB Written"


def dd_progress_bar(img_size: int):
    """
    wrapper function for thread to create the progress bar
    :param img_size: size of selected image in MB
    :return:
    """

    sleep(1)

    percent = dd_status(img_size)
    while percent != 100:
        percent = dd_status(img_size)
        sys.stdout.write("\r"+generate_status_bar(percent, img_size))
        sleep(0.5)
    print("\n")
