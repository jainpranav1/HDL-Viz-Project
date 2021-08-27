# README
# to use:
# import chip_designer as cd
#
# Function chip_designer
# cd.chip_designer(gmatrix, phdl)
# "gmatrix" is gate matrix
# "phdl" is parsed hdl dictionary
# returns nothing
# the chip_designer function adds gate objects to phdl dictionary
#
# example:
#    cd.chip_designer(gmatrix, phdl)

import schemdraw.elements as elm
from schemdraw.logic import *


def ov_pin_spacing(pins):
    track_spacing = 0.4
    spacing = 1.8 - track_spacing
    for i in pins:
        if i != "---":
            return spacing
    return 0


def shorten_pins(pins):
    short_pins = []

    # maximum number of allowed characters
    # .. [] each considered 1 character
    # [:] considered 2 characters
    # numbers and letters considered 1 character

    max_char = 8

    for p in pins:
        brack_ind = p.find("[")

        if brack_ind == -1:
            if len(p) > max_char:
                short_pins.append(p[0:(max_char - 1)] + "..")
            else:
                short_pins.append(p)
        else:
            name_part = p[0: brack_ind]
            brack_part = p[brack_ind:]

            max_letters = max_char - (len(brack_part) - 1)

            if len(name_part) > max_letters:
                short_pins.append(name_part[0:(max_letters - 1)] + ".." + brack_part)
            else:
                short_pins.append(p)

    return short_pins


def generic_gate_maker(name, input_pins, output_pins, ov_input, ov_output, in_pin_sizes, out_pin_sizes):
    pins = []
    short_input_pins = shorten_pins(input_pins)
    short_output_pins = shorten_pins(output_pins)
    short_ov_input = shorten_pins(ov_input)
    short_ov_output = shorten_pins(ov_output)
    num_inputs = len(input_pins)
    num_outputs = len(output_pins)
    label_width = 1.8

    for i in range(0, num_inputs):
        if in_pin_sizes[i] == 1:
            pins.append(elm.IcPin(name=short_input_pins[i], side="left"))
        else:
            pins.append(elm.IcPin(name=short_input_pins[i], pin=str(in_pin_sizes[i]), side="left"))
    for j in range(0, num_outputs):
        if out_pin_sizes[j] == 1:
            pins.append(elm.IcPin(name=short_output_pins[j], side="right"))
        else:
            pins.append(elm.IcPin(name=short_output_pins[j], pin=str(out_pin_sizes[j]), side="right"))
    pins.reverse()
    max_pins = max([num_inputs, num_outputs])

    pin_hei = 0.6
    gate = elm.Ic(pins=pins, size=[2 * label_width, pin_hei * (max_pins + 1)], edgepadH=pin_hei / 2, plblsize=11,
                  plblofst=0.1).label(name, "top", ofst=[0, -0.35], fontsize=11)
    # pins are 0.5 (width)

    left_spacing = ov_pin_spacing(ov_input)
    right_spacing = ov_pin_spacing(ov_output)

    size_bbox = [2 * label_width + 1 + left_spacing + right_spacing, pin_hei * (max_pins + 1)]

    # coordinates of gate relative to bbox
    rel_coor = [0.5 + left_spacing, 0]

    # adds overall inputs and outputs
    for i in range(0, num_inputs):
        if short_ov_input[i] != "---":
            gate.label(short_ov_input[i], loc="inL" + str(num_inputs - i), fontsize=11)
    for i in range(0, num_outputs):
        if short_ov_output[i] != "---":
            gate.label(short_ov_output[i], loc="inR" + str(num_outputs - i), fontsize=11)

    return gate, size_bbox, rel_coor


def mux_dmux(dmux, input_pins, output_pins, ov_input, ov_output):
    pins = []
    short_ov_input = shorten_pins(ov_input)
    short_ov_output = shorten_pins(ov_output)
    num_inputs = len(input_pins)
    num_outputs = len(output_pins)

    # pins are 0.5
    # width of gate box is 1.25
    # height of gate box is 1.25; triangles height is 0.47; from origin to top is 2

    right_spacing = ov_pin_spacing(ov_output)

    # adds spacing in case their are overall inputs / outputs
    left_spacing = 0
    for i in range(0, num_inputs):
        if (ov_input[i] != "---") and (input_pins[i] != "sel"):
            left_spacing += 1.25
            break

    top_spacing = 0
    for i in range(0, num_inputs):
        if (ov_input[i] != "---") and (input_pins[i] == "sel"):
            top_spacing += 0.45
            break

    size_bbox = [2.25 + right_spacing + left_spacing, 2.47 + top_spacing]

    # coordinates of gate relative to bbox
    rel_coor = [0.5 + left_spacing, + 0.47]

    for i in input_pins:
        if "sel" in i:
            pins.append(elm.IcPin(name=i, side="T"))
        else:
            pins.append(elm.IcPin(name=i, side="L"))

    for j in output_pins:
        pins.append(elm.IcPin(name=j, side="R"))

    pins.reverse()
    gate = elm.Multiplexer(pins=pins, size=[1.25, 1.25], edgepadH=-0.15, slant=20, demux=dmux, plblsize=11)

    # adds overall inputs and outputs
    count = 0

    for i in reversed(range(0, num_inputs)):
        if "sel" in input_pins[i]:
            if short_ov_input[i] != "---":
                gate.label(short_ov_input[i], loc="inT1", fontsize=11)
        else:
            if short_ov_input[i] != "---":
                gate.label(short_ov_input[i], loc="inL" + str(count + 1), fontsize=11)
            count += 1
    for i in range(0, num_outputs):
        if short_ov_output[i] != "---":
            gate.label(short_ov_output[i], loc="inR" + str(num_outputs - i), fontsize=11)

    return gate, size_bbox, rel_coor


