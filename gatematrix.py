from nand2tetris_hdl_parser import parse_hdl
import getpins
import numpy as np

# the gate_matrix function
# takes a path to an hdl file
# returns a gate matrix (numpy array) and parsed hdl file
# the gate matrix contains indices referring to parsed hdl file's "parts" array
# example
#   path = r"C:\Users\prana\Desktop\hdl_direc\LogicGate2.hdl"
#   phdl, gmatrix = gm.gate_matrix(path)
# gmatrix's indices refer to elements in phdl["parts"]


def gate_matrix(path):
    og_file = open(path, "r")
    phdl = parse_hdl(og_file.read())

    # adjust pins of overall chip
    for i in phdl["inputs"]:
        if i["end"] != 0:
            i["start"] = 0
            i["end"] = i["end"] - 1

    for i in phdl["outputs"]:
        if i["end"] != 0:
            i["start"] = 0
            i["end"] = i["end"] - 1

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
                    if input_arr[ind]["end"] == 0:
                        phdl["parts"][i]["internal"][j]["end"] = input_arr[ind]["end"]
                    else:
                        phdl["parts"][i]["internal"][j]["end"] = input_arr[ind]["end"] - 1
                else:
                    if output_arr[ind]["end"] == 0:
                        phdl["parts"][i]["internal"][j]["end"] = output_arr[ind]["end"]
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

    # Creates large matrix
    # values are indices of phdl["parts"] array
    matrix_data = []

    prv_outs = []
    for i in phdl['inputs']:
        prv_outs.append(i["name"])

    unused_ind = list(range(0, num_chips))
    max_row = -1
    max_col = -1
    for k in range(0, num_chips):
        nxt_outs = []
        nxt_row = 0
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
                row = 2 * nxt_row + 1
                col = 2 * k + 1
                matrix_data.append([row, col, i])
                if row > max_row:
                    max_row = row
                if col > max_col:
                    max_col = col
                nxt_row += 1
                for lead in chip["external"]:
                    if lead["inout"] == "out":
                        nxt_outs.append(lead["name"])

        for i in ind_rem:
            unused_ind.remove(i)
        prv_outs = nxt_outs

    lm_row = max_row + 2
    lm_col = max_col + 2
    lm = np.zeros([lm_row, lm_col]) - 1
    for val in matrix_data:
        lm[val[0], val[1]] = val[2]


    # centers blocks in large matrix
    for i in range(1, lm_col, 2):
        indices = []
        for j in range(1, lm_row, 2):
            if lm[j][i] != -1:
                indices.append(j)
            else:
                break
        avg = sum(indices)/len(indices)
        shift = int(np.floor(lm_row/2) - avg)
        for j in reversed(indices):
            temp = lm[j][i]
            lm[j][i] = -1
            lm[j+shift][i] = temp
            phdl["parts"][int(temp)]["coord"] = [j+shift, i]

    return lm, phdl
