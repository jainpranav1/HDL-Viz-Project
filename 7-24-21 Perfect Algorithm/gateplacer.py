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


def gate_placer(path, max_to_col, d, show_track, show_grid):

    gmatrix, wmatrix, phdl = gd.gate_data(path, max_to_col)
    gi.gate_info(phdl)

    num_row = len(gmatrix)
    num_col = len(gmatrix[0])

    num_h_tracks = np.zeros(num_row, dtype=int)
    num_v_tracks = np.zeros(num_col, dtype=int)

    # gets number of horizontal and vertical tracks
    for chip in phdl["parts"]:
        for wire in chip["external"]:
            if wire["inout"] == "out" and wire["overall"] == "none":
                for path in wire["path"]:

                    if len(path) == 2:
                        num_v_tracks[path[0][1]] += 1

                    if path[-2][1] == chip["coord"][1] + 1:
                        num_h_tracks[path[1][0]] += 1
                        num_v_tracks[path[1][1]] += 1

                    last_move = 'N'
                    for a in range(0, len(path) - 2):
                        if path[a][0] == path[a + 1][0]:
                            if last_move != 'H':
                                num_h_tracks[path[a][0]] += 1
                                last_move = 'H'
                        else:
                            if last_move != 'V':
                                num_v_tracks[path[a][1]] += 1
                                last_move = 'V'

                    if last_move == 'H':
                        num_v_tracks[path[-2][1]] += 1

    track_spacing = 0.4

    # gets column size for each column
    col_size = []
    for j in range(0, num_col):
        temp_cols = []
        for i in range(0, num_row):
            if gmatrix[i][j] == -1:
                temp_cols.append(track_spacing * (num_v_tracks[j] + 1))
            else:
                temp_cols.append(phdl["parts"][gmatrix[i][j]]["bbox_size"][0])
        col_size.append(max(temp_cols))

    # gets row size for each row
    row_size = []
    for i in range(0, num_row):
        temp_rows = []
        for j in range(0, num_col):
            if gmatrix[i][j] == -1:
                temp_rows.append(track_spacing * (num_h_tracks[i] + 1))
            else:
                temp_rows.append(phdl["parts"][gmatrix[i][j]]["bbox_size"][1])
        row_size.append(max(temp_rows))

    sum_max_rows = sum(row_size)
    sum_max_cols = sum(col_size)

    # gets vertical track coordinates
    vt_coor = []
    curr_x_vt = 0
    for i in range(0, num_col):
        temp = []

        for j in range(1, num_v_tracks[i] + 1):
            val = curr_x_vt + (j * col_size[i]) / (num_v_tracks[i] + 1)
            temp.append(val)

        vt_coor.append(temp)
        curr_x_vt += col_size[i]

    # gets horizontal track coordinates
    ht_coor = []
    curr_y_ht = sum_max_rows
    for i in range(0, num_row):
        temp1 = []

        for j in range(1, num_h_tracks[i] + 1):
            val1 = curr_y_ht - (j * row_size[i]) / (num_h_tracks[i] + 1)
            temp1.append(val1)

        ht_coor.append(temp1)
        curr_y_ht -= row_size[i]

    if show_track:
        for i in vt_coor:
            for j in i:
                d.add(Line([j, sum_max_rows], [j, 0], "red"))
        for i in ht_coor:
            for j in i:
                d.add(Line([0, j], [sum_max_cols, j], "green"))

    # places gates on output screen
    curr_x = 0
    for i in range(0, num_col):
        curr_y = sum_max_rows
        grid_wid = col_size[i]

        for j in range(0, num_row):
            grid_hei = row_size[j]
            curr_y -= row_size[j]
            g_ind = gmatrix[j][i]

            if g_ind != -1:
                # find position of gate
                shift = sub_list([grid_wid / 2, grid_hei / 2], div_list(phdl["parts"][g_ind]["bbox_size"], 2))
                temp_pos = add_list([curr_x, curr_y], phdl["parts"][g_ind]["rel_coor"])
                final_pos = add_list(temp_pos, shift)

                gate = phdl["parts"][g_ind]["gate"]
                gate.at(final_pos)
                d.add(gate)

            # draws grid
            if show_grid:
                d.add(elm.Ic(size=[grid_wid, grid_hei]).at([curr_x, curr_y]))

        curr_x += col_size[i]

    return gmatrix, wmatrix, phdl, vt_coor, ht_coor