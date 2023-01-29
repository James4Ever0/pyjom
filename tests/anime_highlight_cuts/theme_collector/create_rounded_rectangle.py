
from PIL import Image, ImageDraw
def rectangle(output_path):
    image = Image.new("BGR", (400, 400), "black")
    draw = ImageDraw.Draw(image)
    # Draw a regular rectangle
    draw.rectangle((200, 100, 300, 200), fill="red")
    # Draw a rounded rectangle
    draw.rounded_rectangle((50, 50, 150, 150), fill="blue", outline="yellow",
                           width=3, radius=7)