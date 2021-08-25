import hdl_image_maker
import sys

if(len(sys.argv) < 2):
	print("please include an HDL file as an argument :)")
else:
	hdl_image_maker.image_maker(sys.argv[1])