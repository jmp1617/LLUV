# L.L.U.V.
The LLUV machine (or Linux Live Usb Vending) machine is a service that allows
users to select an image from a repository and write it to a usb storage device.
The backend uses DD so use with care. If the usb device is allocated and writable, 
a block size will automatically be generated for optimal performance.

# Dependencies
lsscsi - for discovering usb storage devices
DD - for writing the image
Awk - for testing mount location

# Run
sudo python3.5 lluv_cli.py (needs root for storage device acess)
