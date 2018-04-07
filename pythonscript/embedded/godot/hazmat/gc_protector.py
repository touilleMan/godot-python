from pythonscriptcffi import ffi


# Protect python objects passed to C from beeing garbage collected


class ProtectFromGC:

    def __init__(self):
        self._data = {}

    def register(self, value):
        self._data[id(value)] = value

    def unregister(self, value):
        del self._data[id(value)]

    def unregister_by_id(self, id):
        del self._data[id]

    def clear(self):
        self._data.clear()


protect_from_gc = ProtectFromGC()


def connect_handle(obj):
    handle = obj.__dict__.get("_cffi_handle")
    if not handle:
        handle = ffi.new_handle(obj)
        obj._cffi_handle = handle
    return handle
