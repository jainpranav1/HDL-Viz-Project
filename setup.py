#!/usr/bin/python
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only

def get_include_files():
    if sys.platform == "linux":
        return ("../parse/target/release/libnand2tetris_hdl_parser.so", "lib/nand2tetris_hdl_parser.cpython-39-x86_64-linux-gnu.so")
    elif sys.platform == "darwin":
        return ("../parse/target/release/libnand2tetris_hdl_parser.dylib", "lib/nand2tetris_hdl_parser.cpython-39-darwin.so")
    elif sys.platform == "win32":
        return ("../parse/target/release/nand2tetris_hdl_parser.dll", "lib/nand2tetris_hdl_parser.cp39-win_amd64.pyd")


build_exe_options = {
    "packages": ["nand2tetris_hdl_parser"],
    "include_files": [get_include_files()],
    "build_exe": "dist"

}

setup(
    name = "HDL_Visualizer",
    version = "0.1",
    options = {"build_exe": build_exe_options},
    executables = [Executable("cli.py")]
)
