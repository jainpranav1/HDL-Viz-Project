# README
# to use:
# import hdl_image_maker as him
#
# Function chip_placer
# him.image_maker(path_of_file):
# "path_of_file" is path of hdl file
# returns nothing
# the image_maker function outputs svg with hdl file visualization
#
# example:
#    path = r"C:\Users\prana\Desktop\csce_312_files\CPU.hdl"
#    him.image_maker(path)

import schemdraw
import chip_placer as cp
import extra_functions as ef


def image_maker(path_of_file):
    d = schemdraw.Drawing()
    track = False
    grid = False

    gmatrix, lmatrix, phdl, vt_coor, ht_coor = cp.chip_placer(path_of_file, d, track, grid)

    num_row = len(gmatrix)
    num_col = len(gmatrix[0])

    elem_gates = ["And", "Nand", "Or", "Nor", "Xor", "Xnor", "Not"]

    # adds starting coordinates of each wire
    for i in range(0, num_col):
        for j in range(0, num_row):
            ind = gmatrix[j][i]
            if ind != -1:
                chip = phdl["parts"][ind]
                pin_coord = chip["gate"].absanchors

                # calculates number of output pins on starting chip
                num_out_w = 0
                for k in range(0, len(chip["internal"])):
                    if chip["external"][k]["inout"] == "out":
                        num_out_w += 1

                o_counter = num_out_w + 1
                for k in range(0, len(chip["internal"])):
                    if chip["external"][k]["inout"] == "out":

                        o_counter -= 1
                        if not chip["external"][k]["overall"]:

                            abs_paths = []
                            for l in range(0, len(chip["external"][k]["path"])):

                                abs_path = []
                                # adds starting coordinates of wires (different for custom/mux gates vs elem gates)

                                # delays adding of special wires
                                # special wires - short wires, horizontal wires, ending gates in adjacent column
                                spec_case = False
                                path_g = chip["external"][k]["path"][l]

                                if len(path_g) == 2:
                                    spec_case = True
                                elif path_g[0][0] == path_g[1][0]:
                                    spec_case = True
                                elif path_g[-2][1] == i + 1:
                                    if gmatrix[j][i + 2] == -1:
                                        spec_case = True

                                if spec_case:
                                    if chip["name"] in elem_gates:
                                        [ox, oy] = list(pin_coord["out"])
                                        if chip["name"] == "Not":
                                            abs_path.append([ox + 0.90, oy])
                                        else:
                                            abs_path.append([ox, oy])
                                    else:
                                        [ox, oy] = list(pin_coord["inR" + str(o_counter)])
                                        abs_path.append([ox, oy])
                                else:
                                    if chip["name"] in elem_gates and not chip["custom_pins"]:
                                        [ox, oy] = list(pin_coord["out"])
                                        if chip["name"] == "Not":
                                            abs_path.append([ox + 0.90, oy])
                                        else:
                                            abs_path.append([ox, oy])
                                    else:
                                        [ox, oy] = list(pin_coord["inR" + str(o_counter)])
                                        abs_path.append([ox, oy])
                                    abs_path.append([vt_coor[i + 1][0], oy])
                                    vt_coor[i + 1].pop(0)

                                abs_paths.append(abs_path)

                            chip["external"][k]["abs_paths"] = abs_paths

    # adds special wires to start_v_tracks
    for i in range(0, num_col):
        for j in range(0, num_row):
            ind = gmatrix[j][i]
            if ind != -1:
                chip = phdl["parts"][ind]

                # calculates number of output pins on starting chip
                num_out_w = 0
                for k in range(0, len(chip["internal"])):
                    if chip["external"][k]["inout"] == "out":
                        num_out_w += 1

                o_counter = num_out_w + 1
                for k in range(0, len(chip["internal"])):
                    if chip["external"][k]["inout"] == "out":

                        o_counter -= 1
                        if not chip["external"][k]["overall"]:

                            for l in range(0, len(chip["external"][k]["path"])):

                                add_tracks = False
                                path_g = chip["external"][k]["path"][l]

                                if len(path_g) == 2:
                                    add_tracks = True
                                elif path_g[0][0] == path_g[1][0]:
                                    add_tracks = True
                                elif path_g[-2][1] == i + 1:
                                    if gmatrix[j][i + 2] == -1:
                                        if lmatrix[j][i + 2] != 0:
                                            add_tracks = True

                                if add_tracks:
                                    if "start_v_tracks" not in chip:
                                        chip["start_v_tracks"] = []

                                    chip["start_v_tracks"].append(vt_coor[i + 1][0])
                                    vt_coor[i + 1].pop(0)

    # adds middle coordinates of each wire
    for i in range(0, num_col):
        for j in range(0, num_row):
            ind = gmatrix[j][i]
            if ind != -1:
                chip = phdl["parts"][ind]

                for k in range(0, len(chip["internal"])):

                    if chip["external"][k]["inout"] == "out":
                        if not chip["external"][k]["overall"]:

                            for l in range(0, len(chip["external"][k]["path"])):
                                abs_path = chip["external"][k]["abs_paths"][l]

                                # adds middle coordinates of wires
                                path_g = chip["external"][k]["path"][l]
                                curr = abs_path[-1]

                                if len(path_g) != 2:

                                    # adds wires to initial horizontal track if necessary
                                    if path_g[0][0] == path_g[1][0]:
                                        if curr[1] <= ht_coor[path_g[0][0]][0]:
                                            curr = [chip["start_v_tracks"][0], curr[1]]
                                            abs_path.append(curr)
                                            chip["start_v_tracks"].pop(0)
                                        else:
                                            curr = [chip["start_v_tracks"][-1], curr[1]]
                                            abs_path.append(curr)
                                            chip["start_v_tracks"].pop(-1)
                                        curr = [curr[0], ht_coor[path_g[0][0]][0]]
                                        abs_path.append(curr)
                                        ht_coor[path_g[0][0]].pop(0)

                                    if path_g[-2][1] == i + 1:
                                        if gmatrix[j][i + 2] == -1:
                                            if lmatrix[j][i + 2] != 0:
                                                if curr[1] <= ht_coor[path_g[0][0]][0]:
                                                    curr = [chip["start_v_tracks"][0], curr[1]]
                                                    abs_path.append(curr)
                                                    chip["start_v_tracks"].pop(0)
                                                else:
                                                    curr = [chip["start_v_tracks"][-1], curr[1]]
                                                    abs_path.append(curr)
                                                    chip["start_v_tracks"].pop(-1)
                                                curr = [curr[0], ht_coor[path_g[0][0]][0]]
                                                abs_path.append(curr)
                                                ht_coor[path_g[0][0]].pop(0)
                                            curr = [vt_coor[path_g[0][1]][-1], curr[1]]
                                            abs_path.append(curr)
                                            vt_coor[path_g[0][1]].pop(-1)
                                        else:
                                            curr = [curr[0], ht_coor[path_g[1][0]][0]]
                                            abs_path.append(curr)
                                            ht_coor[path_g[1][0]].pop(0)
                                            curr = [vt_coor[path_g[1][1]][-1], curr[1]]
                                            abs_path.append(curr)
                                            vt_coor[path_g[1][1]].pop(-1)

                                    else:
                                        trigger = False
                                        for g in range(0, len(path_g) - 3):
                                            if (path_g[g][0] == path_g[g + 1][0]) and (
                                                    path_g[g + 1][1] == path_g[g + 2][1]):
                                                if path_g[-2][0] == path_g[-1][0] and path_g[-1][1] == path_g[g + 1][
                                                    1] + 1:
                                                    if path_g[g][1] < path_g[g + 1][1] and gmatrix[path_g[g + 1][0]][
                                                        path_g[g + 1][1] + 1] != -1:
                                                        [cx, cy] = path_g[g + 1]
                                                        curr = [vt_coor[cy][0], curr[1]]
                                                        vt_coor[cy].pop(0)
                                                        abs_path.append(curr)
                                                        trigger = True

                                                    else:
                                                        [cx, cy] = path_g[g + 1]
                                                        curr = [vt_coor[cy][-1], curr[1]]
                                                        vt_coor[cy].pop(-1)
                                                        abs_path.append(curr)

                                                else:
                                                    [cx, cy] = path_g[g + 1]
                                                    curr = [vt_coor[cy][0], curr[1]]
                                                    vt_coor[cy].pop(0)
                                                    abs_path.append(curr)

                                            elif (path_g[g][1] == path_g[g + 1][1]) and (
                                                    path_g[g + 1][0] == path_g[g + 2][0]):
                                                [cx, cy] = path_g[g + 1]
                                                curr = [curr[0], ht_coor[cx][0]]
                                                ht_coor[cx].pop(0)
                                                abs_path.append(curr)

                                            elif trigger:
                                                [cx, cy] = path_g[g + 1]
                                                curr = [curr[0], ht_coor[cx][0]]
                                                ht_coor[cx].pop(0)
                                                abs_path.append(curr)

                                                curr = [vt_coor[cy][-1], curr[1]]
                                                vt_coor[cy].pop(-1)
                                                abs_path.append(curr)

                                                trigger = False

    # adds end coordinates of each wire
    colors = ["red", "orange", "green", "blue", "purple"]

    color_counter = 0
    for i in range(0, num_col):
        for j in range(0, num_row):
            ind = gmatrix[j][i]
            if ind != -1:
                chip = phdl["parts"][ind]

                for k in range(0, len(chip["internal"])):

                    if chip["external"][k]["inout"] == "out":
                        if not chip["external"][k]["overall"]:
                            color_counter += 1

                            # runs for each output wire from pin (can be multiple)

                            # indices in parts array
                            used_end_gates = []
                            for l in range(0, len(chip["external"][k]["path"])):
                                abs_path = chip["external"][k]["abs_paths"][l]

                                # calculates number of input pins on ending chip
                                path_g = chip["external"][k]["path"][l]
                                [er, ec] = path_g[-1]
                                end_chip = phdl["parts"][gmatrix[er][ec]]
                                end_pin_coord = end_chip["gate"].absanchors

                                # counts number of input wires on left side of chip (excluding select pin)
                                num_in_w = 0
                                for wire in end_chip["external"]:
                                    if wire["inout"] == "in" and wire["wire_direc"] == "left":
                                        num_in_w += 1

                                # searches for wire index in end chip
                                wire_name = chip["external"][k]["name"]
                                w_ind = -1
                                a_counter = used_end_gates.count(gmatrix[er][ec])
                                for n in range(0, len(end_chip["internal"])):
                                    if end_chip["external"][n]["name"] == wire_name:
                                        used_end_gates.append(gmatrix[er][ec])
                                        if a_counter == 0:
                                            w_ind = n
                                            break
                                        else:
                                            a_counter -= 1

                                # adds ending coordinates of wires (different for custom/mux gates vs elem gates)
                                last_coord = abs_path[-1]
                                if end_chip["name"] in elem_gates and not end_chip["custom_pins"]:
                                    if end_chip["name"] != "Not":
                                        [ox, oy] = list(end_pin_coord["in" + str(w_ind + 1)])

                                        # for special cases
                                        if len(path_g) == 2:
                                            abs_path.append([chip["start_v_tracks"][0], last_coord[1]])
                                            chip["start_v_tracks"].pop(0)
                                            last_coord = abs_path[-1]
                                        elif path_g[-3][0] == path_g[-2][0] and path_g[-2][0] == path_g[-1][0]:
                                            abs_path.append([vt_coor[path_g[-2][1]][0], last_coord[1]])
                                            vt_coor[path_g[-2][1]].pop(0)
                                            last_coord = abs_path[-1]

                                        abs_path.append([last_coord[0], oy])
                                        abs_path.append([ox, oy])
                                    else:
                                        [ox, oy] = list(end_pin_coord["in"])

                                        # for special cases
                                        if len(path_g) == 2:
                                            if last_coord[1] <= oy:
                                                abs_path.append([chip["start_v_tracks"][0], last_coord[1]])
                                                chip["start_v_tracks"].pop(0)
                                            else:
                                                abs_path.append([chip["start_v_tracks"][-1], last_coord[1]])
                                                chip["start_v_tracks"].pop(-1)
                                            last_coord = abs_path[-1]
                                        elif path_g[-3][0] == path_g[-2][0] and path_g[-2][0] == path_g[-1][0]:
                                            if last_coord[1] <= oy:
                                                abs_path.append([vt_coor[path_g[-2][1]][0], last_coord[1]])
                                                vt_coor[path_g[-2][1]].pop(0)
                                            else:
                                                abs_path.append([vt_coor[path_g[-2][1]][-1], last_coord[1]])
                                                vt_coor[path_g[-2][1]].pop(-1)
                                            last_coord = abs_path[-1]

                                        abs_path.append([last_coord[0], oy])
                                        abs_path.append([ox - 0.90, oy])

                                else:
                                    if end_chip["external"][w_ind]["wire_direc"] == "top":

                                        [ox, oy] = list(end_pin_coord["inT1"])
                                        abs_path.append([ox, last_coord[1]])
                                        abs_path.append([ox, oy])
                                    else:
                                        nw_ind = num_in_w - w_ind
                                        [ox, oy] = list(end_pin_coord["inL" + str(nw_ind)])

                                        # for special cases
                                        if len(path_g) == 2:
                                            if last_coord[1] <= oy:
                                                abs_path.append([chip["start_v_tracks"][0], last_coord[1]])
                                                chip["start_v_tracks"].pop(0)
                                            else:
                                                abs_path.append([chip["start_v_tracks"][-1], last_coord[1]])
                                                chip["start_v_tracks"].pop(-1)
                                            last_coord = abs_path[-1]
                                        elif path_g[-3][0] == path_g[-2][0] and path_g[-2][0] == path_g[-1][0]:
                                            if last_coord[1] <= oy:
                                                abs_path.append([vt_coor[path_g[-2][1]][0], last_coord[1]])
                                                vt_coor[path_g[-2][1]].pop(0)
                                            else:
                                                abs_path.append([vt_coor[path_g[-2][1]][-1], last_coord[1]])
                                                vt_coor[path_g[-2][1]].pop(-1)
                                            last_coord = abs_path[-1]

                                        abs_path.append([last_coord[0], oy])
                                        abs_path.append([ox, oy])

                                # adds wires
                                d.add(ef.Wire(abs_path, colors[color_counter % len(colors)]).at([0, 0]))

    d.draw(backend='svg', show=True)