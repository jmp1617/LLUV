"""
simple CLI for LLUV
"""
from lluv import *


def display_curr_choices(selected_usb: str, selected_iso: str, p_usb_devices: dict, images: dict):
    if selected_usb is not "":
        print("\nSelected USB Device:", p_usb_devices[selected_usb].get_name())
    else:
        print("\nSelected USB Device: Not Yet Selected")
    if selected_iso is not "":
        print("Selected Image:", images[selected_iso].get_name(), "\n")
    else:
        print("Selected Image: Not Yet Selected\n")


def main():
    """
    main lluv routine
    :return: None
    """
    selected_usb = ""
    selected_iso = ""
    selected_block_size = "512K"

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
        done_step_three = False
        not_finished = True

        while not_finished:
            while not done_step_one:  # Step One
                done_step_one = True
                done_step_two = False
                done_step_three = False

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

            while not done_step_two and done_step_one:
                done_step_two = True
                done_step_three = False

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
                        done_step_two = False
                        p_usb_devices = fetch_usb()
                        images = fetch_images(iso_dir_path)
                    elif choice == 0:
                        exit()
                    else:
                        selected_iso = choice

                except ValueError:
                    print("\nNot a number, choose a number 0 -", key_num+1, "\n")
                    done_step_two = False
            if selected_iso is not "" and done_step_one and done_step_two:
                print("\nRunning Compatibility Check...")
                if check_compatibility(p_usb_devices[selected_usb].get_size(), images[selected_iso].get_rsize()):
                    print("Selected Device Compatible with Selected Image")
                else:
                    print("WARNING: devices may not be compatible")
                    print("Image recommended size:", images[selected_iso].get_rsize())
                    print("Selected USB size:", p_usb_devices[selected_usb].get_size()/1000000000, " GB")

                print("\nCalculating Block Size for " + p_usb_devices[selected_usb].get_name() + "...")
                try:
                    selected_block_size = calculate_block_size(p_usb_devices[selected_usb].get_path())
                    print("Using: "+selected_block_size+" as it is an optimal bs")
                except ValueError:
                    config = configparser.ConfigParser()
                    config.read('lluv.conf')

                    mount_path = config['configuration']['mount']  # mount point
                    subprocess.run(["sudo", "umount", mount_path])
                    print("Could not calculate optimal block size\n"
                          "This could be because the drive is write protected\n"
                          "(ex. already a live usb).\n"
                          "It could also be because the drive is unallocated.\n"
                          "A default block size of 512K will be used.")

            while not done_step_three and done_step_two:
                done_step_three = True

                display_curr_choices(selected_usb, selected_iso, p_usb_devices, images)

                print("STEP THREE - Write")
                print("\t1 )  Write To Device")
                print("\t2 )  Go Back to Step One")
                print("\t3 )  Go Back to Step Two")
                print("\t0 )  QUIT")

                try:
                    choice = int(input("\nlluv -> "))

                    if choice < 0 or choice > 3:
                        print("\nNot a valid number, choose a number 0 - 3\n")
                        done_step_three = False
                    elif choice == 2:
                        done_step_one = False
                        done_step_three = False
                        p_usb_devices = fetch_usb()
                        images = fetch_images(iso_dir_path)
                        break
                    elif choice == 3:
                        done_step_two = False
                        done_step_three = False
                        p_usb_devices = fetch_usb()
                        images = fetch_images(iso_dir_path)
                        break
                    elif choice == 0:
                        exit()
                    else:
                        print("\nAre you sure you want to write:")
                        print("\t", images[selected_iso].get_name())
                        print("To USB device:")
                        print("\t", p_usb_devices[selected_usb].get_name(), "\n")
                        print("WARNING: This will destroy everything on selected device\n")
                        final = input("(Y/N) -> ")
                        if final == "Y":
                            print("Beginning Write...")
                            write_to_device(images[selected_iso].get_name(),
                                            p_usb_devices[selected_usb].get_path(), iso_dir_path, selected_block_size,
                                            images[selected_iso].get_size()[:len(images[selected_iso].get_size())-2])
                            print("Done")
                            exit()
                        else:
                            done_step_three = False

                except ValueError:
                    print("\nNot a number, choose a number 0 - 3\n")
                    done_step_three = False

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
