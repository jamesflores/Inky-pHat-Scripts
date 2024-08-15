from inky import InkyPHAT
from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont


# Initialize InkyPHAT manually without EEPROM
inky_display = auto()
inky_display.set_border(inky_display.WHITE)
print(f"Inky dimensions {inky_display.WIDTH}x{inky_display.HEIGHT}")


# Create a new PIL image with the dimensions of the InkyPHAT
img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT), inky_display.WHITE)
draw = ImageDraw.Draw(img)


# Load a font
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)


# Sample text to display
text = "Hello world"


# Calculate the size of the text and position it at the center
text_bbox = draw.textbbox((0, 0), text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]
x = (inky_display.WIDTH - text_width) // 2
y = (inky_display.HEIGHT - text_height) // 2


# Draw the text onto the image
draw.text((x, y), text, inky_display.BLACK, font)


# Display the image on InkyPHAT
inky_display.set_image(img.rotate(180))  # mine is upside down
inky_display.show()

