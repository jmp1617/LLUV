# L.L.U.V.
The **LLUV** machine (or Linux Live Usb Vending) machine is a service that allows <br />
users to select an image from a repository and write it to a usb storage device with <br />
an easy to use user interface. The backend uses DD so use with care. If the usb device <br />
is allocated and writable, a block size will automatically be generated for  <br />
optimal performance.

**LLUV** is designed to run in a kiosk fashion, and read from large lists of images, both <br />
local and remote.

# Dependencies
lsscsi - for discovering usb storage devices <br />
DD - for writing the image <br />
Awk - for testing mount location <br />

# Run
**sudo python3.5 lluv_cli.py** (_needs root for storage device access_)

# Configuration file
Edit values such as the path to the images, drives to ignore, leeway in recommended <br />
drive capacity, and more.

# Image Categories
By default, Images in the image directory specified in the config will be put in the No-Category <br />
category. To create Image categories, create a subdirectory and place images of said category inside. <br />
For example, placing fedora images in the directory /"default img path"/Fedora would render them in the <br />
"Fedora" category. Categories will be sorted alphabetically.