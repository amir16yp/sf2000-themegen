#!/usr/bin/python3

from PIL import Image, ImageDraw, ImageFont
import os.path
import shutil
import json


def load_theme_config():
    # Load configuration from theme.json
    theme_config = {}
    with open('theme.json', 'r') as f:
        theme_config = json.loads(f.read())
    return theme_config


def create_gradient_background(width, height, start_color, end_color, direction):
    base = Image.new('RGB', (width, height), start_color)
    top = Image.new('RGB', (width, height), end_color)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base


def create_dark_background(width, height, config_bg):
    bg_type = config_bg.get("type", "solid")
    if bg_type == "gradient":
        start_color = tuple(config_bg["start_color"])
        end_color = tuple(config_bg["end_color"])
        direction = config_bg["direction"]
        return create_gradient_background(width, height, start_color, end_color, direction)
    else:
        rgb = tuple(config_bg.get("color", [0, 0, 0]))
        image = Image.new("RGB", (width, height), rgb)
        return image


def draw_frames_on_background(console, image):
    draw = ImageDraw.Draw(image)
    rect_coords_and_numbers = [
        (43, 290, 163, 410),
        (188, 290, 308, 410),
        (333, 290, 453, 410),
        (478, 290, 598, 410)
    ]
    font_size = 66
    try:
        font = ImageFont.truetype("PressStart2P-Regular.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    for idx, (left, top, right, bottom) in enumerate(rect_coords_and_numbers, start=1):
        file_path = os.path.join("input", console, f"{idx}.png")
        if os.path.isfile(file_path):
            frame_image = Image.open(file_path)
            frame_image = frame_image.resize((right - left, bottom - top))
            image.paste(frame_image, (left, top))
        else:
            rect_color = (255, 255, 255)
            draw.rectangle([left, top, right, bottom], outline=rect_color, width=2)
            text_x, text_y = left + 5, top + 5
            draw.text((text_x, text_y), str(idx), fill="white", font=font)

    return image


def generate_console_background(console, console_image_path, bg_image_path, corner="top_right", numbers=True):
    print(f'generating main menu background for {console}')
    theme_config = load_theme_config()

    # Create an inverted gradient background
    bg_image = create_dark_background(640, 480, theme_config["game_menu_background"])

    # Add top and bottom bar drawing logic here, similar to create_listing_image
    draw = ImageDraw.Draw(bg_image)
    top_bar_height = theme_config.get("console_top_bar_size_px", 0)
    bottom_bar_height = theme_config.get("console_bottom_bar_size_px", 0)
    top_bar_color = tuple(theme_config.get("console_top_bar_color_rgb", [0, 0, 0]))
    bottom_bar_color = tuple(theme_config.get("console_bottom_bar_color_rgb", [0, 0, 0]))

    # Draw top bar
    draw.rectangle([(0, 0), (640, top_bar_height)], fill=top_bar_color)

    # Draw bottom bar
    draw.rectangle([(0, 480 - bottom_bar_height), (640, 480)], fill=bottom_bar_color)

    if console_image_path:

        # Open the console image
        console_image = Image.open(console_image_path)

        # Calculate the new size maintaining the aspect ratio within a maximum width
        max_console_width = 150  # Maximum width for the console image to fit nicely on the background
        aspect_ratio = console_image.width / console_image.height
        new_console_width = min(console_image.width, max_console_width)
        new_console_height = int(new_console_width / aspect_ratio)
        console_image = console_image.resize((new_console_width, new_console_height))

        # Calculate the position for the console image based on the corner
        if corner == "top_left":
            position = (10, 100)  # Padding of 10 pixels from the top left corner
        elif corner == "top_right":
            position = (640 - new_console_width - 10, 100)  # Padding of 10 pixels from the top right corner
        else:
            raise ValueError("Invalid corner specified. Use 'top_left' or 'top_right'.")

        # Paste the console image onto the background
        bg_image.paste(console_image, position, console_image if console_image.mode == 'RGBA' else None)

    if numbers:
        # Draw rectangles with larger numbers on the background
        bg_image = draw_frames_on_background(console, bg_image)

    # Save the final image with the console name
    bg_image.save("output/" + bg_image_path)

    return bg_image_path


def create_listing_image(console_name, image_path, output_file, include_text=True):
    print(f'generating ROM listing background for {console_name}')
    theme_config = load_theme_config()

    # Create a new image with RGB mode and black background
    img = create_dark_background(640, 480, theme_config["game_menu_background"])
    draw = ImageDraw.Draw(img)
    background_color_above_line = tuple(theme_config.get("game_menu_top_bar_color_rgb", [0, 0, 0]))

    image_width = 640
    header_height = theme_config.get("game_menu_top_bar_size_px", 0)
    bottom_bar_height = theme_config.get("game_menu_bottom_bar_size_px", 0)
    bottom_bar_color = tuple(theme_config.get("game_menu_bottom_bar_color_rgb", [0, 0, 0]))

    # Draw the header bar
    draw.rectangle([(0, 0), (image_width, header_height)], fill=background_color_above_line)

    # Draw the bottom bar
    draw.rectangle([(0, 480 - bottom_bar_height), (image_width, 480)], fill=bottom_bar_color)

    # Load and process the image to be pasted (logo)
    logo = Image.open(image_path)
    # Calculate its size to fit the height of 50px while maintaining aspect ratio
    aspect_ratio = logo.width / logo.height
    logo_height = 50
    logo_width = int(aspect_ratio * logo_height)
    logo = logo.resize((logo_width, logo_height))

    # Draw the horizontal line at y=header_height
    line_color = "white"
    draw.line((0, header_height, image_width, header_height), fill=line_color)

    # Calculate logo and text positions
    logo_position = (10, (header_height - logo_height) // 2)
    text_x = logo_position[0] + logo_width + 10
    text_position = (text_x, (header_height - logo_height) // 2)

    # Paste the logo image at its position
    img.paste(logo, logo_position, logo)
    if include_text:

    # Load custom font and set the font size
        font_size = 36  # You can adjust the font size as needed
        try:
            font = ImageFont.truetype('PressStart2P-Regular.ttf', font_size)
        except IOError:
            font = ImageFont.load_default()  # Use default font if the custom font is not available

        # Draw the console name text next to the logo
        draw.text(text_position, console_name, fill="white", font=font)

    # Save the final image
    img.save('output/' + output_file, format='PNG')


def copy_generic_image(filepath):
    filename = os.path.basename(filepath)
    print(f'copying generic background image {filename}')
    shutil.copy(filepath, 'output/' + filename)


# TODO: surely there's a better way to do this but i cant be arsed right now
generate_console_background("snes", "input/snes_c.png", "snes_c.png")  # drivr.ers
generate_console_background("md", "input/md_c.png", "md_c.png")  # icuin.cpl
generate_console_background("gb", "input/gb_c.png", "gb_c.png")  # irftp.ctp
generate_console_background("gbc", "input/gbc_c.png", "gbc_c.png")  # qwave.bke
generate_console_background("gba", "input/gba_c.png", "gba_c.png")  # irftp.ctp
generate_console_background("nes", "input/nes_c.png", "nes_c.png")  # fixas.ctp
generate_console_background("mame", None, "mame_c.png")  # hctml.ers
generate_console_background("settings", "input/settings_c.png", "settings.png", "top_right", False)  # dsuei.cpl
copy_generic_image("input/lowbattery.png")  # jccatm.kbp

create_listing_image('SNES', 'input/snes.png', 'snes_bg.png')  # c1eac.pal
create_listing_image('GB', 'input/gb.png', 'gb_bg.png')  # fltmc.sta
create_listing_image('GBC', 'input/gbc.png', 'gbc_bg.png')  # cero.phl
create_listing_image('GBA', 'input/gba.png', 'gba_bg.png')  # efsui.stc
create_listing_image('NES', 'input/nes.png', 'nes_bg.png')  # urlkp.bvs
create_listing_image('MAME', 'input/mame.png', 'mame_bg.png')  # apisa.dlk
create_listing_image('MD', 'input/md.png', 'md_bg.png')  # ihdsf.bke
create_listing_image('Search', 'input/search.png', 'search_bg.png', include_text=False) # lfsvc.dll		
