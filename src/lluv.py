"""
LLUV base routines

author: Jacob Potter CSH:(jpotter)
"""
import subprocess
import configparser
import math
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
                usb_dict[usb_num] = UsbStorageDevice(name, get_usb_size(split[6]), split[6])
                usb_num += 1
            else:
                print("IGNORING: ", name)

        elif len(split) == 6:  # If the device name is one word
            name = split[3]
            if name not in ignore:
                usb_dict[usb_num] = UsbStorageDevice(name, get_usb_size(split[5]), split[5])
                usb_num += 1
            else:
                print("IGNORING: ", name)

    return usb_dict


def get_usb_size(path: str) -> int:
    """
    Function to get the storage size of the usb drive addressed by the path
    :param path: /dev/sda or whatever
    :return: size of the device
    """
    size = str(subprocess.run(["blockdev", "--getsize64", path], stdout=subprocess.PIPE)).split('\'')[7]
    return int(size[:len(size)-2])


def fetch_images(iso_dir: str) -> dict:
    """
    Function to gather data about iso files in the specified directory
    :return: images
    """
    images = {}
    image_num = 1

    out = ((str(subprocess.run(["ls", "-l", "--block-siz=MB", iso_dir], stdout=subprocess.PIPE)))[122:]).split("\\n")
    out.remove("')")

    for line in out:
        split = line.split()
        if (split[8])[(len(split[8])-4):] == ".iso":
            images[image_num] = Image(split[8], split[4], get_rec_size(split[4]))
            image_num += 1
        else:
            print(split[8], ", Why is this here?")

    return images


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


def check_for_partitions(usb_path: str) -> bool:
    None


def calculate_block_size(usb_path: str) -> str:
    """
    function to calculate the optimal block size for selected device
    tests block sizes ranging from 512b - 64M
    device must have a mountable partition
    :param usb_path: path of usb with a mountable partition
    :return: optimal block size with speed
    """
    config = configparser.ConfigParser()
    config.read('lluv.conf')

    mount_path = config['configuration']['mount']  # mount point

    err = subprocess.run(["sudo", "mount", usb_path+"1", mount_path], stderr=subprocess.PIPE)

    test_file_size = 134217728  # 128 m
    b_size = 65536
    count = test_file_size//b_size  # number of segment copies

    subprocess.run(["sudo", "dd", "if=/dev/urandom", "of="+mount_path+"/temp", "bs="+str(b_size), "count="+str(count)],
                   stderr=subprocess.PIPE)

    block_sizes = {512: "512b", 1024: "1K", 2048: "2K", 4096: "4k", 8192: "8K", 16384: "16K", 32768: "32K",
                   65536: "64K", 131072: "128K", 262144: "256K", 524288: "512K", 1048576: "1M", 2097152: "2M",
                   4194304: "4M", 8388608: "8M", 16777216: "16M", 33554432: "32M", 67108864: "64M"}
    best_speed = -1
    best_size = ""
    for block_size in block_sizes.keys():
        out = str(subprocess.run(["dd", "if="+mount_path+"/temp", "of=/dev/null", "bs="+str(block_size)],
                                stderr=subprocess.PIPE)).split()
        result = out[len(out)-2]
        if float(result) > best_speed:
            best_speed = float(result)
            best_size = block_size

    subprocess.run(["sudo", "rm", "-rf", mount_path+"/temp"])
    subprocess.run(["sudo", "umount", mount_path])

    return block_sizes[best_size]


def write_to_device(image_name: str, usb_path: str, iso_dir_path: str, block: str):
    """
    Function to take the gathered information and perform the write
    using dd
    :param image_name: name of image to write
    :param usb_path: path to usb device
    :param iso_dir_path: path to iso
    :return: None
    """
    full_iso_path = iso_dir_path+"/"+image_name
    out = str(subprocess.run(["sudo", "dd", "bs="+block, "if=" + full_iso_path, "of=" + usb_path],
                         stderr=subprocess.PIPE)).split("\\n")
    subprocess.run(["sync"])

    print(out[2])


