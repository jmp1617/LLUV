"""
A very basic cli
Basically just dd with a status bar
"""
import sys
import lluv.lluv as lluv
import os


def start():

    disk_path = input("Device Path >")
    image = input("Image Path >")
    bs = input("Block Size (blank for defualt) >")
    if bs == "":
        bs = "512K"

    if bs in ["512b", "1K", "2K", "4k", "8K", "16K", "32K", "64K", "128K", "256K", "512K", "1M", "2M", "4M", "8M",
              "16M", "32M", "64M"]:
        try:
            lluv.write_to_device("", disk_path, bs, str(round(os.path.getsize(sys.argv[1]) / 1000000)), True, image)
        except Exception:   # broad
            print("Error, check inputs")
    else:
        print("Not a valid bs (ex: 4K, 16M, etc)")
    
if __name__ == '__main__':
    start()
