# README
# to use:
# import get_pins as gpi
#
# Function get_pins
# gpi.get_pins(chip, og_file)
# "chip" is the part that you need pins for
# "og_file" is the original master file being read
# returns (inputs, outputs) in a tuple
# it will return (None, None) if it cannot find the chip
#
# example:
#    og_file = open("*.hdl", "r")
#    hdl = og_file.read()
#    for chip in parse_hdl(hdl)['parts']:
#        part['inputs'], part['outputs'] = gpi.get_pins(chip, og_file)

from nand2tetris_hdl_parser import parse_hdl
import os

# pins formatted to match parse_hdl output

# if start, end = -1, pin sizes are not specified in hdl file (default to 0)
# else, pin sizes are specified in hdl file (start and end values specify pin size)

def RAM64_pins():
    return ([{'name': 'in', 'start': 16, 'end': 16},
             {'name': 'load', 'start': -1, 'end': -1},
             {'name': 'address', 'start': 6, 'end': 6}],

            [{'name': 'out', 'start': 16, 'end': 16}])


def Not16_pins():
    return ([{'name': 'in', 'start': 16, 'end': 16}],

            [{'name': 'out', 'start': 16, 'end': 16}])


def RAM512_pins():
    return ([{'name': 'in', 'start': 16, 'end': 16},
             {'name': 'load', 'start': -1, 'end': -1},
             {'name': 'address', 'start': 9, 'end': 9}],

            [{'name': 'out', 'start': 16, 'end': 16}])


def Mux16_pins():
    return ([{'name': 'a', 'start': 16, 'end': 16},
             {'name': 'b', 'start': 16, 'end': 16},
             {'name': 'sel', 'start': -1, 'end': -1}],

            [{'name': 'out', 'start': 16, 'end': 16}])


def Xor_pins():
    return ([{'name': 'a', 'start': -1, 'end': -1},
             {'name': 'b', 'start': -1, 'end': -1}],

            [{'name': 'out', 'start': -1, 'end': -1}])


def Mux8Way16_pins():
    return ([{'name': 'a', 'start': 16, 'end': 16},
             {'name': 'b', 'start': 16, 'end': 16},
             {'name': 'c', 'start': 16, 'end': 16},
             {'name': 'd', 'start': 16, 'end': 16},
             {'name': 'e', 'start': 16, 'end': 16},
             {'name': 'f', 'start': 16, 'end': 16},
             {'name': 'g', 'start': 16, 'end': 16},
             {'name': 'h', 'start': 16, 'end': 16},
             {'name': 'sel', 'start': 3, 'end': 3}],

            [{'name': 'out', 'start': 16, 'end': 16}])


def DMux4Way_pins():
    return ([{'name': 'in', 'start': -1, 'end': -1},
             {'name': 'sel', 'start': 2, 'end': 2}],

            [{'name': 'a', 'start': -1, 'end': -1},
             {'name': 'b', 'start': -1, 'end': -1},
             {'name': 'c', 'start': -1, 'end': -1},
             {'name': 'd', 'start': -1, 'end': -1}])


def RAM8_pins():
    return ([{'name': 'in', 'start': 16, 'end': 16},
             {'name': 'load', 'start': -1, 'end': -1},
             {'name': 'address', 'start': 3, 'end': 3}],

            [{'name': 'out', 'start': 16, 'end': 16}])


def Register_pins():
    return ([{'name': 'in', 'start': 16, 'end': 16},
             {'name': 'load', 'start': -1, 'end': -1}],

            [{'name': 'out', 'start': 16, 'end': 16}])


def RAM16K_pins():
    return ([{'name': 'in', 'start': 16, 'end': 16},
             {'name': 'load', 'start': -1, 'end': -1},
             {'name': 'address', 'start': 14, 'end': 14}],

            [{'name': 'out', 'start': 16, 'end': 16}])


def Mux4Way16_pins():
    return ([{'name': 'a', 'start': 16, 'end': 16},
             {'name': 'b', 'start': 16, 'end': 16},
             {'name': 'c', 'start': 16, 'end': 16},
             {'name': 'd', 'start': 16, 'end': 16},
             {'name': 'sel', 'start': 2, 'end': 2}],

            [{'name': 'out', 'start': 16, 'end': 16}])


def PC_pins():
    return ([{'name': 'in', 'start': 16, 'end': 16},
             {'name': 'load', 'start': -1, 'end': -1},
             {'name': 'inc', 'start': -1, 'end': -1},
             {'name': 'reset', 'start': -1, 'end': -1}],

            [{'name': 'out', 'start': 16, 'end': 16}])


def Or8Way_pins():
    return ([{'name': 'in', 'start': 8, 'end': 8}],

            [{'name': 'out', 'start': -1, 'end': -1}])


