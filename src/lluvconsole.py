"""
lluv's main script. Use this to start either the TUI,
advanced CLI, or simple CLI.

author: Jacob Potter CSH:(jpotter)
"""

import lluv_tui
import lluv_cli
import lluv_simple_cli

def main():
    """
    prompt the user for a lluv interface
    """
    print("\nWELCOME TO THE L.L.U.V. (Linux Live USB Vending) MACHINE CLI")
    print("by Jacob Potter (jpotter)\n")
    print("1: Start TUI")
    print("2: Start Advanced CLI")
    print("3: Start Simple CLI (basically dd with a progressbar)")
    print("0: Quit\n")

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

    if option == 0: # Quit
        print("Quitting")
        exit()
    if option == 1:
        lluv_tui.start()
    if option == 2:
        lluv_cli.start()
    if option == 3:
        lluv_simple_cli.start()

if __name__ == '__main__':
    main()
