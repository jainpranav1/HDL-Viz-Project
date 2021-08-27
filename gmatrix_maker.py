# README
# to use:
# import gmatrix_maker as gm
#
# Function gmatrix_maker
# gm.gmatrix_maker(path, max_to_col)
# "path" is path of hdl file
# returns phdl dictionary (parsed hdl file) and gmatrix (matrix of gates)
# values of gmatrix are indices of phdl["parts"] array
#
# example:
#    path = r"C:\Users\prana\Desktop\csce_312_files\CPU.hdl"
#    gmatrix, phdl = gm.gmatrix_maker(path, 4)

import get_phdl as gph
import math as m
import statistics as s
import extra_functions as ef


def gmatrix_maker(path):
    phdl = gph.get_phdl(path)

    # Creates gate matrix (gmatrix)
    # values of gmatrix reference different chips
    # specifically, values of gmatrix are indices of phdl["parts"] array

    # specifies the maximum number of gates per column
    max_to_col = 4

    # specifies maximum number of gates at which centering placing algorithm is used
    max_gates = 20

    # centering placing algorithm
    if len(phdl["parts"]) <= max_gates:
        # create gmatrix_prep array, which contains the indices in the order to be placed
        gmatrix_prep = []
        prv_outs = []
        chips = phdl["parts"]
        for c in range(0, len(chips)):
            all_ov_inputs = True
            for wire in chips[c]["external"]:
                if wire["inout"] == "in" and not wire["overall"]:
                    all_ov_inputs = False

            if all_ov_inputs:
                if len(gmatrix_prep) == 0:
                    gmatrix_prep.append([])
                gmatrix_prep[0].append(c)

                for wire in chips[c]["external"]:
                    if wire["inout"] == "out" and not wire["overall"]:
                        prv_outs.append(wire["name"])

        num_chips = len(phdl["parts"])
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
        num_rows = 2 * max_to_col + 1
        num_cols = 2 * len(gmatrix_prep_short) + 1
        gmatrix = ef.matrix_maker(num_rows, num_cols, -1)

        # places gates in gmatrix
        for i in range(0, len(gmatrix_prep_short)):
            avg = 2 * s.mean(list(range(0, len(gmatrix_prep_short[i])))) + 1
            shift = int(m.floor(num_rows / 2) - avg)
            for j in range(0, len(gmatrix_prep_short[i])):
                ind = gmatrix_prep_short[i][j]
                row = 2 * j + 1 + shift
                col = 2 * i + 1
                gmatrix[row][col] = ind
                phdl["parts"][ind]["coord"] = [row, col]

    # non-centering placing algorithm
    else:
        # create gmatrix_prep array, which contains the indices in the order to be placed
        gmatrix_prep = []
        prv_outs = []
        chips = phdl["parts"]
        for c in range(0, len(chips)):
            all_ov_inputs = True
            for wire in chips[c]["external"]:
                if wire["inout"] == "in" and not wire["overall"]:
                    all_ov_inputs = False

            if all_ov_inputs:
                gmatrix_prep.append(c)

                for wire in chips[c]["external"]:
                    if wire["inout"] == "out" and not wire["overall"]:
                        prv_outs.append(wire["name"])

        num_chips = len(phdl["parts"])
        if len(gmatrix_prep) == 0:
            for i in phdl['inputs']:
                prv_outs.append(i["name"])

        if len(gmatrix_prep) != 0:
            unused_ind = []
            for i in range(0, num_chips):
                if i not in gmatrix_prep:
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

            for i in ind_rem:
                gmatrix_prep.append(i)
                unused_ind.remove(i)
            prv_outs = nxt_outs

        # creates matrix and adds gates
        num_rows = 2 * max_to_col + 1
        num_cols = 2 * m.ceil(len(gmatrix_prep) / max_to_col) + 1
        gmatrix = ef.matrix_maker(num_rows, num_cols, -1)

        # places gates in gmatrix
        counter_row = 0
        counter_col = 0
        for i in gmatrix_prep:
            gmatrix[2*counter_row + 1][2*counter_col + 1] = i
            phdl["parts"][i]["coord"] = [2*counter_row + 1, 2*counter_col + 1]

            if counter_row == max_to_col - 1:
                counter_row = 0
                counter_col += 1
            else:
                counter_row += 1


    return gmatrix, phdl
