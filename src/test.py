from cffi import FFI


def main():
    from pathlib import Path
    file_path = Path(__file__).absolute()
    file_directory = file_path.parent

    dll = file_directory / "mylib.dll"

    ffi = FFI()

    ffi.cdef("double plus_one(double n);")
    lib = ffi.dlopen(str(dll.absolute()))

    print("calling: lib.plus_one(2)")
    print(lib.plus_one(2))
    print("test ok")


if __name__ == '__main__':
    main()
