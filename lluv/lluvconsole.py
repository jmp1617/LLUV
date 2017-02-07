"""
lluv's main script. Use this to start either the TUI,
advanced CLI, or simple CLI.

author: Jacob Potter CSH:(jpotter)
"""

import lluv.lluv_tui as lluv_tui
import lluv.lluv_cli as lluv_cli
import lluv.lluv_simple_cli as lluv_simple_cli
import lluv.lluv as lluv
import sys


def main():
    start()
    

def start():
    """
    prompt the user for a lluv interface
    """

    # config init
    if not lluv.check_config():
        print("Config Gen Error")
        exit()

    print("\nWELCOME TO THE L.L.U.V. (Linux Live USB Vending) MACHINE CLI")
    print("by Jacob Potter (jpotter)\n")
    print("1: Start TUI")
    print("2: Start Advanced CLI")
    print("3: Start Simple CLI (basically dd with a progressbar)")
    print("0: Quit\n")

    option = 0
    cont = False
    while not cont:
        try:
            option = int(input("lluv -> "))
            if option < 0 or option > 3:
                cont = False
                print("Enter a number 0-3")
            else:
                cont = True
        except ValueError:
            cont = False
            print("Enter a number 0-3")

    if option == 0:  # Quit
        print("Quitting")
        exit()
    if option == 1:
        sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=47, cols=143))  # Resize the term
        print("Starting TUI")
        lluv_tui.start()
    if option == 2:
        lluv_cli.start()
    if option == 3:
        lluv_simple_cli.start()

if __name__ == '__main__':
    main()
