from pyonfx import *

io = Ass(path_output="output_scratch.ass")

newLine = Line()
newLine.text = "hello world"
newLine.start_time = 0
newLine.end_time = 10

io.write_line(newLine)
io.save()