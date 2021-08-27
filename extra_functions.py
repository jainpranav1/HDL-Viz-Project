import schemdraw.elements as elm
from schemdraw.segments import *


def matrix_maker(num_rows, num_cols, value):
    # alternative to numpy.zeros
    # makes a matrix filled with specified value

    matrix = []
    for i in range(0, num_rows):
        matrix.append([])
        for j in range(0, num_cols):
            matrix[i].append(value)
    return matrix


def vector_maker(num_elems, value):
    # makes a vector filled with specified value

    vector = []
    for i in range(0, num_elems):
        vector.append(value)
    return vector


def sum_lists(list_array):
    # adds all lists in list_array together

    output = vector_maker(len(list_array[0]), 0)
    for list in list_array:
        for i in range(0, len(list)):
            output[i] += list[i]
    return output


def sub_list(list1, list2):
    return [list1[0]-list2[0], list1[1]-list2[1]]


def div_list(list1, n):
    return [list1[0]/n, list1[1]/n]


def print_matrix(matrix):
    for line in matrix:
        print(line)


class Wire(elm.Element):
    def __init__(self, path, color):
        super().__init__()

        line = Segment(path)
        line.color = color
        self.segments.append(line)
