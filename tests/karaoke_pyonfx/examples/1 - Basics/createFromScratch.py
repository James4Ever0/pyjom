from pyonfx import *
import os
os.system("touch output_scratch.ass")
io = Ass("output_scratch.ass",path_output="output_scratch.ass")

newLine = Line()
newLine.text = "hello world"
newLine.start_time = 0
newLine.end_time = 10
newLine.comment=False

io.write_line(newLine)
io.save()