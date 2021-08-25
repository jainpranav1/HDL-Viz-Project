import gatedata as gd
import tkinter as tk
from tkinter import filedialog
from functools import partial
import hdl_image_maker as him
from PIL import ImageTk, Image

root = tk.Tk()
frame1 = tk.Frame(root)
plus_frame = tk.Frame(root)

frame1.pack(side="top")
plus_frame.pack(side="bottom")

# title
tk.Label(frame1,
         text="Chip Visualizer",
         bg="black",
         fg="white").pack(side="left",
                          ipadx=50,
                          ipady=5,
                          pady=30)

# Button for exiting out
quit = tk.Button(frame1,
                 text="x",
                 fg="white",
                 bg="red",
                 command=root.destroy)
quit.pack(side="left")

chip_frames = {}

# format of chip_frames:
# dictionary of dictionaries
# each item:
# { i : {frame:, button:, name:, run:, del:, data: }
# where
# i is the frame number
# frame is the frame object
# button is the button object
# name is the filename
# run is the run button
# del is the delete button
# data is a list of the data [gmatrix, wmatrix, phdl]

# prints gate
def print_data(filepath):
    him.image_maker(filepath)





# deletes the i-th chip on the list
def chip_delete(i):
    chip_frames[i]["frame"].destroy()
    chip_frames.pop(i)

def make_chip(i=0):
    filepath = filedialog.askopenfilename()
    print(filepath)
    filename = filepath.split("/")[-1]
    if (filename == ""):
        return
    else:
        chip_frames[i]["name"] = filename
        chip_frames[i]["button"]["text"] = filename

        run_button = tk.Button(chip_frames[i]["frame"],
                               text=">",
                               fg="green",
                               command=partial(print_data, filepath))

        del_button = tk.Button(chip_frames[i]["frame"],
                               text="x",
                               fg="red",
                               command=partial(chip_delete, i))

        chip_frames[i]["run"] = run_button
        chip_frames[i]["del"] = del_button

        chip_frames[i]["button"].pack(side="left")
        chip_frames[i]["run"].pack(side="left")
        chip_frames[i]["del"].pack(side="left")
    return filepath


# stores plus and minus buttons
plus_minus_dict = {}


# destroys the last chip on the list
def chip_decrement():
    i = len(chip_frames) - 1
    chip_frames[i]["frame"].destroy()
    chip_frames.pop(i)


# creates a new chip on the list
def chip_increment():
    chip_i = len(chip_frames)

    new_frame = tk.Frame(root)
    new_frame.pack(side="top")

    new_chip = tk.Button(new_frame,
                         text="Select File",
                         command=partial(make_chip, i=chip_i))
    new_chip.pack(side="top", ipadx=100)

    plus_minus_dict[0]["frame"].destroy()
    plus_minus_frame = tk.Frame(root)
    plus_minus_frame.pack(side="top")
    plus = tk.Button(plus_minus_frame,
                     text="+",
                     command=chip_increment)
    plus.pack(side="left")

    minus_frame = tk.Frame(root)
    minus_frame.pack(side="top")
    minus = tk.Button(plus_minus_frame,
                      text="−",
                      command=chip_decrement)
    minus.pack(side="left")

    plus_minus_dict[0] = {"frame": plus_minus_frame, "plus": plus, "minus": minus}

    chip_frames[chip_i] = {"frame": new_frame, "button": new_chip}


# default empty chip
default_frame = tk.Frame(root)
default_frame.pack(side="top")

default_chip = tk.Button(default_frame,
                         text="Select File",
                         command=partial(make_chip, 0))
default_chip.pack(side="top", ipadx=100)

chip_frames[0] = {"frame": default_frame, "button": default_chip}

# default plus and minus buttons
plus_minus_frame = tk.Frame(root)
plus_minus_frame.pack(side="top")
plus = tk.Button(plus_minus_frame,
                 text="+",
                 command=chip_increment)
plus.pack(side="left")

minus_frame = tk.Frame(root)
minus_frame.pack(side="top")
minus = tk.Button(plus_minus_frame,
                  text="−",
                  command=chip_decrement)
minus.pack(side="left")

plus_minus_dict[0] = {"frame": plus_minus_frame, "plus": plus, "minus": minus}

root.mainloop()