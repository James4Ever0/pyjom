import pixie

image = pixie.Image(200,200)

path = pixie.Path()
path.rounded_rect(20,20,100,100,25,25,25,25)
paint = pixie.Paint(pixie.SOLID_PAINT)
paint.color = pixie.Color(0,1,0,1)

image.stroke_path(path, paint=paint, stroke_width=3)

image.write_file('stroke_round_rect.png')

# stroke on a transparent background. well shit.