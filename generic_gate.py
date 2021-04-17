import schemdraw
import schemdraw.elements as elm
from schemdraw.segments import *
from schemdraw import logic
import math
import numpy
import random


class Connection(elm.Element):
    def __init__(self, start, end):
        super().__init__()

        # draws line from start location to end location (without diagonals)
        #self.segments.append(Segment([(start[0], start[1]), (end[0], start[1]), (end[0], end[1])]))
        #self.segments.append(Segment([(start[0], start[1]), (end[0], end[1])]))

        # generates curved connection (using sigmoid function)
        array = []
        flatten = 15
        for i in numpy.arange(start[0], end[0], 0.001):
            array.append((i, start[1] + (end[1] - start[1])/(1 + math.exp(-flatten * (i - (start[0] + end[0])/2)))))

        self.segments.append(Segment(array))



class GenericGate(elm.Element):
    def __init__(self, input_wires, output_wires, coor):
        super().__init__()

        input_wires.reverse()
        output_wires.reverse()

        # sets coordinates of gate
        xcoor = coor[0]
        ycoor = coor[1]

        # sets size of dots
        dot_size = 0.05

        # determines number of input and output wires
        num_inputs = len(input_wires)
        num_outputs = len(output_wires)

        # sets length of input/output wires (io_width) and gap size of input/output wires (io_height)
        io_width = 0.35
        io_height = 0.4

        # sets height of box
        if num_inputs >= num_outputs:
            height = 0.1 + (num_inputs * io_height)
        else:
            height = 0.1 + (num_inputs * io_height)

        # sets width of box
        width = 2 * height
        half_height = height/2

        # attribute - dictionary of start coordinates of input wires
        self.iw = {}

        # attribute - dictionary of end coordinates of output wires
        self.ow = {}


        # draws box
        self.segments.append(Segment([(io_width + xcoor, ycoor), (io_width + xcoor, half_height + ycoor),
                                      (io_width + xcoor + width, half_height + ycoor),
                                      (io_width + width + xcoor, -half_height + ycoor),
                                      (io_width + xcoor, -half_height + ycoor), (io_width + xcoor, ycoor)]))


        # draws input wires
        shift_down_odd_in = io_height * (num_inputs // 2)
        shift_down_even_in = shift_down_odd_in - (io_height / 2)
        if num_inputs % 2 == 1:
            for i in range(0, num_inputs):
                self.segments.append(Segment([(xcoor, i * io_height - shift_down_odd_in + ycoor),
                                              (io_width + xcoor, i * io_height - shift_down_odd_in + ycoor)]))
                self.iw[input_wires[i]] = [xcoor, i * io_height - shift_down_odd_in + ycoor]
                self.segments.append(SegmentCircle((xcoor, i * io_height - shift_down_odd_in + ycoor),
                                                   dot_size, fill='black'))

                # adds labels to wires
                self.segments.append(SegmentText([xcoor + io_width + 0.18, i * io_height - shift_down_odd_in + ycoor - 0.025], input_wires[i], fontsize=12))
        else:
            for i in range(0, num_inputs):
                self.segments.append(Segment([(xcoor, i * io_height - shift_down_even_in + ycoor),
                                              (io_width + xcoor, i * io_height - shift_down_even_in + ycoor)]))
                self.iw[input_wires[i]] = [xcoor, i * io_height - shift_down_even_in + ycoor]
                self.segments.append(SegmentCircle((xcoor, i * io_height - shift_down_even_in + ycoor),
                                                   dot_size, fill='black'))

                # adds labels to wires
                self.segments.append(SegmentText([xcoor + io_width + 0.18, i * io_height - shift_down_even_in + ycoor - 0.025], input_wires[i], fontsize=12))


        # draws output wires
        shift_down_odd_out = io_height * (num_outputs // 2)
        shift_down_even_out = shift_down_odd_out - (io_height / 2)
        if num_outputs % 2 == 1:
            for i in range(0, num_outputs):
                self.segments.append(Segment([(io_width + width + xcoor,
                                               i * io_height - shift_down_odd_out + ycoor),
                                              (2 * io_width + width + xcoor,
                                               i * io_height - shift_down_odd_out + ycoor)]))
                self.ow[output_wires[i]] = [2 * io_width + width + xcoor,  i * io_height - shift_down_odd_out + ycoor]
                self.segments.append(SegmentCircle((2 * io_width + width + xcoor,
                                                    i * io_height - shift_down_odd_out + ycoor), dot_size, fill='black'))

                # adds labels to wires
                self.segments.append(SegmentText([io_width + width + xcoor - 0.1,
                                                  i * io_height - shift_down_odd_out + ycoor - 0.025],
                                                 output_wires[i], fontsize=12, align=('right', 'center')))

        else:
            for i in range(0, num_outputs):
                self.segments.append(Segment([(io_width + width + xcoor,
                                               i * io_height - shift_down_even_out + ycoor),
                                              (2 * io_width + width + xcoor,
                                               i * io_height - shift_down_even_out + ycoor)]))
                self.ow[output_wires[i]] = [2 * io_width + width + xcoor,  i * io_height - shift_down_even_out + ycoor]
                self.segments.append(SegmentCircle((2 * io_width + width + xcoor,
                                                    i * io_height - shift_down_even_out + ycoor), dot_size, fill='black'))

                # adds labels to wires
                self.segments.append(SegmentText([io_width + width + xcoor - 0.1,
                                                  i * io_height - shift_down_even_out + ycoor - 0.025],
                                                 output_wires[i], fontsize=12, align=('right', 'center')))


        # draws vertical line to connect inputs
        if num_inputs % 2 == 1:
            self.segments.append(Segment([(io_width + xcoor, -shift_down_odd_in + ycoor),
                                          (io_width + xcoor, shift_down_odd_in + ycoor)]))
        else:
            self.segments.append(Segment([(io_width + xcoor, -shift_down_even_in + ycoor),
                                          (io_width + xcoor, shift_down_even_in + ycoor)]))


        # draws vertical line to connect outputs
        if num_outputs % 2 == 1:
            self.segments.append(Segment([(io_width + width + xcoor, -shift_down_odd_out + ycoor),
                                          (io_width + width + xcoor, shift_down_odd_out + ycoor)]))
        else:
            self.segments.append(Segment([(io_width + width + xcoor, -shift_down_even_out + ycoor),
                                          (io_width + width + xcoor, shift_down_even_out + ycoor)]))


d = schemdraw.Drawing()

gate1 = GenericGate(['A', 'B', 'C'], ['Out'], [0, 3]).label("AND1")
gate2 = GenericGate(['A'], ['Out'], [0, 0]).label("AND2")
gate3 = GenericGate(['A', 'B'], ['Out'], [5, 2]).label("NOT")
connec1 = Connection(gate1.ow['Out'], gate3.iw['A'])
connec2 = Connection(gate2.ow['Out'], gate3.iw['B'])

d.add(gate1)
d.add(gate2)
d.add(gate3)
d.add(connec1)
d.add(connec2)

d.draw()
