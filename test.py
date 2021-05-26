import gatedata as gd
import schemdraw
import schemdraw.elements as elm
from schemdraw.segments import *
from schemdraw.logic import *
import numpy as np
import re

path = r"/home/patelaaniket/Documents/HDL-Viz-Project/LogicGate1.hdl"
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
        print(x,y)
        self.segments.append(Segment([(x, y), (x+1, y), (x+1, y+1), (x, y+1), (x, y)]))

d = schemdraw.Drawing()

test = phdl["parts"]

for i in range(len(gmatrix)):
    for j in range(len(gmatrix[i])):
        if (gmatrix[i][j] != -1):
            fullname = test[gmatrix[i][j].astype(np.int64)]["name"]
            name = re.split('\d+', fullname)[0]
            print(name)
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
            if gate != None:
                d.add(gate)


d.save('schematic.svg')