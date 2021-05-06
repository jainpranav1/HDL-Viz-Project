from nand2tetris_hdl_parser import parse_hdl
import getpins

class Gate:
    def __init__(self, name_gate, inputs, outputs):
        self.name = name_gate
        self.inputs = inputs
        self.outputs = outputs


class Connector:
    def __init__(self, name_con, start, end):
        self.name = name_con
        self.start = start
        self.end = end


og_file = open("CustomChip1.hdl", "r")
hdl = og_file.read()

gate_dict = {}
count1 = 1
for chip in parse_hdl(hdl)['parts']:
    # creates a gate object for each gate
    # gate objects stored in gate_dict (accessed with Gate_1, Gate_2, etc.)

    name = chip['name']
    init_in = []
    init_out = []
    input_arr, output_arr = getpins.get_pins(chip, og_file)

    # stores input and output names on arrays
    for i in range(0, len(input_arr)):
        init_in.append(input_arr[i]['name'])
    for j in range(0, len(output_arr)):
        init_out.append(output_arr[j]['name'])

    # determines which inputs and outputs are split
    dup_in = []
    dup_out = []
    int_chip = chip['internal']
    for i in init_in:
        count2 = 0
        for j in int_chip:
            if i == j['name']:
                count2 += 1
            if count2 > 1:
                break
        if count2 > 1:
            dup_in.append(True)
        else:
            dup_in.append(False)

    for i in init_out:
        count2 = 0
        for j in int_chip:
            if i == j['name']:
                count2 += 1
            if count2 > 1:
                break
        if count2 > 1:
            dup_out.append(True)
        else:
            dup_out.append(False)

    # adds sizes to inputs and outputs which are split
    actual_in = []
    actual_out = []
    for i in range(0, len(int_chip)):
        try:
            ind = init_in.index(int_chip[i]['name'])
            if dup_in[ind]:
                actual_in.append(int_chip[i]['name'] + "[" + str(int_chip[i]['start']) + ".." + str(int_chip[i]['end']) + "]")
            else:
                actual_in.append(int_chip[i]['name'])
        except ValueError:
            ind = init_out.index(int_chip[i]['name'])
            if dup_out[ind]:
                actual_out.append(int_chip[i]['name'] + "[" + str(int_chip[i]['start']) + ".." + str(int_chip[i]['end']) + "]")
            else:
                actual_out.append(int_chip[i]['name'])

    # creates a gate object for each gate and saves
    gate_dict["Gate_" + str(count1)] = Gate(name, actual_in, actual_out)
    count1 += 1

    print(actual_in, actual_out)
