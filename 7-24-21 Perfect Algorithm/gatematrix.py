from nand2tetris_hdl_parser import parse_hdl
import getpins
import numpy as np
import math

# the gate_matrix function
# takes a path to an hdl file and max number of gates in column
# returns a gate matrix (numpy array) and parsed hdl file
# the gate matrix contains indices referring to parsed hdl file's "parts" array
# example
#   import gatematrix as gm
#   path = r"C:\Users\prana\Desktop\hdl_direc\LogicGate2.hdl"
#   phdl, gmatrix = gm.gate_matrix(path, max_to_col)
# gmatrix's indices refer to elements in phdl["parts"]


def gate_matrix(path, max_to_col):
    og_file = open(path, "r")
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
        if i["end"] != 0:
            i["start"] = 0
            i["end"] = i["end"] - 1
        else:
            i["start"] = 0
            i["end"] = 0

    # phdl["parts"] is an array of internal chip dictionaries
    num_chips = len(phdl["parts"])
    for i in range(0, num_chips):
        input_arr, output_arr = getpins.get_pins(phdl["parts"][i], og_file)

        ind = -1
        # Adds inout to each pin and wire
        for j in range(0, len(phdl["parts"][i]["internal"])):
            found = False
            for l in range(0, len(input_arr)):
                if phdl["parts"][i]["internal"][j]["name"] == input_arr[l]["name"]:
                    found = True
                    ind = l
                    break
            if found:
                phdl["parts"][i]["internal"][j]["inout"] = "in"
                phdl["parts"][i]["external"][j]["inout"] = "in"
            else:
                phdl["parts"][i]["internal"][j]["inout"] = "out"
                phdl["parts"][i]["external"][j]["inout"] = "out"

                for m in range(0, len(output_arr)):
                    if phdl["parts"][i]["internal"][j]["name"] == output_arr[m]["name"]:
                        ind = m
                        break

            # fixes start and end of wires and pins
            if phdl["parts"][i]["internal"][j]["end"] == -1:
                phdl["parts"][i]["internal"][j]["spec_by_user"] = False
                phdl["parts"][i]["internal"][j]["start"] = 0
                if phdl["parts"][i]["internal"][j]["inout"] == "in":
                    if (input_arr[ind]["end"] == 0) or (input_arr[ind]["end"] == -1):
                        phdl["parts"][i]["internal"][j]["end"] = 0
                    else:
                        phdl["parts"][i]["internal"][j]["end"] = input_arr[ind]["end"] - 1
                else:
                    if (output_arr[ind]["end"] == 0) or (output_arr[ind]["end"] == -1):
                        phdl["parts"][i]["internal"][j]["end"] = 0
                    else:
                        phdl["parts"][i]["internal"][j]["end"] = output_arr[ind]["end"] - 1
            else:
                phdl["parts"][i]["internal"][j]["spec_by_user"] = True

            if phdl["parts"][i]["external"][j]["end"] == -1:
                phdl["parts"][i]["external"][j]["start"] = 0
                stop = phdl["parts"][i]["internal"][j]["end"]
                begin = phdl["parts"][i]["internal"][j]["start"]
                size = stop - begin
                phdl["parts"][i]["external"][j]["end"] = size
                phdl["parts"][i]["external"][j]["spec_by_user"] = False
            else:
                phdl["parts"][i]["external"][j]["spec_by_user"] = True


    # Creates gate matrix
    # values are indices of phdl["parts"] array

    # gets order of indices in gate matrix
    matrix_data = []

    prv_outs = []
    for i in phdl['inputs']:
        prv_outs.append(i["name"])

    unused_ind = list(range(0, num_chips))
    for k in range(0, num_chips):
        nxt_outs = []
        ind_rem = []
        for i in unused_ind:
            found = False
            chip = phdl["parts"][i]
            for wire in chip["external"]:
                if (wire["name"] in prv_outs) and (wire["inout"] == "in"):
                    found = True
                    break
            if found:
                ind_rem.append(i)
                matrix_data.append(i)
                for lead in chip["external"]:
                    if lead["inout"] == "out":
                        nxt_outs.append(lead["name"])

        for i in ind_rem:
            unused_ind.remove(i)
        prv_outs = nxt_outs


    # creates matrix and adds gates
    num_ind = len(matrix_data)
    num_rows = 2*max_to_col + 1
    temp = math.ceil(num_ind/max_to_col)
    num_cols = 2*temp + 1
    gmatrix = np.zeros([num_rows, num_cols]).astype(int) - 1

    counter = 0
    for i in range(0, temp):
        for j in range(0, max_to_col):
            if counter < num_ind:
                gmatrix[2*j + 1][2*i + 1] = matrix_data[counter]
                phdl["parts"][matrix_data[counter]]["coord"] = [2*j + 1, 2*i + 1]
                counter += 1


    return gmatrix, phdl