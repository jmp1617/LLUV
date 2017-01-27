"""
Classes for defining usb devices, images, and categories

author: Jacob Potter CSH:(jpotter)
"""


class UsbStorageDevice:
    """
    object to hold define a usb device
    """
    def __init__(self, name: str, size: int, path: str, key: int):
        self._name = name
        self._size = size
        self._path = path
        self._key = key

    def __str__(self) -> str:
        return "USB DEVICE[ name:\'"+self._name+"\' size:"+str(self._size)+" path:"+self._path+" ]"

    def __repr__(self) -> str:
        return self.__str__()

    def get_name(self) -> str:
        return self._name

    def get_size(self) -> int:
        return self._size

    def get_path(self) -> str:
        return self._path

    def get_key(self) -> int:
        return self._key


class Image:
    """
    object to define an image
    """
    def __init__(self, name: str, size: str, rsize: str, cat: str):
        self._name = name
        self._size = size
        self._rsize = rsize
        self._cat = cat

    def __str__(self) -> str:
        return "IMAGE[ name:\'"+self._name+"\' size:"+str(self._size) + \
               " recommended size:"+self._rsize+" category: "+self._cat+"]"

    def __repr__(self) -> str:
        return self.__str__()

    def get_name(self) -> str:
        return self._name

    def get_size(self) -> str:
        return self._size

    def get_rsize(self) -> str:
        return self._rsize

    def get_cat(self) -> str:
        return self._cat


class Category:
    """
    object do define a category
    contains name and list of images in category
    """
    def __init__(self, name: str, images: dict):
        self._name = name
        self._images = images

    def __str__(self) -> str:
        return "CATEGORY [ name:"+self._name+" images: "+str(self._images)+" ]"

    def __repr__(self) -> str:
        return self.__str__()

    def get_name(self) -> str:
        return self._name

    def get_images(self) -> dict:
        return self._images
