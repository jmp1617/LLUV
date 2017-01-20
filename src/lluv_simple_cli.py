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
    else:
        print("USAGE: lluv_simple_cli [image] [device to write to]")
