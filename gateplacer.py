import gateinfo as gi
import gatedata as gd
from schemdraw.segments import *
import schemdraw.elements as elm

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

    track_spacing = 0.5

    # gets max column size for each column
    max_cols = []
    for j in range(0, num_col):
        temp_cols = []
        for i in range(0, num_row):
            if gmatrix[i][j] == -1:
                temp_cols.append(track_spacing * (max_wires_col[j] + 1))
            else:
                temp_cols.append(phdl["parts"][int(gmatrix[i][j])]["bbox_size"][0])
        max_cols.append(max(temp_cols))

    # gets max row size for each row
    max_rows = []
    for i in range(0, num_row):
        temp_rows = []
        for j in range(0, num_col):
            if gmatrix[i][j] == -1:
                temp_rows.append(track_spacing * (max_wires_row[i] + 1))
            else:
                temp_rows.append(phdl["parts"][int(gmatrix[i][j])]["bbox_size"][1])
        max_rows.append(max(temp_rows))

    sum_max_rows = sum(max_rows)
    sum_max_cols = sum(max_cols)

    # gets vertical track coordinates
    vt_coor = []
    curr_x_vt = 0
    for i in range(0, num_col):
        temp = []

        for j in range(1, max_wires_col[i] + 1):
            val = curr_x_vt + (j * max_cols[i]) / (max_wires_col[i] + 1)
            temp.append(val)

        vt_coor.append(temp)
        curr_x_vt += max_cols[i]

    # gets horizontal track coordinates
    ht_coor = []
    curr_y_ht = sum_max_rows
    for i in range(0, num_row):
        temp1 = []

        for j in range(1, max_wires_row[i] + 1):
            val1 = curr_y_ht - (j * max_rows[i]) / (max_wires_row[i] + 1)
            temp1.append(val1)

        ht_coor.append(temp1)
        curr_y_ht -= max_rows[i]

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
        grid_wid = max_cols[i]

        for j in range(0, num_row):
            grid_hei = max_rows[j]
            curr_y -= max_rows[j]
            g_ind = int(gmatrix[j][i])

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

    return gmatrix, wmatrix, phdl, vt_coor, ht_coor