def RAM4K_pins():
    return ([{'name': 'in', 'start': 16, 'end': 16},
             {'name': 'load', 'start': -1, 'end': -1},
             {'name': 'address', 'start': 12, 'end': 12}],

            [{'name': 'out', 'start': 16, 'end': 16}])


def DRegister_pins():
    return ([{'name': 'in', 'start': 16, 'end': 16},
             {'name': 'load', 'start': -1, 'end': -1}],

            [{'name': 'out', 'start': 16, 'end': 16}])


def DMux8Way_pins():
    return ([{'name': 'in', 'start': -1, 'end': -1},
             {'name': 'sel', 'start': 3, 'end': 3}],

            [{'name': 'a', 'start': -1, 'end': -1},
             {'name': 'b', 'start': -1, 'end': -1},
             {'name': 'c', 'start': -1, 'end': -1},
             {'name': 'd', 'start': -1, 'end': -1},
             {'name': 'e', 'start': -1, 'end': -1},
             {'name': 'f', 'start': -1, 'end': -1},
             {'name': 'g', 'start': -1, 'end': -1},
             {'name': 'h', 'start': -1, 'end': -1}])


def And16_pins():
    return ([{'name': 'a', 'start': 16, 'end': 16},
             {'name': 'b', 'start': 16, 'end': 16}],

            [{'name': 'out', 'start': 16, 'end': 16}])


def Inc16_pins():
    return ([{'name': 'in', 'start': 16, 'end': 16}],

            [{'name': 'out', 'start': 16, 'end': 16}])


def Screen_pins():
    return ([{'name': 'in', 'start': 16, 'end': 16},
             {'name': 'load', 'start': -1, 'end': -1},
             {'name': 'address', 'start': 13, 'end': 13}],

            [{'name': 'out', 'start': 16, 'end': 16}])


def ALU_pins():
    return ([{'name': 'x', 'start': 16, 'end': 16},
             {'name': 'y', 'start': 16, 'end': 16},
             {'name': 'zx', 'start': -1, 'end': -1},
             {'name': 'nx', 'start': -1, 'end': -1},
             {'name': 'zy', 'start': -1, 'end': -1},
             {'name': 'ny', 'start': -1, 'end': -1},
             {'name': 'f', 'start': -1, 'end': -1},
             {'name': 'no', 'start': -1, 'end': -1}],

            [{'name': 'out', 'start': 16, 'end': 16},
             {'name': 'zr', 'start': -1, 'end': -1},
             {'name': 'ng', 'start': -1, 'end': -1}])


def ARegister_pins():
    return ([{'name': 'in', 'start': 16, 'end': 16},
             {'name': 'load', 'start': -1, 'end': -1}],

            [{'name': 'out', 'start': 16, 'end': 16}])


def ROM32K_pins():
    return ([{'name': 'address', 'start': 15, 'end': 15}],

            [{'name': 'out', 'start': 16, 'end': 16}])


def FullAdder_pins():
    return ([{'name': 'a', 'start': -1, 'end': -1},
             {'name': 'b', 'start': -1, 'end': -1},
             {'name': 'c', 'start': -1, 'end': -1}],

            [{'name': 'sum', 'start': -1, 'end': -1},
             {'name': 'carry', 'start': -1, 'end': -1}])


def DMux_pins():
    return ([{'name': 'in', 'start': -1, 'end': -1},
             {'name': 'sel', 'start': -1, 'end': -1}],

            [{'name': 'a', 'start': -1, 'end': -1},
             {'name': 'b', 'start': -1, 'end': -1}])


def Keyboard_pins():
    return ([{'name': 'Keyboard', 'start': -1, 'end': -1}],

            [{'name': 'out', 'start': 16, 'end': 16}])


def Nand_pins():
    return ([{'name': 'a', 'start': -1, 'end': -1},
             {'name': 'b', 'start': -1, 'end': -1}],

            [{'name': 'out', 'start': -1, 'end': -1}])


def DFF_pins():
    return ([{'name': 'in', 'start': -1, 'end': -1}],

            [{'name': 'out', 'start': -1, 'end': -1}])


def Bit_pins():
    return ([{'name': 'in', 'start': -1, 'end': -1},
             {'name': 'load', 'start': -1, 'end': -1}],

            [{'name': 'out', 'start': -1, 'end': -1}])


def CPU_pins():
    return ([{'name': 'inM', 'start': 16, 'end': 16},
             {'name': 'instruction', 'start': 16, 'end': 16},
             {'name': 'reset', 'start': -1, 'end': -1}],

            [{'name': 'outM', 'start': 16, 'end': 16},
             {'name': 'writeM', 'start': -1, 'end': -1},
             {'name': 'addressM', 'start': 15, 'end': 15},
             {'name': 'pc', 'start': 16, 'end': 16}])


