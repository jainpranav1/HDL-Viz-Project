from nand2tetris_hdl_parser import parse_hdl
import getpins
import numpy as np
import random

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


    # list of overall chip's outputs
    ov_out = []
    for p in phdl["outputs"]:
        ov_out.append(p["name"])

    # list of overall chip's inputs
    ov_in = []
    for p in phdl["inputs"]:
        ov_in.append(p["name"])

    # adds "overall" information to wires (determines whether connected to outer pin)
    for p in phdl["parts"]:
        for k in p["external"]:
            if k["inout"] == "in":
                if k["name"] in ov_in:
                    k["overall"] = "in"
                else:
                    k["overall"] = "none"
            else:
                if k["name"] in ov_out:
                    k["overall"] = "out"
                else:
                    k["overall"] = "none"

    # Creates gate matrix
    # values are indices of phdl["parts"] array

    # create gmatrix_prep array, which contains the indices in the order to be placed
    gmatrix_prep = []
    prv_outs = []
    chips = phdl["parts"]
    for c in range(0, len(chips)):
        all_ov_inputs = True
        for wire in chips[c]["external"]:
            if wire["inout"] == "in" and wire["overall"] == "none":
                all_ov_inputs = False

        if all_ov_inputs:
            if len(gmatrix_prep) == 0:
                gmatrix_prep.append([])
            gmatrix_prep[0].append(c)

            for wire in chips[c]["external"]:
                if wire["inout"] == "out" and wire["overall"] == "none":
                    prv_outs.append(wire["name"])

    if len(gmatrix_prep) == 0:
        for i in phdl['inputs']:
            prv_outs.append(i["name"])

    if len(gmatrix_prep) != 0:
        unused_ind = []
        for i in range(0, num_chips):
            if i not in gmatrix_prep[0]:
                unused_ind.append(i)
    else:
        unused_ind = list(range(0, num_chips))

    while len(unused_ind) != 0:
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
                for lead in chip["external"]:
                    if lead["inout"] == "out":
                        nxt_outs.append(lead["name"])

        gmatrix_prep.append(ind_rem)
        for i in ind_rem:
            unused_ind.remove(i)
        prv_outs = nxt_outs

    # limits number of gates per column in gmatrix_prep array
    gmatrix_prep_short = []
    for g in gmatrix_prep:
        counter = 0
        temp = []
        for i in g:
            if counter >= max_to_col:
                gmatrix_prep_short.append(temp)
                temp = [i]
                counter = 1
            else:
                temp.append(i)
                counter += 1

        if counter != 0:
            gmatrix_prep_short.append(temp)

    # creates matrix and adds gates
    num_rows = 2*max_to_col + 1
    num_cols = 2*len(gmatrix_prep_short) + 1
    gmatrix = np.zeros([num_rows, num_cols]).astype(int) - 1

    # places gates in gmatrix
    for i in range(0, len(gmatrix_prep_short)):
        avg = 2 * np.mean(list(range(0, len(gmatrix_prep_short[i])))) + 1
        shift = int(np.floor(num_rows/2) - avg)
        for j in range(0, len(gmatrix_prep_short[i])):
            ind = gmatrix_prep_short[i][j]
            row = 2*j + 1 + shift
            col = 2*i + 1
            gmatrix[row][col] = ind
            phdl["parts"][ind]["coord"] = [row, col]

    return gmatrix, phdl