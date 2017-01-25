"""
A very basic cli
Basically just dd with a status bar
"""
import sys
import lluv
import os

if __name__ == '__main__':
    if len(sys.argv) == 3:  # Assume user wants default block size
        print("Writing...")
        lluv.write_to_device("", sys.argv[2], "512K", str(round(os.path.getsize(sys.argv[1])/1000000)), True, sys.argv[1])
        print("Done")
    elif:
        if sys.argv[3] in ["512b", "1K", "2K", "4k", "8K", "16K", "32K", "64K", "128K", "256K", "512K", "1M", "2M",
                       "4M", "8M", "16M", "32M", "64M"]
            print("Writing using block size: "+sys.argv[3])
            lluv.write_to_device("", sys.argv[2], sys.argv, str(round(os.path.getsize(sys.argv[1])/1000000)), True, sys.argv[1])
            print("Done")
        else:
            print("Invalid BS")
            print("USAGE: lluv_simple_cli [image] - Path to image [device to write to] - path to device [dd block size] - Optional, leave black to use default 512K")
    else:
        print("USAGE: lluv_simple_cli [image] - Path to image [device to write to] - path to device [dd block size] - Optional, leave black to use default 512K")