def elem_gate_maker(name, input_pins, ov_input, ov_output):
    short_ov_input = shorten_pins(ov_input)
    short_ov_output = shorten_pins(ov_output)

    num_in = len(input_pins)

    # height of gates is 1
    # width of gates varies

    left_spacing = ov_pin_spacing(ov_input)
    right_spacing = ov_pin_spacing(ov_output)

    bbox_height = 1

    # coordinates of gate relative to bbox
    rel_coor = [left_spacing, bbox_height / 2]

    # creates gate
    if name == "Or":
        gate = logic.Or(inputs=num_in)
        bbox_width = 1.95 + left_spacing + right_spacing
    elif name == "Nor":
        gate = logic.Nor(inputs=num_in)
        bbox_width = 1.95 + left_spacing + right_spacing
    elif name == "And":
        gate = logic.And(inputs=num_in)
        bbox_width = 1.9 + left_spacing + right_spacing
    elif name == "Nand":
        gate = logic.Nand(inputs=num_in)
        bbox_width = 1.9 + left_spacing + right_spacing
    elif name == "Xor":
        gate = logic.Xor(inputs=num_in)
        bbox_width = 2.1 + left_spacing + right_spacing
    elif name == "Xnor":
        gate = logic.Xnor(inputs=num_in)
        bbox_width = 2.1 + left_spacing + right_spacing
    else:
        gate = logic.Not()
        if short_ov_input[0] != "---":
            gate.label(short_ov_input[0], loc="in", ofst=[-1, -0.1], fontsize=11, halign="right")
        if short_ov_output[0] != "---":
            gate.label(short_ov_output[0], loc="out", ofst=[1, -0.1], fontsize=11, halign="left")
        bbox_width = 3 + left_spacing + right_spacing
        return gate, [bbox_width, bbox_height], rel_coor

    # label's gate's pins
    if num_in > 0:
        for i in range(0, num_in):
            if (name == "Xor") or (name == "Xnor"):
                gate.label(input_pins[i], loc="in" + str(i + 1), ofst=[1, 0], fontsize=11)
                gate.label("out", loc="out", ofst=[-1, 0], fontsize=10)
            elif (name == "Or") or (name == "Nor"):
                gate.label(input_pins[i], loc="in" + str(i + 1), ofst=[0.85, 0], fontsize=11)
                gate.label("out", loc="out", ofst=[-1, 0], fontsize=10)
            else:
                gate.label(input_pins[i], loc="in" + str(i + 1), ofst=[0.65, 0], fontsize=11)
                gate.label("out", loc="out", ofst=[-0.9, 0], fontsize=10)

    # adds overall inputs and outputs
    for i in range(0, num_in):
        if short_ov_input[i] != "---":
            gate.label(short_ov_input[i], loc="in" + str(i + 1), fontsize=11)
    if short_ov_output[0] != "---":
        gate.label(short_ov_output[0], loc="out", fontsize=11)

    return gate, [bbox_width, bbox_height], rel_coor


