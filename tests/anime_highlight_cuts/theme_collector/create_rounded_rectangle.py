
from PIL import Image, ImageDraw
def rectangle():
    image = Image.new("BGR", (800,
     400), "black")
    draw = ImageDraw.Draw(image)
    # Draw a regular rectangle
    draw.rectangle((200, 100, 300, 200), fill="white")
    # Draw a rounded rectangle
    draw.rounded_rectangle((50, 50, 150, 150), fill="white", radius=20)
    image.