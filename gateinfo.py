import gatedata as gd
import schemdraw
import schemdraw.elements as elm
from schemdraw.segments import *
from schemdraw.logic import *

def ov_pin_spacing(pins):
    spacing = 1.4
    for i in pins:
        if (i != "---"):
            return spacing
    return 0

def shorten_pins(pins):
    short_pins = []
    max_length_1 = 3
    max_length_2 = 6
    for p in pins:
        ind = p.find("[")

        # if [ is present (ex. in[0:3]
        if ind != -1:
            name = p[0:ind]
            if len(name) > max_length_1:
                short_pins.append(p[0:(max_length_1-1)] + "..." + p[ind:])
            else:
                short_pins.append(p)

        else:
            if len(p) > max_length_2:
                short_pins.append(p[0:(max_length_2-1)] + "...")
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
    label_width = 1.5

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
    gate = elm.Ic(pins=pins, size=[2*label_width, 0.8 * max_pins], edgepadH=0.05, plblsize=11, plblofst=0.1).label(name, "top", fontsize=11)

    # pins are 0.5, top label is 0.5
    horiz_padding = 0.1
    top_padding = 0.5
    bottom_padding = 0.1

    left_spacing = ov_pin_spacing(ov_input)
    right_spacing = ov_pin_spacing(ov_output)

    size_bbox = [2*label_width + 1 + (2*horiz_padding) + left_spacing + right_spacing, (0.8 * max_pins) + top_padding + bottom_padding]

    # coordinates of gate relative to bbox
    rel_coor = [horiz_padding + 0.5 + left_spacing, bottom_padding]

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
    vert_padding = 0.1
    horiz_padding = 0.1

    right_spacing = ov_pin_spacing(ov_output)

    # adds spacing in case their are overall inputs / outputs
    left_spacing = 0
    for i in range(0, num_inputs):
        if (ov_input[i] != "---") and (input_pins[i] != "sel"):
            left_spacing += 1.4
            break

    top_spacing = 0
    for i in range(0, num_inputs):
        if (ov_input[i] != "---") and (input_pins[i] == "sel"):
            top_spacing += 0.5
            break

    size_bbox = [(2*horiz_padding) + 2.25 + right_spacing + left_spacing, (2*vert_padding) + 2.47 + top_spacing]

    # coordinates of gate relative to bbox
    rel_coor = [horiz_padding + 0.5 + left_spacing, vert_padding + 0.47]

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
                gate.label(short_ov_input[i], loc="inL" + str(count+1), fontsize=11)
            count += 1
    for i in range(0, num_outputs):
        if short_ov_output[i] != "---":
            gate.label(short_ov_output[i], loc="inR" + str(num_outputs-i), fontsize=11)

    return gate, size_bbox, rel_coor

