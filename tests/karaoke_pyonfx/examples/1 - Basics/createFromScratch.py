from pyonfx import *

io = Ass(save_path="")

newLine = Line()
newLine.text = "hello world"
newLine.start_time = 0
newLine.end_time = 10

io.write_line(newLine)
io.save()