def chip_designer(gmatrix, phdl):
    # adds all gate information to phdl dictionary

    # need to first reorder pins/wires to prevent overlapping wires

    # note all wires that need to be reordered (all wires that end horizontally)
    for j in range(0, len(gmatrix[0])):
        for i in range(0, len(gmatrix)):
            ind = gmatrix[i][j]
            if ind != -1:
                gate = phdl["parts"][ind]
                for wires in gate["external"]:
                    if not wires["overall"] and wires["inout"] == "out":
                        for path in wires["path"]:
                            if (len(path) == 2) or ((path[-3][0] == path[-2][0]) and (path[-2][0] == path[-1][0])):
                                end_ind = gmatrix[path[-1][0]][path[-1][1]]
                                end_gate = phdl["parts"][end_ind]
                                for e in range(0, len(end_gate["external"])):
                                    if end_gate["external"][e]["name"] == wires["name"]:
                                        end_gate["external"][e]["special"] = True

    # move pins receiving output from horizontally entering wire first in phdl dictionary
    for j in range(0, len(gmatrix[0])):
        for i in range(0, len(gmatrix)):
            ind = gmatrix[i][j]
            if ind != -1:
                gate = phdl["parts"][ind]
                for wires in gate["external"]:
                    if not wires["overall"] and wires["inout"] == "out":
                        for path in wires["path"]:
                            if (len(path) == 2) or ((path[-3][0] == path[-2][0]) and (path[-2][0] == path[-1][0])):
                                end_ind = gmatrix[path[-1][0]][path[-1][1]]
                                end_gate = phdl["parts"][end_ind]
                                for e in range(0, len(end_gate["external"])):
                                    if end_gate["external"][e]["name"] == wires["name"]:
                                        add_ind = -1
                                        for f in range(0, len(end_gate["external"])):
                                            if end_gate["external"][f]["inout"] == "in":
                                                if "special" in end_gate["external"][f].keys():
                                                    if "final" not in end_gate["external"][f].keys():
                                                        end_gate["external"][e]["final"] = True
                                                        add_ind = f
                                                        break

                                        temp1 = end_gate["external"][add_ind]
                                        end_gate["external"][add_ind] = end_gate["external"][e]
                                        end_gate["external"][e] = temp1

                                        temp2 = end_gate["internal"][add_ind]
                                        end_gate["internal"][add_ind] = end_gate["internal"][e]
                                        end_gate["internal"][e] = temp2

    elem_gates = ["And", "Nand", "Or", "Nor", "Xor", "Xnor", "Not"]

    # adds gate object to each chip
    for gate in phdl["parts"]:

        # gets pin information
        input_pins = []
        in_pin_sizes = []
        output_pins = []
        out_pin_sizes = []
        for i in gate["internal"]:
            if i["inout"] == "in":
                in_pin_sizes.append(i["end"] - i["start"] + 1)
                if not i["spec_by_user"]:
                    input_pins.append(i["name"])
                else:
                    if i["start"] != i["end"]:
                        input_pins.append(i["name"] + "[" + str(i["start"]) + ":" + str(i["end"]) + "]")
                    else:
                        input_pins.append(i["name"] + "[" + str(i["start"]) + "]")

            else:
                out_pin_sizes.append(i["end"] - i["start"] + 1)
                if not i["spec_by_user"]:
                    output_pins.append(i["name"])
                else:
                    if i["start"] != i["end"]:
                        output_pins.append(i["name"] + "[" + str(i["start"]) + ":" + str(i["end"]) + "]")
                    else:
                        output_pins.append(i["name"] + "[" + str(i["start"]) + "]")

        # gets overall input wire information (and true or false inputs)
        ov_input = []
        for i in gate["external"]:
            if i["inout"] == "in":
                if (i["name"] == "true") or (i["name"] == "false"):
                    ov_input.append(i["name"])
                elif i["overall"]:
                    if not i["spec_by_user"]:
                        ov_input.append(i["name"])
                    else:
                        if i["start"] != i["end"]:
                            ov_input.append(i["name"] + "[" + str(i["start"]) + ":" + str(i["end"]) + "]")
                        else:
                            ov_input.append(i["name"] + "[" + str(i["start"]) + "]")
                else:
                    ov_input.append("---")

        # gets overall output wire information
        ov_output = []
        for i in gate["external"]:
            if i["inout"] == "out":
                if i["overall"]:
                    if not i["spec_by_user"]:
                        ov_output.append(i["name"])
                    else:
                        if i["start"] != i["end"]:
                            ov_output.append(i["name"] + "[" + str(i["start"]) + ":" + str(i["end"]) + "]")
                        else:
                            ov_output.append(i["name"] + "[" + str(i["start"]) + "]")
                else:
                    ov_output.append("---")

        # gate maker
        if gate["name"] in elem_gates and not gate["custom_pins"]:
            chip, bbox_size, rel_coor = elem_gate_maker(gate["name"], input_pins, ov_input, ov_output)

        elif gate["name"] == "Mux" and not gate["custom_pins"]:
            chip, bbox_size, rel_coor = mux_dmux(False, input_pins, output_pins, ov_input, ov_output)

        elif gate["name"] == "DMux" and not gate["custom_pins"]:
            chip, bbox_size, rel_coor = mux_dmux(True, input_pins, output_pins, ov_input, ov_output)

        else:
            chip, bbox_size, rel_coor = generic_gate_maker(gate["name"], input_pins, output_pins,
                                                           ov_input, ov_output, in_pin_sizes, out_pin_sizes)

        # adds to phdl["parts"] dictionary
        gate["gate"] = chip
        gate["bbox_size"] = bbox_size
        gate["rel_coor"] = rel_coor
