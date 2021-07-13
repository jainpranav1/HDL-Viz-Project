import gateplacer as gp
import schemdraw
import schemdraw.elements as elm
from schemdraw.segments import *

class Wire(elm.Element):
    def __init__(self, abs_path, grid_path, color):
        super().__init__()

        abs_path[2][1] = abs_path[1][1]
        abs_path[-3][1] = abs_path[-2][1]

        line = Segment(abs_path)
        line.color = color
        self.segments.append(line)




path = r"C:\Users\prana\Desktop\CSCE_312\P5Codes\P5Codes\Pranav-Jain-727009500\CPU.hdl"
#path = r"C:\Users\prana\Desktop\hdl_direc\LogicGate2.hdl"
#path = r"C:\Users\prana\Desktop\CSCE_312\P2Codes\Pranav-Jain-727009500\ALU.hdl"
#path = r"C:\Users\prana\Desktop\CSCE_312\project 1\P1Codes\Pranav-Jain-727009500\Onion.hdl"
#path = r"C:\Users\prana\Desktop\CSCE_312\project 1\P1Codes\Pranav-Jain-727009500\Mux4Way16.hdl"
#path = r"C:\Users\prana\Desktop\CSCE_312\project 1\P1Codes\Pranav-Jain-727009500\Palindrome.hdl"
#path = r"C:\Users\prana\Desktop\CSCE_312\project 1\P1Codes\Pranav-Jain-727009500\Or.hdl"
#path = r"C:\Users\prana\Desktop\CSCE_312\project 1\P1Codes\Pranav-Jain-727009500\Xnor.hdl"
#path = r"C:\Users\prana\Desktop\CSCE_312\P2Codes\Pranav-Jain-727009500\FastRCA12.hdl"
#path = r"C:\Users\prana\Desktop\CSCE_312\P2Codes\Pranav-Jain-727009500\Inc16.hdl"
#path = r"C:\Users\prana\Desktop\CSCE_312\P2Codes\Pranav-Jain-727009500\AddSub10.hdl"
#path = r"C:\Users\prana\Desktop\CSCE_312\P5Codes\P5Codes\Pranav-Jain-727009500\Memory.hdl"

n = 4
d = schemdraw.Drawing()
grid = True
dots = True

gmatrix, wmatrix, phdl, dmatrix = gp.gate_placer(path, n, d, grid, dots)

print(wmatrix)

num_row = len(gmatrix)
num_col = len(gmatrix[0])

elem_gates = ["And", "Nand", "Or", "Nor", "Xor", "Xnor", "Not"]
colors = ["red", "orange", "green", "blue", "purple"]

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

                        # runs for each output wire from pin (can be multiple)

                        # indices in parts array
                        used_end_gates = []
                        abs_paths = []
                        for l in range(0, len(chip["external"][k]["path"])):
                            abs_path = []
                            # adds starting coordinates of wires (different for custom/mux gates vs elem gates)
                            if chip["name"] in elem_gates:
                                if chip["name"] == "Not":
                                    [ox, oy] = list(pin_coord["out"])
                                    abs_path.append([ox+0.90, oy])
                                    abs_path.append([dmatrix[j][i][1], oy])
                                else:
                                    [ox, oy] = list(pin_coord["out"])
                                    abs_path.append([ox, oy])
                                    abs_path.append([dmatrix[j][i][1], oy])
                            else:
                                [ox, oy] = list(pin_coord["inR" + str(o_counter)])
                                abs_path.append([ox, oy])
                                abs_path.append([dmatrix[j][i][1], oy])

                            # adds first middle coordinate of wires
                            path_gmatrix = chip["external"][k]["path"][l]
                            [c_row, c_col] = path_gmatrix[0]
                            abs_path.append(dmatrix[c_row][c_col][0])
                            dmatrix[c_row][c_col].pop(0)

                            abs_paths.append(abs_path)

                        chip["external"][k]["abs_paths"] = abs_paths



# adds middle and end coordinates of each wire
color_counter = 0
for i in range(0, num_col):
    for j in range(0, num_row):
        ind = gmatrix[j][i]
        if ind != -1:
            chip = phdl["parts"][ind]

            for k in range(0, len(chip["internal"])):
                color_counter += 1

                if chip["external"][k]["inout"] == "out":
                    if chip["external"][k]["overall"] != "out":

                        # runs for each output wire from pin (can be multiple)

                        # indices in parts array
                        used_end_gates = []
                        for l in range(0, len(chip["external"][k]["path"])):
                            abs_path = chip["external"][k]["abs_paths"][l]

                            # adds rest of middle coordinates of wires
                            path_gmatrix = chip["external"][k]["path"][l]
                            for p_coor in path_gmatrix[1:-1]:
                                [c_row, c_col] = p_coor
                                abs_path.append(dmatrix[c_row][c_col][0])
                                dmatrix[c_row][c_col].pop(0)

                            # calculates number of input pins on ending chip
                            [er, ec] = path_gmatrix[-1]
                            end_chip = phdl["parts"][gmatrix[er][ec]]
                            end_pin_coord = end_chip["gate"].absanchors

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
                            if end_chip["name"] in elem_gates:
                                if end_chip["name"] != "Not":
                                    [ox, oy] = list(end_pin_coord["in" + str(w_ind + 1)])
                                    abs_path.append([dmatrix[er][ec][0], oy])
                                    abs_path.append([ox, oy])
                                else:
                                    [ox, oy] = list(end_pin_coord["in"])
                                    abs_path.append([dmatrix[er][ec][0], oy])
                                    abs_path.append([ox-0.90, oy])
                            else:
                                if (end_chip["name"] == "Mux" or end_chip["name"] == "DMux") \
                                        and end_chip["internal"][w_ind]["name"] == "sel":

                                    [ox, oy] = list(end_pin_coord["inT1"])
                                    abs_path.append([dmatrix[er][ec][0], oy])
                                    abs_path.append([ox, oy])
                                else:
                                    nw_ind = num_in_w - w_ind
                                    [ox, oy] = list(end_pin_coord["inL" + str(nw_ind)])
                                    abs_path.append([dmatrix[er][ec][0], oy])
                                    abs_path.append([ox, oy])

                            # adds wires
                            d.add(Wire(abs_path, chip["external"][k]["path"][l], colors[color_counter % len(colors)]).at([0, 0]))

d.draw(backend="svg")
#d.draw()