def Memory_pins():
    return ([{'name': 'in', 'start': 16, 'end': 16},
             {'name': 'load', 'start': -1, 'end': -1},
             {'name': 'address', 'start': 15, 'end': 15}],

            [{'name': 'out', 'start': 16, 'end': 16}])


def HalfAdder_pins():
    return ([{'name': 'a', 'start': -1, 'end': -1},
             {'name': 'b', 'start': -1, 'end': -1}],

            [{'name': 'sum', 'start': -1, 'end': -1},
             {'name': 'carry', 'start': -1, 'end': -1}])


def And_pins():
    return ([{'name': 'a', 'start': -1, 'end': -1},
             {'name': 'b', 'start': -1, 'end': -1}],

            [{'name': 'out', 'start': -1, 'end': -1}])


def Add16_pins():
    return ([{'name': 'a', 'start': 16, 'end': 16},
             {'name': 'b', 'start': 16, 'end': 16}],

            [{'name': 'out', 'start': 16, 'end': 16}])


def Not_pins():
    return ([{'name': 'in', 'start': -1, 'end': -1}],

            [{'name': 'out', 'start': -1, 'end': -1}])


def Mux_pins():
    return ([{'name': 'a', 'start': -1, 'end': -1},
             {'name': 'b', 'start': -1, 'end': -1},
             {'name': 'sel', 'start': -1, 'end': -1}],

            [{'name': 'out', 'start': -1, 'end': -1}])


def Or16_pins():
    return ([{'name': 'a', 'start': 16, 'end': 16},
             {'name': 'b', 'start': 16, 'end': 16}],

            [{'name': 'out', 'start': 16, 'end': 16}])


def Or_pins():
    return ([{'name': 'a', 'start': -1, 'end': -1},
             {'name': 'b', 'start': -1, 'end': -1}],

            [{'name': 'out', 'start': -1, 'end': -1}])


def get_pins_local_files(chip, og_file):
    real_path = os.path.realpath(og_file.name)
    path = os.path.dirname(real_path) + "/"
    chip_file = path + "{}.hdl".format(chip['name'])
    try:
        hdl = open(chip_file, "r").read()
    except IOError as e:
        pins = (None, None)
        return pins

    json_data = parse_hdl(hdl)
    pins = (json_data['inputs'], json_data['outputs'])
    return pins


def get_pins(chip, og_file):
    switches = {
        "Add16": Add16_pins,
        "ALU": ALU_pins,
        "And16": And16_pins,
        "And": And_pins,
        "ARegister": ARegister_pins,
        "Bit": Bit_pins,
        "CPU": CPU_pins,
        "DFF": DFF_pins,
        "DMux4Way": DMux4Way_pins,
        "DMux8Way": DMux8Way_pins,
        "DMux": DMux_pins,
        "DRegister": DRegister_pins,
        "FullAdder": FullAdder_pins,
        "HalfAdder": HalfAdder_pins,
        "Inc16": Inc16_pins,
        "Keyboard": Keyboard_pins,
        "Memory": Memory_pins,
        "Mux16": Mux16_pins,
        "Mux4Way16": Mux4Way16_pins,
        "Mux8Way16": Mux8Way16_pins,
        "Mux": Mux_pins,
        "Nand": Nand_pins,
        "Not16": Not16_pins,
        "Not": Not_pins,
        "Or16": Or16_pins,
        "Or8Way": Or8Way_pins,
        "Or": Or_pins,
        "PC": PC_pins,
        "RAM16K": RAM16K_pins,
        "RAM4K": RAM4K_pins,
        "RAM512": RAM512_pins,
        "RAM64": RAM64_pins,
        "RAM8": RAM8_pins,
        "Register": Register_pins,
        "ROM32K": ROM32K_pins,
        "Screen": Screen_pins,
        "Xor": Xor_pins,
    }

    # stores if chip is defined locally
    local_file = False

    # stores if chip shares name with inbuilt chip
    built_in = False

    pins = get_pins_local_files(chip, og_file)
    if pins != (None, None):
        local_file = True

    func = switches.get(chip['name'])
    if func is not None:
        built_in = True

    # returns pins
    if local_file and not built_in:
        chip["custom_pins"] = True
        return pins

    elif local_file and built_in:
        if func() == pins:
            chip["custom_pins"] = False
            return func()
        else:
            chip["custom_pins"] = True
            return pins

    elif built_in:
        chip["custom_pins"] = False
        return func()

    else:
        # error
        # cannot find local file
        # returns (None, None)

        chip["custom_pins"] = False
        return pins