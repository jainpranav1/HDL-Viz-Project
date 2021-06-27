import gateplacer as gp
import schemdraw
import schemdraw.elements as elm
import schemdraw.segments as sgm
import numpy as np

path = r"/home/robert/tamu/spring_2021/csce-312-200/honors_project/HDL-Viz-Project/CPU.hdl" #CPU.hdl
#path = r"/home/robert/tamu/spring_2021/csce-312-200/project3/P3Codes/TrafficController.hdl" #CPU.hdl
#path = r"/home/robert/tamu/spring_2021/csce-312-200/honors_project/HDL-Viz-Project/Xor.hdl" #CPU.hdl
n = 5
d = schemdraw.Drawing()
track = True
grid = True

gmatrix, wmatrix, phdl, vt_coor, ht_coor = gp.gate_placer(path, n, d, track, grid)

def draw_path(path, wmatrix, ht_coor, vt_coor):
    draw_path = []
    x_pops = np.zeros(len(vt_coor))
    y_pops = np.zeros(len(ht_coor))

    prev_y, prev_x = path[0]
    #draw_path += [(vt_coor[prev_x][0]-9.9, ht_coor[prev_y][0]-5)]
    draw_path += [(vt_coor[prev_x][0], ht_coor[prev_y][0])]
    for y,x in path[1:-1]:

        # draw on first available track at position
        #draw_path += [(ht_coor[x][0], vt_coor[y][0])]
        #draw_path += [(vt_coor[x][0]-9.9, ht_coor[y][0]-5)]
        draw_path += [(vt_coor[x][0], ht_coor[y][0])]

        if wmatrix[y][x] > 1:
                # more than 1 wire in box
                # cannot share track
                # schedule pop

            if (prev_x == x):
                x_pops[x] = True


            if (prev_y == y):
                y_pops[y] = True
        
        prev_x = x
        prev_y = y


    # pop
    for x in np.where(x_pops)[0]:
        vt_coor[int(x)].pop(0)
    for y in np.where(y_pops)[0]:
        ht_coor[int(y)].pop(0)

    return draw_path



class Wire(elm.Element):
    def __init__(self, draw_path):
        super().__init__()
        wire = sgm.Segment(draw_path)
        wire.color = 'blue'
        self.at((0,0))
        self.segments.append(wire)

#draw_path1 = draw_path(phdl['parts'][0]['external'][1]['path'][0], wmatrix, ht_coor, vt_coor)
#d.add(Wire(draw_path1))
elem_gates = ["And", "Nand", "Or", "Nor", "Xor", "Xnor", "Not"] 
for part in phdl['parts']:
    if part['name'] not in elem_gates:
        print("CUSTOM")
        print(part['name'])
    else:
        continue
    #print(part)
    #print(gmatrix)
    for external in part['external']:
        if external['inout'] == 'out':
            #draw_path_out = draw_path(external['path'][0], wmatrix, ht_coor, vt_coor)
            #d.add(Wire(draw_path_out))
            #try:
            draw_path_out = draw_path(external['path'][0], wmatrix, ht_coor, vt_coor)

            # prepend start draw
            #print(dir(part['gate']))
            out_anc = part['gate'].absanchors['out']
            draw_path_out.insert(0, [draw_path_out[0][0], out_anc[1]])
            draw_path_out.insert(0, [out_anc[0], out_anc[1]])

            # end coords
            x, y = external['path'][0][-1]
            end_to_gate = phdl['parts'][gmatrix[x][y]]


            #ext_count = 0
            print("COMPARING EXTERNAL NAMES")
            print(external['name'])
            print(end_to_gate['external'])
            for i, ext in enumerate(end_to_gate['external']):
                if external['name'] == ext['name']:
                    # custom gate
                    if part['name'] not in elem_gates:
                        print("hi")
                        pin_name = 'inL' + str(i+1)
                        in_anc = end_to_gate['gate'].absanchors[pin_name]
                        draw_path_out[-1] = [draw_path_out[-1][0], in_anc[1]]
                        draw_path_out.append([in_anc[0], in_anc[1]])


                    # normal gate
                    else:
                        print("hi")
                        #print("NOT CUSTOM\n"*20)
                        pin_name = 'in' + str(i+1)
                        in_anc = end_to_gate['gate'].absanchors[pin_name]
                        draw_path_out[-1] = [draw_path_out[-1][0], in_anc[1]]
                        draw_path_out.append([in_anc[0], in_anc[1]])
                #ext_count += 1
            #print(phdl['parts'][external['path'][0][-1]])


            external['abspath'] = draw_path_out # NEED TO APPEND BECAUSE COULD HAVE 2 OUT PATHS
            d.add(Wire(draw_path_out))
            #except Exception as e:
                #print("ERROR", e)


print(wmatrix)

print()
print("CHECKING ABSANCHORS")
print("AREGISTER")
print(phdl['parts'][3])
print()
print("AREG ANCHORS")
print(phdl['parts'][3]['gate'].absanchors)
print()
print("NOTGATE")
print(phdl['parts'][1]['gate'].absanchors)
for i, part in enumerate(phdl['parts']):
    continue
    #print(i, part['name'])

d.draw(backend='svg')
