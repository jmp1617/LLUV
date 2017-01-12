class UsbStorageDevice:
    def __init__(self, name: str, size: int, path: str):
        self._name = name
        self._size = size
        self._path = path

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


class Image:
    def __init__(self, name: str, size: str, rsize: str):
        self._name = name
        self._size = size
        self._rsize = rsize

    def __str__(self) -> str:
        return "IMAGE[ name:\'"+self._name+"\' size:"+str(self._size)+" recommended size:"+self._rsize+" ]"

    def __repr__(self) -> str:
        return self.__str__()

    def get_name(self) -> str:
        return self._name

    def get_size(self) -> str:
        return self._size

    def get_rsize(self) -> str:
        return self._rsize
