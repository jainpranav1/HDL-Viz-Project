#!/usr/bin/python
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {
    "packages": ["nand2tetris_hdl_parser"],
    # "include_files": [("/home/sky/git/nand2tetris-hdl-parser/target/release/libnand2tetris_hdl_parser.so", "lib/nand2tetris_hdl_parser.cpython-39-x86_64-linux-gnu.so")],
    "include_files": [("parse/target/release/libnand2tetris_hdl_parser.so", "lib/nand2tetris_hdl_parser.cpython-39-x86_64-linux-gnu.so")],

}

setup(
    name = "HDL_Visualizer",
    version = "0.1",
    options = {"build_exe": build_exe_options},
    executables = [Executable("cli.py")]
)
