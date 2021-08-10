import gateplacer as gp
import schemdraw
import schemdraw.elements as elm
from schemdraw.segments import *


class Wire(elm.Element):
    def __init__(self, path, color):
        super().__init__()

        line = Segment(path)
        line.color = color
        self.segments.append(line)


def image_maker(path):
    n = 4
    d = schemdraw.Drawing()
    track = False
    grid = False

    gmatrix, wmatrix, phdl, vt_coor, ht_coor = gp.gate_placer(path, n, d, track, grid)

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
                        if chip["external"][k]["overall"] != "out":

                            abs_paths = []
                            for l in range(0, len(chip["external"][k]["path"])):

                                abs_path = []
                                # adds starting coordinates of wires (different for custom/mux gates vs elem gates)

                                # delays adding of short wires
                                if len(chip["external"][k]["path"][l]) == 2:
                                    if chip["name"] in elem_gates:
                                        [ox, oy] = list(pin_coord["out"])
                                        if chip["name"] == "Not":
                                            abs_path.append([ox + 0.90, oy])
                                        else:
                                            abs_path.append([ox, oy])
                                    else:
                                        [ox, oy] = list(pin_coord["inR" + str(o_counter)])
                                        abs_path.append([ox, oy])

                                    if "saved_v_tracks" not in chip:
                                        chip["saved_v_tracks"] = []

                                    chip["saved_v_tracks"].append(vt_coor[i + 1][0])
                                    vt_coor[i + 1].pop(0)

                                else:
                                    if chip["name"] in elem_gates:
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

    # adds middle coordinates of each wire
    for i in range(0, num_col):
        for j in range(0, num_row):
            ind = gmatrix[j][i]
            if ind != -1:
                chip = phdl["parts"][ind]

                for k in range(0, len(chip["internal"])):

                    if chip["external"][k]["inout"] == "out":
                        if chip["external"][k]["overall"] != "out":

                            for l in range(0, len(chip["external"][k]["path"])):
                                abs_path = chip["external"][k]["abs_paths"][l]

                                # adds middle coordinates of wires
                                path_g = chip["external"][k]["path"][l]
                                curr = abs_path[-1]

                                # adds rest of middle coordinates

                                if (path_g[-2][1] == i + 1) and (len(path_g) != 2):
                                    [px, py] = path_g[1]
                                    curr = abs_path[-1]
                                    curr = [curr[0], ht_coor[px][0]]
                                    abs_path.append(curr)
                                    ht_coor[px].pop(0)

                                    curr = [vt_coor[py][0], curr[1]]
                                    abs_path.append(curr)
                                    vt_coor[py].pop(0)
                                else:
                                    for g in range(0, len(path_g) - 3):
                                        if (path_g[g][0] == path_g[g + 1][0]) and (
                                                path_g[g + 1][1] == path_g[g + 2][1]):
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

    # adds end coordinates of each wire
    colors = ["red", "orange", "green", "blue", "purple"]
    # colors = ["black"]

    color_counter = 0
    for i in range(0, num_col):
        for j in range(0, num_row):
            ind = gmatrix[j][i]
            if ind != -1:
                chip = phdl["parts"][ind]

                for k in range(0, len(chip["internal"])):

                    if chip["external"][k]["inout"] == "out":
                        if chip["external"][k]["overall"] != "out":
                            color_counter += 1

                            # runs for each output wire from pin (can be multiple)

                            # indices in parts array
                            used_end_gates = []
                            for l in range(0, len(chip["external"][k]["path"])):
                                abs_path = chip["external"][k]["abs_paths"][l]

                                # calculates number of input pins on ending chip
                                path_gmatrix = chip["external"][k]["path"][l]
                                [er, ec] = path_gmatrix[-1]
                                end_chip = phdl["parts"][gmatrix[er][ec]]
                                end_pin_coord = end_chip["gate"].absanchors

                                # counts number of input wires on left side of chip (excluding select pin)
                                num_in_w = 0
                                for m in range(0, len(end_chip["internal"])):
                                    if end_chip["external"][m]["inout"] == "in" \
                                            and not ((end_chip["name"] == "Mux" or end_chip["name"] == "DMux")
                                                     and end_chip["internal"][m]["name"] == "sel"):
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
                                if end_chip["name"] in elem_gates:
                                    if end_chip["name"] != "Not":
                                        [ox, oy] = list(end_pin_coord["in" + str(w_ind + 1)])

                                        if len(abs_path) == 1:
                                            abs_path.append([chip["saved_v_tracks"][0], last_coord[1]])
                                            chip["saved_v_tracks"].pop(0)
                                            last_coord = abs_path[-1]

                                        abs_path.append([last_coord[0], oy])
                                        abs_path.append([ox, oy])
                                    else:
                                        [ox, oy] = list(end_pin_coord["in"])

                                        if len(abs_path) == 1:
                                            if last_coord[1] <= oy:
                                                abs_path.append([chip["saved_v_tracks"][0], last_coord[1]])
                                                chip["saved_v_tracks"].pop(0)
                                            else:
                                                abs_path.append([chip["saved_v_tracks"][-1], last_coord[1]])
                                                chip["saved_v_tracks"].pop(-1)
                                            last_coord = abs_path[-1]

                                        abs_path.append([last_coord[0], oy])
                                        abs_path.append([ox - 0.90, oy])
                                else:
                                    if (end_chip["name"] == "Mux" or end_chip["name"] == "DMux") \
                                            and end_chip["internal"][w_ind]["name"] == "sel":

                                        [ox, oy] = list(end_pin_coord["inT1"])
                                        abs_path.append([ox, last_coord[1]])
                                        abs_path.append([ox, oy])
                                    else:
                                        nw_ind = num_in_w - w_ind
                                        [ox, oy] = list(end_pin_coord["inL" + str(nw_ind)])

                                        if len(abs_path) == 1:
                                            if last_coord[1] <= oy:
                                                abs_path.append([chip["saved_v_tracks"][0], last_coord[1]])
                                                chip["saved_v_tracks"].pop(0)
                                            else:
                                                abs_path.append([chip["saved_v_tracks"][-1], last_coord[1]])
                                                chip["saved_v_tracks"].pop(-1)
                                            last_coord = abs_path[-1]

                                        abs_path.append([last_coord[0], oy])
                                        abs_path.append([ox, oy])

                                # adds wires
                                d.add(Wire(abs_path, colors[color_counter % len(colors)]).at([0, 0]))

    d.draw(backend='svg', show=True)
    #d.save("temp.png")
