# README
# to use:
# import chip_placer as cp
#
# Function chip_placer
# cp.chip_placer(path_of_file, d, show_track, show_grid):
# "path_of_file" is path of hdl file
# "d" is schemdraw drawing
# "show_track" specifies if wire tracks should be shown or not
# "show_grid" specifies if grid should be shown or not
# returns gmatrix, lmatrix, phdl, vt_coor, and ht_coor
# lmatrix is a matrix of number of wires entering/exiting from left of each cell
# vt_coor and ht_coor are coordinates of horizontal and vertical tracks
# the chip_placer function places chips and tracks onto schemdraw drawing
#
# example:
#    gmatrix, lmatrix, phdl, vt_coor, ht_coor = cp.chip_placer(path, d, False, False)

import path_finder as pf
import chip_designer as cd
import schemdraw.elements as elm
import extra_functions as ef


def chip_placer(path_of_file, d, show_track, show_grid):
    gmatrix, phdl = pf.path_finder(path_of_file)
    cd.chip_designer(gmatrix, phdl)

    num_row = len(gmatrix)
    num_col = len(gmatrix[0])

    # lmatrix is a matrix of number of wires entering/exiting from left of each cell
    lmatrix = ef.matrix_maker(num_row, num_col, 0)
    for chip in phdl["parts"]:
        for wire in chip["external"]:
            if (wire["inout"] == "out") and not wire["overall"]:
                for path_g in wire["path"]:
                    for i in range(0, len(path_g) - 1):
                        if path_g[i][0] == path_g[i+1][0] and path_g[i][1] < path_g[i+1][1]:
                            lmatrix[path_g[i+1][0]][path_g[i+1][1]] += 1
                        elif path_g[i][0] == path_g[i+1][0] and path_g[i][1] > path_g[i+1][1]:
                            lmatrix[path_g[i][0]][path_g[i][1]] += 1

    num_h_tracks = ef.vector_maker(num_row, 0)
    num_v_tracks = ef.vector_maker(num_col, 0)

    # gets number of horizontal and vertical tracks
    for chip in phdl["parts"]:
        [cx, cy] = chip["coord"]

        for wire in chip["external"]:
            if wire["inout"] == "out" and not wire["overall"]:
                for path in wire["path"]:

                    if len(path) == 2:
                        num_v_tracks[path[0][1]] += 1
                    else:
                        if path[0][0] == path[1][0]:
                            num_v_tracks[path[0][1]] += 1

                        if path[-3][0] == path[-2][0] and path[-2][0] == path[-1][0]:
                            num_v_tracks[path[-2][1]] += 1

                        if path[-2][1] == cy + 1:
                            if gmatrix[cx][cy + 2] == -1:
                                if lmatrix[cx][cy + 2] != 0:
                                    num_h_tracks[path[0][0]] += 1
                                    num_v_tracks[path[0][1]] += 1
                            else:
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
                                    if path[-2][0] == path[-1][0]:
                                        if path[-1][1] == path[a][1] + 1:
                                            if gmatrix[path[a][0]][path[a][1] + 1] != -1:
                                                num_v_tracks[path[a][1]] += 1
                                                num_h_tracks[path[a + 1][0]] += 1

                                    num_v_tracks[path[a][1]] += 1
                                    last_move = 'V'

    track_spacing = 0.4

    # gets column size for each column
    col_size = []
    for j in range(0, num_col):
        temp_cols = []
        for i in range(0, num_row):
            if gmatrix[i][j] == -1:
                if num_v_tracks[j] == 0:
                    temp_cols.append(2 * track_spacing)
                else:
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
                if num_h_tracks[i] == 0:
                    temp_rows.append(2 * track_spacing)
                else:
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
                d.add(ef.Wire([[j, sum_max_rows], [j, 0]], "red"))
        for i in ht_coor:
            for j in i:
                d.add(ef.Wire([[0, j], [sum_max_cols, j]], "green"))

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
                shift = ef.sub_list([grid_wid / 2, grid_hei / 2], ef.div_list(phdl["parts"][g_ind]["bbox_size"], 2))
                temp_pos = ef.sum_lists([[curr_x, curr_y], phdl["parts"][g_ind]["rel_coor"]])
                final_pos = ef.sum_lists([temp_pos, shift])

                gate = phdl["parts"][g_ind]["gate"]
                gate.at(final_pos)
                d.add(gate)

            # draws grid
            if show_grid:
                d.add(elm.Ic(size=[grid_wid, grid_hei]).at([curr_x, curr_y]))

        curr_x += col_size[i]

    return gmatrix, lmatrix, phdl, vt_coor, ht_coor
