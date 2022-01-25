from pathlib import Path
import sys
from subprocess import check_output, run

file_path = Path(__file__).absolute()
file_directory = file_path.parent

llvm_path = Path(
    check_output("where clang").decode().splitlines()[0].strip()).parent.parent
clang_windows = llvm_path / "lib/clang/13.0.0/lib/windows"
clang_rt_asan_thunk_lib = clang_windows / "clang_rt.asan_dll_thunk-x86_64.lib"
assert clang_rt_asan_thunk_lib.exists(), f"{clang_rt_asan_thunk_lib} not found"

cflags_base = " ".join((
    "--target=x86_64-pc-windows-msvc",
    "-fuse-ld=lld",
    "-Wno-cast-align",
    "-fcomment-block-commands=retval",
    "-ferror-limit=200",
    "-fmessage-length=0",
    "-fno-short-enums",
    "-ffunction-sections",
    "-fdata-sections",
    "-std=c99",
))
strict_flags = "-Weverything -Werror -pedantic-errors"

cflags_windows = "-DWIN32 -D_WINDLL"

lib_cflags = " ".join((cflags_base, cflags_windows))

cc = llvm_path / 'bin/clang.exe'

assan_flags = " ".join(("-g", "-gdwarf-4", "-O0", "-fno-omit-frame-pointer",
                        "-fno-optimize-sibling-calls", "-fsanitize=address"))

link_flags = ",".join([
    "-Wl",  # -Wl,<arg>               Pass the comma separated arguments in <arg> to the linker
    # lld-link --help to see possibilities
    "/ignore:longsections",
    "/WX",  # Treat warnings as errors
])
sources = "mylib.c"
includes = f"-I{file_directory}"

cmd = (
    f'"{cc}" {lib_cflags} {strict_flags} {assan_flags} {includes} -c {sources} -o mylib.o'
)
print(f"Running\n  {cmd}")
run(cmd)

cmd = (
    f'"{cc}" {lib_cflags} {assan_flags} "{clang_rt_asan_thunk_lib}" mylib.o '
    '-shared -o mylib.dll')
print(f"Running\n  {cmd}")
run(cmd)

py_file_run_c = "py_file_run.c"

clang_rt_asan_libs = (
    clang_windows / "clang_rt.asan-x86_64.lib",
    clang_windows / "clang_rt.asan_cxx-x86_64.lib",
)
assert all(x.exists() for x in clang_rt_asan_libs), (
    f"{[x for x in clang_rt_asan_libs if not x.exists()]} not found")

clang_rt_asan_libs_str = [f'"{x}"' for x in clang_rt_asan_libs]

default_python_dir = Path(
    f"c:/Python{sys.version_info.major}{sys.version_info.minor}")
if (default_python_dir / "include/Python.h").exists():
    python_dir = default_python_dir
elif (Path(sys.executable).parent / "include/Python.h").exists():
    python_dir = Path(sys.executable).parent
else:
    raise RuntimeError("Python.h not found")
python_include_dir = python_dir / "include"
print(f"Python include directory {python_include_dir}")
python_libs_dir = python_dir / "libs"
print(f"Python libs directory {python_libs_dir}")
py_file_run_link_flags = f"{link_flags},/wholearchive"

cmd = " ".join((
    f'"{cc}" {cflags_base} {cflags_windows} -Wno-everything '
    f'{assan_flags} ',
    f'{py_file_run_link_flags} ',
    f'-I{python_include_dir} ',
    f'-L {python_libs_dir} ',
    # The EXE needs to have clang_rt.asan-x86_64.lib linked
    f' {" ".join([x for x in clang_rt_asan_libs_str])} '
    ' py_file_run.c -o py_file_run.exe',
))
print(f"Running\n  {cmd}")
run(cmd)