def elem_gate_maker(name, input_pins, ov_input, ov_output):
    short_ov_input = shorten_pins(ov_input)
    short_ov_output = shorten_pins(ov_output)

    num_in = len(input_pins)

    # height of gates is 1
    # width of gates varies
    vert_padding = 0.1
    horiz_padding = 0.1

    left_spacing = ov_pin_spacing(ov_input)
    right_spacing = ov_pin_spacing(ov_output)

    bbox_height = 1 + (2*vert_padding)

    # coordinates of gate relative to bbox
    rel_coor = [horiz_padding + left_spacing, bbox_height/2]

    # creates gate
    if name == "Or":
        gate = logic.Or(inputs=num_in)
        bbox_width = 1.95 + (2 * horiz_padding) + left_spacing + right_spacing
    elif name == "Nor":
        gate = logic.Nor(inputs=num_in)
        bbox_width = 1.95 + (2 * horiz_padding) + left_spacing + right_spacing
    elif name == "And":
        gate = logic.And(inputs=num_in)
        bbox_width = 1.9 + (2 * horiz_padding) + left_spacing + right_spacing
    elif name == "Nand":
        gate = logic.Nand(inputs=num_in)
        bbox_width = 1.9 + (2 * horiz_padding) + left_spacing + right_spacing
    elif name == "Xor":
        gate = logic.Xor(inputs=num_in)
        bbox_width = 2.1 + (2 * horiz_padding) + left_spacing + right_spacing
    elif name == "Xnor":
        gate = logic.Xnor(inputs=num_in)
        bbox_width = 2.1 + (2 * horiz_padding) + left_spacing + right_spacing
    else:
        gate = logic.Not()
        if short_ov_input[0] != "---":
            gate.label(short_ov_input[0], loc="in", ofst=[-1, -0.1], fontsize=11, halign="right")
        if short_ov_output[0] != "---":
            gate.label(short_ov_output[0], loc="out", ofst=[1, -0.1], fontsize=11, halign="left")
        bbox_width = 3 + (2 * horiz_padding) + left_spacing + right_spacing
        return gate, [bbox_width, bbox_height], rel_coor

    # label's gate's pins
    if num_in > 0:
        for i in range(0, num_in):
            if (name == "Xor") or (name == "Xnor"):
                gate.label(input_pins[i], loc="in" + str(i+1), ofst=[1, 0], fontsize=11)
                gate.label("out", loc="out", ofst=[-1, 0], fontsize=10)
            elif (name == "Or") or (name == "Nor"):
                gate.label(input_pins[i], loc="in" + str(i+1), ofst=[0.85, 0], fontsize=11)
                gate.label("out", loc="out", ofst=[-1, 0], fontsize=10)
            else:
                gate.label(input_pins[i], loc="in" + str(i+1), ofst=[0.65, 0], fontsize=11)
                gate.label("out", loc="out", ofst=[-0.9, 0], fontsize=10)

    # adds overall inputs and outputs
    for i in range(0, num_in):
        if short_ov_input[i] != "---":
            gate.label(short_ov_input[i], loc="in" + str(i+1), fontsize=11)
    if short_ov_output[0] != "---":
        gate.label(short_ov_output[0], loc="out", fontsize=11)

    return gate, [bbox_width, bbox_height], rel_coor

# adds gate information to phdl dictionary

def gate_info(phdl):

    elem_gates = ["And", "Nand", "Or", "Nor", "Xor", "Xnor", "Not"]

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
                    input_pins.append(i["name"] + "[" + str(i["start"]) + ":" + str(i["end"]) + "]")

            else:
                out_pin_sizes.append(i["end"] - i["start"] + 1)
                if not i["spec_by_user"]:
                    output_pins.append(i["name"])
                else:
                    output_pins.append(i["name"] + "[" + str(i["start"]) + ":" + str(i["end"]) + "]")

        # gets overall input wire information (and true or false inputs)
        ov_input = []
        for i in gate["external"]:
            if i["inout"] == "in":
                if (i["name"] == "true") or (i["name"] == "false"):
                    ov_input.append(i["name"])
                elif i["overall"] == "in":
                    if not i["spec_by_user"]:
                        ov_input.append(i["name"])
                    else:
                        ov_input.append(i["name"] + "[" + str(i["start"]) + ":" + str(i["end"]) + "]")
                else:
                    ov_input.append("---")

        # gets overall output wire information
        ov_output = []
        for i in gate["external"]:
            if i["inout"] == "out":
                if i["overall"] == "out":
                    if not i["spec_by_user"]:
                        ov_output.append(i["name"])
                    else:
                        ov_output.append(i["name"] + "[" + str(i["start"]) + ":" + str(i["end"]) + "]")
                else:
                    ov_output.append("---")

        # gate maker
        if gate["name"] in elem_gates:
            chip, bbox_size, rel_coor = elem_gate_maker(gate["name"], input_pins, ov_input, ov_output)
        elif gate["name"] == "Mux":
            chip, bbox_size, rel_coor = mux_dmux(False, input_pins, output_pins, ov_input, ov_output)
        else:
            chip, bbox_size, rel_coor = generic_gate_maker(gate["name"], input_pins, output_pins, ov_input, ov_output, in_pin_sizes, out_pin_sizes)

        # adds to phdl["parts"] dictionary
        gate["gate"] = chip
        gate["bbox_size"] = bbox_size
        gate["rel_coor"] = rel_coor
