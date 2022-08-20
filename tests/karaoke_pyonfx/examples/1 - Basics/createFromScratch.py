from pyonfx import *
os.system("touch "output_scratch.ass"")
io = Ass("output_scratch.ass",path_output="output_scratch.ass")

newLine = Line()
newLine.text = "hello world"
newLine.start_time = 0
newLine.end_time = 10

io.write_line(newLine)
io.save()