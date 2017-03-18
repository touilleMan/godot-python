import cffi

ffibuilder = cffi.FFI()

ffibuilder.embedding_api("""
    int do_stuff(int, int);
""")

ffibuilder.set_source("pythonscriptcffi", "")

ffibuilder.embedding_init_code("""
    print('============> INIT CFFI <===========')
    import imp
    import sys

    sys.modules["godot"] = imp.new_module("godot")
    sys.modules["godot.bindings"] = imp.new_module("godot.bindings")

    from my_plugin import ffi

    @ffi.def_extern()
    def do_stuff(x, y):
        print("adding %d and %d" % (x, y))
        return x + y
""")

ffibuilder.compile(target="pythonscriptcffi.*", verbose=True)
