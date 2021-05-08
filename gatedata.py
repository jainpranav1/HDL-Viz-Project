import gatematrix as gm
import numpy as np

def sum1(a, b):
    return [a[0] + b[0], a[1] + b[1]]

def equal1(a, b):
    if (a[0] == b[0]) and (a[1] == b[1]):
        return True
    else:
        return False

def short_path(start, end, matrix):
    curr = start
    coordinates = [start]

    # curr moves horizontally until in correct column, then moves vertically to end
    while not equal1(curr, end):

        if curr[1] == end[1]:
            # moves up or down
            if curr[0] < end[0]:
                curr = [curr[0] + 1, curr[1]]
            else:
                curr = [curr[0] - 1, curr[1]]
        else:
            if curr[1] < end[1]:
                # moves right or prepares to move right
                if matrix[curr[0], curr[1] + 1] == -1:
                    curr = [curr[0], curr[1] + 1]
                else:
                    if curr[0] < end[0]:
                        curr = [curr[0] + 1, curr[1]]
                    else:
                        curr = [curr[0] - 1, curr[1]]
            else:
                # moves left or prepares to move left
                if matrix[curr[0], curr[1] - 1] == -1:
                    curr = [curr[0], curr[1] - 1]
                else:
                    if curr[0] < end[0]:
                        curr = [curr[0] + 1, curr[1]]
                    else:
                        curr = [curr[0] - 1, curr[1]]
        coordinates.append(curr)
    return coordinates

# the gate_data function
# takes a path to an hdl file and max number of gates in column
# returns a gate matrix (numpy array), a wire matrix, and the hdl file data
# the gate matrix contains indices referring to the hdl file's "parts" array
# the wire matrix contains counts of the number of wires in each cell of gate matrix
# example
#   import gatedata as gd
#   path = r"C:\Users\prana\Desktop\hdl_direc\LogicGate2.hdl"
#   gmatrix, wmatrix, phdl = gd.gate_data(path, max_to_col)
# gmatrix's indices refer to elements in phdl["parts"]

def gate_data(path, max_to_col):
    gmatrix, phdl = gm.gate_matrix(path, max_to_col)

    num_rows = len(gmatrix)
    num_cols = len(gmatrix[0])

    # list of overall chip's outputs
    ov_out = []
    for p in phdl["outputs"]:
        ov_out.append(p["name"])

    end_dic = {}
    # stores end points on end_dic dictionary
    for p in phdl["parts"]:
        for k in p["external"]:
            if k["inout"] == "in":
                if k["name"] in end_dic:
                    end_dic[k["name"]].append(p["coord"])
                else:
                    end_dic[k["name"]] = [p["coord"]]

    # wire matrix (stores the number of wires occupying each cell)
    wm = np.zeros([num_rows, num_cols]).astype(int)

    # adds coordinates for each wire
    for p in phdl["parts"]:
        wm[p["coord"][0]][p["coord"][1]] = -1
        for k in p["external"]:
            if (k["inout"] == "out") and (k["name"] not in ov_out):
                for end in end_dic[k["name"]]:
                    new_start = sum1(p["coord"], [0, 1])
                    new_end = sum1(end, [0, -1])
                    path = short_path(new_start, new_end, gmatrix)
                    for b in path:
                        wm[b[0]][b[1]] += 1
                    path.append(end)
                    if "path" in k:
                        k["path"].append(path)
                    else:
                        k["path"] = [path]

    return gmatrix, wm, phdl
