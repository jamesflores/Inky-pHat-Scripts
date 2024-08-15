import textwrap
from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont
import requests


def main():
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    joke = get_dad_joke()
    if joke:
        draw_centered_text(joke, font_path, rotate=180, font_size=20)
    else:
        print("Failed to fetch a dad joke.")


def get_dad_joke():
    url = "https://icanhazdadjoke.com"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200 and response.json():
        return response.json()['joke']
    return None


def draw_centered_text(text, font_path, rotate=0, font_size=20):
    # Initialize InkyPHAT
    inky_display = auto()
    inky_display.set_border(inky_display.WHITE)

    # Create a new PIL image
    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT), inky_display.WHITE)
    draw = ImageDraw.Draw(img)

    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    # Determine maximum width for text wrapping
    max_width = inky_display.HEIGHT - 10 if rotate in (90, 270) else inky_display.WIDTH - 10

    # Wrap the text with dynamic width calculation
    wrapped_text = []
    for i in range(len(text), 0, -1):
        wrapped_text = textwrap.wrap(text, width=i)
        longest_line = max(wrapped_text, key=len)
        bbox = font.getbbox(longest_line)
        line_width = bbox[2] - bbox[0]
        if line_width <= max_width:
            break

    # Calculate total height of wrapped text
    bbox = font.getbbox('hg')  # 'hg' accounts for ascenders and descenders
    line_height = bbox[3] - bbox[1]
    total_height = len(wrapped_text) * line_height

    # Calculate starting position to center vertically
    y = (inky_display.HEIGHT - total_height) // 2 if rotate in (0, 180) else (inky_display.WIDTH - total_height) // 2

    # Draw each line of text
    for line in wrapped_text:
        bbox = font.getbbox(line)
        line_width = bbox[2] - bbox[0]
        x = (inky_display.WIDTH - line_width) // 2 if rotate in (0, 180) else (inky_display.HEIGHT - line_width) // 2
        draw.text((x, y), line, inky_display.BLACK, font=font)
        y += line_height

    # Rotate and display the image
    inky_display.set_image(img.rotate(rotate))
    inky_display.show()


if __name__ == "__main__":
    main()

