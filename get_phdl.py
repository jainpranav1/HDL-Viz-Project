# README
# to use:
# import get_phdl as gph
#
# Function get_phdl
# gph.get_phdl(path)
# "path" is path of hdl file
# returns phdl dictionary (parsed hdl file)
#
# example:
#    path = r"C:\Users\prana\Desktop\csce_312_files\CPU.hdl"
#    phdl = gph.get_phdl(path)

from nand2tetris_hdl_parser import parse_hdl
import get_pins as gpi


def get_phdl(path):
    og_file = open(path, "r")

    # phdl stands for parsed hdl
    phdl = parse_hdl(og_file.read())

    # adjust pins of overall chip
    for i in phdl["inputs"]:
        if i["end"] != -1:
            i["start"] = 0
            i["end"] = i["end"] - 1
        else:
            i["start"] = 0
            i["end"] = 0

    for i in phdl["outputs"]:
        if i["end"] != -1:
            i["start"] = 0
            i["end"] = i["end"] - 1
        else:
            i["start"] = 0
            i["end"] = 0

    # phdl["parts"] is an array of internal chip dictionaries
    for chip in phdl["parts"]:
        input_arr, output_arr = gpi.get_pins(chip, og_file)

        # Adds inout to each pin and wire
        # inout specifies whether each pin/wires is an input or output pin/wire
        ind = -1
        for j in range(0, len(chip["internal"])):
            found = False
            for l in range(0, len(input_arr)):
                if chip["internal"][j]["name"] == input_arr[l]["name"]:
                    found = True
                    ind = l
                    break
            if found:
                chip["internal"][j]["inout"] = "in"
                chip["external"][j]["inout"] = "in"
            else:
                chip["internal"][j]["inout"] = "out"
                chip["external"][j]["inout"] = "out"

                for m in range(0, len(output_arr)):
                    if chip["internal"][j]["name"] == output_arr[m]["name"]:
                        ind = m
                        break

            # fixes start and end of wires and pins
            if chip["internal"][j]["end"] == -1:
                chip["internal"][j]["spec_by_user"] = False
                chip["internal"][j]["start"] = 0
                if chip["internal"][j]["inout"] == "in":
                    if input_arr[ind]["end"] == -1:
                        chip["internal"][j]["end"] = 0
                    else:
                        chip["internal"][j]["end"] = input_arr[ind]["end"] - 1
                else:
                    if output_arr[ind]["end"] == -1:
                        chip["internal"][j]["end"] = 0
                    else:
                        chip["internal"][j]["end"] = output_arr[ind]["end"] - 1
            else:
                chip["internal"][j]["spec_by_user"] = True

            if chip["external"][j]["end"] == -1:
                chip["external"][j]["start"] = 0
                stop = chip["internal"][j]["end"]
                begin = chip["internal"][j]["start"]
                size = stop - begin
                chip["external"][j]["end"] = size
                chip["external"][j]["spec_by_user"] = False
            else:
                chip["external"][j]["spec_by_user"] = True

    # list of overall chip's outputs
    ov_out = []
    for p in phdl["outputs"]:
        ov_out.append(p["name"])

    # list of overall chip's inputs
    ov_in = []
    for p in phdl["inputs"]:
        ov_in.append(p["name"])

    # adds "overall" to each wire
    # "overall" specifies if wire is connected to outer pin or not
    for p in phdl["parts"]:
        for k in p["external"]:
            if k["inout"] == "in":
                if k["name"] in ov_in:
                    k["overall"] = True
                else:
                    k["overall"] = False
            else:
                if k["name"] in ov_out:
                    k["overall"] = True
                else:
                    k["overall"] = False

    # adds wire_direc to each input wire
    # wire_direc specifies if input wire should come from left or top
    for p in phdl["parts"]:
        for k in range(0, len(p["external"])):
            if p["external"][k]["inout"] == "in":
                if not p["custom_pins"]:
                    if ((p["name"] == "Mux") or (p["name"] == "DMux")) and (p["internal"][k]["name"] == "sel"):
                        p["external"][k]["wire_direc"] = "top"
                    else:
                        p["external"][k]["wire_direc"] = "left"
                else:
                    p["external"][k]["wire_direc"] = "left"

    return phdl

