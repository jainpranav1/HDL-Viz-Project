# README
# to use:
# import path_finder as pf
#
# Function path_finder
# pf.path_finder(path)
# "path" is path of hdl file
# returns phdl dictionary (parsed hdl file), and gmatrix
# the path_finder function adds gmatrix path to each wire
#
# example:
#    path = r"C:\Users\prana\Desktop\csce_312_files\CPU.hdl"
#    gmatrix, phdl = pf.path_finder(path, 4)

import gmatrix_maker as gm
import extra_functions as ef


def short_path(start, end, matrix, wire_direc):
    # gets shortest path from "start" to "end"

    curr = ef.sum_lists([start, [0, 1]])
    coordinates = [curr]

    # for non-mux/dmux gates
    if wire_direc == "left":
        before_end = ef.sum_lists([end, [0, -1]])

        # curr moves horizontally until in correct column, then moves vertically to end
        while curr != before_end:
            if curr[1] == before_end[1]:
                # moves up or down
                if curr[0] < before_end[0]:
                    curr = [curr[0] + 1, curr[1]]
                else:
                    curr = [curr[0] - 1, curr[1]]
            else:
                if curr[1] < before_end[1]:
                    # moves right or prepares to move right
                    if matrix[curr[0]][curr[1] + 1] == -1:
                        curr = [curr[0], curr[1] + 1]
                    else:
                        if curr[0] < before_end[0]:
                            curr = [curr[0] + 1, curr[1]]
                        else:
                            curr = [curr[0] - 1, curr[1]]
                else:
                    # moves left or prepares to move left
                    if matrix[curr[0]][curr[1] - 1] == -1:
                        curr = [curr[0], curr[1] - 1]
                    else:
                        if curr[0] < before_end[0]:
                            curr = [curr[0] + 1, curr[1]]
                        else:
                            curr = [curr[0] - 1, curr[1]]
            coordinates.append(curr)
        coordinates.append(end)

    # for mux/dmux gates
    else:
        # curr moves horizontally until in left or right, then moves vertically to end
        before_end = ef.sum_lists([end, [-1, 0]])
        left = ef.sum_lists([before_end, [0, -1]])
        right = ef.sum_lists([before_end, [0, 1]])

        while (curr != left) and (curr != right):
            print('a')
            if abs(curr[1] - before_end[1]) == 1:
                # moves up or down
                if curr[0] < before_end[0]:
                    curr = [curr[0] + 1, curr[1]]
                else:
                    curr = [curr[0] - 1, curr[1]]
            else:
                if curr[1] < before_end[1]:
                    # moves right or prepares to move right
                    if matrix[curr[0]][curr[1] + 1] == -1:
                        curr = [curr[0], curr[1] + 1]
                    else:
                        if curr[0] < before_end[0]:
                            curr = [curr[0] + 1, curr[1]]
                        else:
                            curr = [curr[0] - 1, curr[1]]
                else:
                    # moves left or prepares to move left
                    if matrix[curr[0]][curr[1] - 1] == -1:
                        curr = [curr[0], curr[1] - 1]
                    else:
                        if curr[0] < before_end[0]:
                            curr = [curr[0] + 1, curr[1]]
                        else:
                            curr = [curr[0] - 1, curr[1]]
            coordinates.append(curr)
        coordinates.append(before_end)
        coordinates.append(end)

    return coordinates


def path_finder(path):
    gmatrix, phdl = gm.gmatrix_maker(path)

    num_rows = len(gmatrix)
    num_cols = len(gmatrix[0])

    end_dic = {}
    # stores each wire's end point (position on gmatrix) and wire_direc on end_dic dictionary
    for p in phdl["parts"]:
        for wire in p["external"]:
            if wire["inout"] == "in":
                if wire["name"] in end_dic:
                    end_dic[wire["name"]].append([wire["wire_direc"], p["coord"]])
                else:
                    end_dic[wire["name"]] = [[wire["wire_direc"], p["coord"]]]

    # remove wires that don't connect anywhere
    for p in phdl["parts"]:
        new_list_ext = []
        new_list_int = []
        for w in range(0, len(p["external"])):
            wire = p["external"][w]
            pin = p["internal"][w]
            if (wire["inout"] == "out") and not wire["overall"]:
                if wire["name"] in end_dic:
                    new_list_ext.append(wire)
                    new_list_int.append(pin)
            else:
                new_list_ext.append(wire)
                new_list_int.append(pin)

        p["external"] = new_list_ext
        p["internal"] = new_list_int

    # adds "path" to each output wire
    # "path" specifies each wire's path on gmatrix
    for p in phdl["parts"]:
        for wire in p["external"]:
            if (wire["inout"] == "out") and not wire["overall"]:
                for end in end_dic[wire["name"]]:
                    start = p["coord"]
                    path = short_path(start, end[1], gmatrix, end[0])
                    if "path" in wire:
                        wire["path"].append(path)
                    else:
                        wire["path"] = [path]

    return gmatrix, phdl
