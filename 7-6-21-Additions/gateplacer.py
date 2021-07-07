import gateinfo as gi
import gatedata as gd
from schemdraw.segments import *
import schemdraw.elements as elm
import numpy as np

def add_list(list1, list2):
    return [list1[0]+list2[0], list1[1]+list2[1]]

def sub_list(list1, list2):
    return [list1[0]-list2[0], list1[1]-list2[1]]

def div_list(list1, n):
    return [list1[0]/n, list1[1]/n]

class Line(elm.Element):
    def __init__(self, start, end, color):
        super().__init__()
        line = Segment([(start[0], start[1]), (end[0], end[1])])
        line.color = color
        self.segments.append(line)

class Dot(elm.Element):
    def __init__(self, coord):
        super().__init__()
        self.segments.append(SegmentCircle(coord, 0.075, fill="black"))



def gate_placer(path, max_to_col, d, show_grid, show_dots):

    gmatrix, wmatrix, phdl = gd.gate_data(path, max_to_col)
    gi.gate_info(phdl)

    num_row = len(gmatrix)
    num_col = len(gmatrix[0])

    # get number of tracks for each column (max number of wires)
    max_wires_col = []
    for j in range(0, num_col):
        temp_wires_col = []
        for i in range(0, num_row):
            temp_wires_col.append(wmatrix[i][j])
        max_wires_col.append(max(temp_wires_col))

    # get number of tracks for each row (max number of wires)
    max_wires_row = []
    for i in range(0, num_row):
        temp_wires_row = []
        for j in range(0, num_col):
            temp_wires_row.append(wmatrix[i][j])
        max_wires_row.append(max(temp_wires_row))

    dot_spacing = 0.5

    # gets max column size for each column
    max_cols = []
    for j in range(0, num_col):
        temp_cols = []
        for i in range(0, num_row):
            if gmatrix[i][j] == -1:
                temp_cols.append(dot_spacing * (max_wires_col[j] + 1))
            else:
                temp_cols.append(phdl["parts"][gmatrix[i][j]]["bbox_size"][0])
        max_cols.append(max(temp_cols))

    # gets max row size for each row
    max_rows = []
    for i in range(0, num_row):
        temp_rows = []
        for j in range(0, num_col):
            if gmatrix[i][j] == -1:
                temp_rows.append(dot_spacing * (max_wires_row[i] + 1))
            else:
                temp_rows.append(phdl["parts"][gmatrix[i][j]]["bbox_size"][1])
        max_rows.append(max(temp_rows))

    sum_max_rows = sum(max_rows)

    # places gates on output screen
    curr_x = 0
    for i in range(0, num_col):
        curr_y = sum_max_rows
        grid_wid = max_cols[i]

        for j in range(0, num_row):
            grid_hei = max_rows[j]
            curr_y -= max_rows[j]
            g_ind = gmatrix[j][i]

            if g_ind != -1:
                # find position of gate
                shift = sub_list([grid_wid/2, grid_hei/2], div_list(phdl["parts"][g_ind]["bbox_size"], 2))
                temp_pos = add_list([curr_x, curr_y], phdl["parts"][g_ind]["rel_coor"])
                final_pos = add_list(temp_pos, shift)

                gate = phdl["parts"][g_ind]["gate"]
                gate.at(final_pos)
                d.add(gate)

            # draws grid
            if show_grid:
                d.add(elm.Ic(size=[grid_wid, grid_hei]).at([curr_x, curr_y]))

        curr_x += max_cols[i]


    # makes dot matrix (matrix that contains coordinates of dots)
    dm = np.zeros([num_row, num_col]).tolist()
    curr_x = 0
    for i in range(0, num_col):
        curr_y = sum_max_rows
        grid_wid = max_cols[i]

        for j in range(0, num_row):
            grid_hei = max_rows[j]
            curr_y -= max_rows[j]

            num_dots = wmatrix[j][i]

            if num_dots != -1:
                dots = []
                for k in reversed(range(1, num_dots + 1)):
                    dot_x = curr_x + (k * grid_wid) / (num_dots + 1)
                    dot_y = curr_y + (k * grid_hei) / (num_dots + 1)
                    dots.append([dot_x, dot_y])
                    if show_dots:
                        d.add(Dot([dot_x, dot_y]).at([0, 0]))
                dm[j][i] = dots

            else:
                dm[j][i] = [curr_x, curr_x + grid_wid]

        curr_x += max_cols[i]


    return gmatrix, wmatrix, phdl, dm