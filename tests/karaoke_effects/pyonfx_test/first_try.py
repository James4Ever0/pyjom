from pyonfx import *

io = Ass("in.ass")
meta, styles, lines = io.get_data()

lines[0].text = "I am a new line!"
io.write_line(lines[0])

io.save()
# io.open_aegisub()
# there's no aegisub.