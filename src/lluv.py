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
    routine to get the storage size of the usb drive addressed by the path
    :param path: /dev/sda or whatever
    :return: size of the device
    """
    size = str(subprocess.run(["blockdev", "--getsize64", path], stdout=subprocess.PIPE)).split('\'')[7]
    return int(size[:len(size)-2])


def fetch_images(iso_dir: str) -> dict:
    """
    routine to gather data about iso files in the specified directory
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
    routine to check to see if the specified usb storage device is large enough for the selected ISO
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


def check_compatibility(selected_usb_size: str, iso_rec_size: int) -> bool:
    """
    function to test whether or not the usb is large enough for selected ISO
    :param:string: selected_usb_size pointer to selected usb device size
    :param:int: iso_rec_size recommended size selected ISO needs
    :return: true if size is large enough
    """
    print(selected_usb_size)
    print(iso_rec_size)
    if selected_usb_size >= iso_rec_size * 1000000000:
        return True
    else:
        return False


def write_to_device(image_name: str, usb_path: str, iso_dir_path):
    full_iso_path = iso_dir_path+"/"+image_name


