# L.L.U.V.
The **LLUV** machine (or Linux Live Usb Vending) machine is a service that allows <br />
users to select an image from a repository and write it to a usb storage device with <br />
an easy to use user interface. The backend uses DD so use with care. If the usb device <br />
is allocated and writable, a block size will automatically be generated for  <br />
optimal performance.

**LLUV** was originally designed to run in a kiosk fashion, and read from large lists of images, both <br />
local and remote.<br />

Note: The DD process is completely isolated from LLUV, therefor, if a drive is corrupted, <br />
it was probably DD's alter ego; Disk Destroyer.

# Dependencies
lsscsi - for discovering usb storage devices <br />
DD - for writing the image <br />
Awk - for testing mount location <br />

Note: lluv_simple_cli has no dependencies besides dd itself

# Run
Note:_lluv needs root for storage device access_ <br />

To start the lluv console run:<br />
**sudo lluv.lluvconsole**  This will allow an option of interfaces along with automatic<br />
terminal resizing. <br />

**sudo lluv.cli**  <br />

**sudo lluv.tui** Note: Terminal will not be auto resized without using lluvconsole so<br />
the application may crash if the terminal is to small.<br />

**sudo lluv.simple_cli.py** A simple lluv cli. Basically a simplified dd with a progress bar <br />

# The TUI
Written using the [npyscreen](https://github.com/pfalcon-mirrors/npyscreen "npyscreen") library.
The TUI was designed to be used as a kiosk and therefore has no quit option <br />
(use CTRL-C) and must be used in larger terminal formats.

# Configuration file
Edit values such as the path to the images, drives to ignore, leeway in recommended <br />
drive capacity, and more.

# Image Categories
By default, Images in the image directory specified in the config will be put in the No-Category <br />
category. To create Image categories, create a subdirectory and place images of said category inside. <br />
For example, placing fedora images in the directory /"default img path"/Fedora would render them in the <br />
"Fedora" category. Categories will be sorted alphabetically.

# Compatible Operating Systems
Linux

# Current Version: 1.2
1.2 = 1/26<br />
    - lluv console <br />
    - auto term resize <br />

1.1 = 1/19<br />
    - .lluvrc<br />
    - bug fixes<br />
    - code cleanup<br />

1.0 = 1/18<br />
    - prototype<br />
