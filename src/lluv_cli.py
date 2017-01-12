"""
simple CLI for LLUV
"""
from lluv import *


def display_curr_choices(selected_usb: str, selected_iso: str, p_usb_devices: dict, images: dict):
    if selected_usb is not None:
        print("\nSelected USB Device:", p_usb_devices[selected_usb].get_name())
    else:
        print("\nSelected USB Device: Not Yet Selected")
    if selected_iso is not None:
        print("Selected Image:", images[selected_iso].get_name(), "\n")
    else:
        print("Selected Image: Not Yet Selected\n")


def main():
    """
    main lluv routine
    :return: None
    """
    selected_usb = None
    selected_iso = None

    print("\nWELCOME TO THE L.L.U.V. (Linux Live USB Vending) MACHINE CLI")
    print("by Jacob Potter (jpotter)\n")
    print("Type start to begin (anything else to exit)\n")
    begin = input("lluv -> ")
    if begin == 'start':

        print("\nStarting... ")
        iso_dir_path = get_path()
        p_usb_devices = fetch_usb()
        images = fetch_images(iso_dir_path)
        print("Done")

        done_step_one = False
        done_step_two = False
        not_finished = True

        while not_finished:
            while not done_step_one:  # Step One
                done_step_one = True
                done_step_two = False

                display_curr_choices(selected_usb, selected_iso, p_usb_devices, images)

                print("STEP ONE - Select a USB storage Device:")

                key_num = 1
                for key, device in p_usb_devices.items():
                    print("\t", key, ") ", device.get_name(), "-", str(int(device.get_size())/1000000) + "MB")
                    key_num = key
                print("\t", key_num+1, ")  Refresh Storage Devices")
                print("\t 0 )  QUIT")

                try:
                    choice = int(input("\nlluv -> "))

                    if choice < 0 or choice > (key_num+1):
                        print("\nNot a valid number, choose a number 0 -", key_num+1, "\n")
                        done_step_one = False
                    elif choice == key_num+1:
                        print("\nRefreshing Devices...")
                        p_usb_devices = fetch_usb()
                        print("Done")
                        done_step_one = False
                    elif choice == 0:
                        exit()
                    else:
                        selected_usb = choice

                except ValueError:
                    print("\nNot a number, choose a number 0 -", key_num+1, "\n")
                    done_step_one = False

            while not done_step_two:
                done_step_two = True

                display_curr_choices(selected_usb, selected_iso, p_usb_devices, images)

                print("STEP TWO - Select an image")

                key_num = 1
                for key, image in images.items():
                    print("\t", key, ") ", image.get_name(), "-", image.get_size())
                    key_num = key
                print("\t", key_num + 1, ")  Refresh Images")
                print("\t", key_num + 2, ")  Go Back")
                print("\t 0 )  QUIT")

                try:
                    choice = int(input("\nlluv -> "))

                    if choice < 0 or choice > (key_num+2):
                        print("\nNot a valid number, choose a number 0 -", key_num+1, "\n")
                        done_step_two = False
                    elif choice == key_num+1:
                        print("\nRefreshing Images...")
                        images = fetch_images(iso_dir_path)
                        print("Done")
                        done_step_two = False
                    elif choice == key_num+2:
                        done_step_one = False
                    elif choice == 0:
                        exit()
                    else:
                        selected_iso = choice


                except ValueError:
                    print("\nNot a number, choose a number 0 -", key_num+1, "\n")
                    done_step_two = False

    elif begin == 'debug':
        print("[DEBUG]")
        iso_dir_path = get_path()
        p_usb_devices = fetch_usb()
        images = fetch_images(iso_dir_path)
        print("Path to images:", iso_dir_path)
        print("Possible USB storage devices:", p_usb_devices)
        print("Possible Images to write:", images)
    else:
        exit()

if __name__ == '__main__':
    main()
