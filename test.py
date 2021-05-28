import gatedata as gd
import schemdraw
import schemdraw.elements as elm
from schemdraw.segments import *
from schemdraw.logic import *
import numpy as np
import re

path = r"/home/patelaaniket/Documents/HDL-Viz-Project/LogicGate2.hdl"
n = 2

gmatrix, wmatrix, phdl = gd.gate_data(path, n)
print(gmatrix)
# print(wmatrix)
# print(phdl)

class Mux(elm.Element):
    def __init__(self, coor):
        super().__init__()
        x = coor[0]
        y = coor[1]
        self.segments.append(Segment([(x, y+0.5), (x+0.5, y), (x+0.5, y+1.5), (x, y+1), (x, y+0.5)]))

class Dmux(elm.Element):
    def __init__(self, coor):
        super().__init__()
        x = coor[0]
        y = coor[1]
        self.segments.append(Segment([(x, y), (x+0.5, y+0.5), (x+0.5, y+1), (x, y+1.5), (x, y)]))

class Box(elm.Element):
    def __init__(self, coor):
        super().__init__()
        x = coor[0]
        y = coor[1]
        self.segments.append(Segment([(x, y), (x+1, y), (x+1, y+1), (x, y+1), (x, y)]))
        self.segments.append(Segment([(x-0.3, y+0.7), (x, y+0.7)]))
        self.segments.append(Segment([(x-0.3, y+0.3), (x, y+0.3)]))
        self.segments.append(Segment([(x+1, y+0.5), (x+1.3, y+0.5)]))

d = schemdraw.Drawing()

test = phdl["parts"]

for i in range(len(gmatrix)):
    for j in range(len(gmatrix[i])):
        if (gmatrix[i][j] != -1):
            test[gmatrix[i][j].astype(np.int64)]["coord"] = [[(j*2 - 0.3, i*3 + 0.7), (j*2 - 0.3, i*3 + 0.3)], [(j*2 + 1.3, i*3 + 0.5)]]
            fullname = test[gmatrix[i][j].astype(np.int64)]["name"]
            name = re.split('\d+', fullname)[0]
            gate = Box([0, 0]).label(fullname).at((j*2, i*3 - 0.5))
            if name == "Mux":
                gate = Mux([j*2, i*3]).label(fullname)
            elif name == "Dmux":
                gate = Dmux([j*2, i*3]).label(fullname)
            elif name == "Or":
                gate = logic.Or().at((j*2, i*3))
            elif name == "Nor":
                gate = logic.Nor().at((j*2, i*3))
            elif name == "And":
                gate = logic.And().at((j*2, i*3))
            elif name == "Nand":
                gate = logic.Nand().at((j*2, i*3))
            elif name == "Xor":
                gate = logic.Xor().at((j*2, i*3))
            elif name == "Xnor":
                gate = logic.Xnor().at((j*2, i*3))
            elif name == "Not":
                gate = logic.Not().at((j*2, i*3))
            else:
                test[gmatrix[i][j].astype(np.int64)]["coord"] = [[(j*2 - 0.3, i*3 + 0.2), (j*2 - 0.3, i*3 - 0.2)], [(j*2 + 1.3, i*3)]]
            if gate != None:
                d.add(gate)

d.save('schematic.svg')