"""
simple CLI for LLUV

author: Jacob Potter CSH:(jpotter)
"""
import lluv.lluv as lluv


def display_curr_choices(selected_usb: str, selected_iso: str, p_usb_devices: dict, images: dict):
    """
    print selected
    :param selected_usb:
    :param selected_iso:
    :param p_usb_devices:
    :param images:
    :return:
    """
    if selected_usb is not "":
        print("\nSelected USB Device:", p_usb_devices[selected_usb].get_name())
    else:
        print("\nSelected USB Device: Not Yet Selected")
    if selected_iso is not "":
        print("Selected Image:", images[selected_iso].get_name(), "\n")
    else:
        print("Selected Image: Not Yet Selected\n")


def start():
    """
    run the CLI
    """
    """
    main lluv routine
    :return: None
    """
    selected_usb = ""
    selected_iso = ""
    selected_block_size = "512K"
    lluv.check_config()

    print("Type start to begin (anything else to exit)\n")
    begin = input("lluv -> ")
    if begin == 'start':

        print("\nStarting... ")
        iso_dir_path = lluv.get_path()
        p_usb_devices = lluv.fetch_usb()
        categories = lluv.fetch_images(iso_dir_path)
        images = lluv.generate_image_master(categories)
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

                key_num = 0
                for key, device in p_usb_devices.items():
                    print("\t", key, ") ", device.get_name(), "-", str(int(device.get_size()) / 1000000) + "MB")
                    key_num = key
                print("\t", key_num + 1, ")  Refresh Storage Devices")
                print("\t 0 )  QUIT")

                try:
                    choice = int(input("\nlluv -> "))

                    if choice < 0 or choice > (key_num + 1):
                        print("\nNot a valid number, choose a number 0 -", key_num + 1, "\n")
                        done_step_one = False
                    elif choice == key_num + 1:
                        print("\nRefreshing Devices...")
                        p_usb_devices = lluv.fetch_usb()
                        print("Done")
                        done_step_one = False
                    elif choice == 0:
                        exit()
                    else:
                        selected_usb = choice

                except ValueError:
                    print("\nNot a number, choose a number 0 -", key_num + 1, "\n")
                    done_step_one = False

            while not done_step_two and done_step_one:
                done_step_two = True
                done_step_three = False

                display_curr_choices(selected_usb, selected_iso, p_usb_devices, images)

                print("STEP TWO - Select an image")
                print("Categories:")

                key_num = 0
                for cat in categories:
                    print("\t" + cat.get_name())
                    for key, image in cat.get_images().items():
                        print("\t\t", key, ") ", image.get_name())
                        key_num += 1

                print("\tOther Options")
                print("\t\t", key_num + 1, ")  Refresh Images")
                print("\t\t", key_num + 2, ")  Go Back")
                print("\t\t 0 )  QUIT")

                try:
                    choice = int(input("\nlluv -> "))

                    if choice < 0 or choice > (key_num + 1):
                        print("\nNot a valid number, choose a number 0 -", key_num + 1, "\n")
                        done_step_two = False
                    elif choice == key_num:
                        print("\nRefreshing Images...")
                        images = lluv.fetch_images(iso_dir_path)
                        print("Done")
                        done_step_two = False
                    elif choice == key_num + 1:
                        done_step_one = False
                        done_step_two = False
                        p_usb_devices = lluv.fetch_usb()
                        categories = lluv.fetch_images(iso_dir_path)
                        images = lluv.generate_image_master(categories)
                    elif choice == 0:
                        exit()
                    else:
                        selected_iso = choice

                except ValueError:
                    print("\nNot a number, choose a number 0 -", key_num + 1, "\n")
                    done_step_two = False
            if selected_iso is not "" and done_step_one and done_step_two:
                print("\nRunning Compatibility Check...")
                if lluv.check_compatibility(p_usb_devices[selected_usb].get_size(), images[selected_iso].get_rsize()):
                    print("Selected Device Compatible with Selected Image")
                else:
                    print("WARNING: devices may not be compatible")
                    print("Image recommended size:", images[selected_iso].get_rsize())
                    print("Selected USB size:", p_usb_devices[selected_usb].get_size() / 1000000000, " GB")

                print("\nCalculating Block Size for " + p_usb_devices[selected_usb].get_name() + "...")

                selected_block_size = lluv.calculate_block_size(p_usb_devices[selected_usb].get_path())

                if selected_block_size == '':
                    print("Could not calculate optimal block size\n"
                          "This could be because the drive is write protected\n"
                          "(ex. already a live usb).\n"
                          "It could also be because the drive is unallocated, or it\n"
                          "was not able to be un mounted.\n"
                          "A default block size of 512K will be used.")
                    selected_block_size = "512K"
                else:
                    print("Using: " + selected_block_size + " as it is an optimal bs")

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
                        p_usb_devices = lluv.fetch_usb()
                        categories = lluv.fetch_images(iso_dir_path)
                        images = lluv.generate_image_master(categories)
                        break
                    elif choice == 3:
                        done_step_two = False
                        done_step_three = False
                        p_usb_devices = lluv.fetch_usb()
                        categories = lluv.fetch_images(iso_dir_path)
                        images = lluv.generate_image_master(categories)
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
                        if final in ("Y", "y"):
                            print("Beginning Write...\n")
                            lluv.write_to_device(images[selected_iso].get_cat() + "/" + images[selected_iso].get_name(),
                                            # Account for iso category
                                            p_usb_devices[selected_usb].get_path(),
                                            selected_block_size,
                                            images[selected_iso].get_size()[:len(images[selected_iso].get_size()) - 2],
                                            True, "")
                            print("Done")
                            exit()
                        else:
                            done_step_three = False

                except ValueError:
                    print("\nNot a number, choose a number 0 - 3\n")
                    done_step_three = False

    elif begin == 'debug':
        print("[DEBUG]")
        iso_dir_path = lluv.get_path()
        p_usb_devices = lluv.fetch_usb()
        images = lluv.fetch_images(iso_dir_path)
        print("Path to images:", iso_dir_path)
        print("Possible USB storage devices:", p_usb_devices)
        print("Possible Images to write:", images)
    else:
        exit()


def main():
    start()

if __name__ == '__main__':
    main()
