import os
import struct
from PIL import Image, ImageDraw, ImageFont

# Function to convert an image to RGB565 Little Endian format
def convert_image_to_rgb565_le(image_path, output_path):
    img = Image.open(image_path)
    print("current image:" + image_path)
    img = img.convert("RGB")

    # Create a bytes object to store the converted image data
    rgb565_data = bytes()

    for pixel in img.getdata():
        r, g, b = pixel
        # Convert RGB values to 5-bit red, 6-bit green, and 5-bit blue
        r = (r >> 3) & 0x1F
        g = (g >> 2) & 0x3F
        b = (b >> 3) & 0x1F

        # Pack the RGB565 values into a 16-bit little-endian binary data
        pixel_data = struct.pack("<H", (r << 11) | (g << 5) | b)

        # Append the pixel data to the output bytes
        rgb565_data += pixel_data

    # Save the converted data as a binary file with the specified output filename
    with open(output_path, "wb") as output_file:
        output_file.write(rgb565_data)
        print("saved " + output_path)

def convert_to_bgra(image_path):
    try:
        # Open the image using Pillow
        image = Image.open(image_path)

        # Convert the image to the 'RGBA' mode
        image = image.convert('RGBA')

        # Create a new image with BGRA mode
        bgra_image = Image.new('BGRA', image.size)

        # Composite the RGBA image onto the BGRA image
        bgra_image.paste(image, (0, 0), image)

        return bgra_image
    except Exception as e:
        print(f"Error: {e}")
        return None

# List of console backgrounds with corresponding filenames
console_backgrounds = [
    ("snes_c.png", "drivr.ers"),
    ("md_c.png", "icuin.cpl"),
    ("gb_c.png", "xajkg.hsp"),
    ("gbc_c.png", "qwave.bke"),
    ("gba_c.png", "irftp.ctp"),
    ("nes_c.png", "fixas.ctp"),
    ("mame_c.png", "hctml.ers"),
    ("settings.png", "dsuei.cpl"),
    ("lowbattery.png", "jccatm.kbp")
]

# List of console listing images with corresponding filenames (only ending with "_bg")
console_listing_images = [
    ('SNES', 'snes_bg.png', 'c1eac.pal'),
    ('GB', 'gb_bg.png', 'fltmc.sta'),
    ('GBC', 'gbc_bg.png', 'cero.phl'),
    ('GBA', 'gba_bg.png', 'efsui.stc'),
    ('NES', 'nes_bg.png', 'urlkp.bvs'),
    ('MAME', 'mame_bg.png', 'apisa.dlk'),
    ('MD', 'md_bg.png', 'ihdsf.bke')
]

# Define the folder containing the images
input_folder = "output"
output_folder = "output/bin"

# Convert console backgrounds and save with specified filenames
for console_bg, output_filename in console_backgrounds:
    # Construct the full paths for the input and output files
    input_path = os.path.join(input_folder, console_bg)
    output_path = os.path.join(output_folder, output_filename.replace(".png", ".rgb565le"))
    
    # Convert the image and save it with the new file extension
    convert_image_to_rgb565_le(input_path, output_path)

# Convert console listing images (ending with "_bg") and save with specified filenames
for console_name, image_path, output_filename in console_listing_images:
    # Construct the full paths for the input and output files
    input_path = os.path.join(input_folder, image_path)
    output_path = os.path.join(output_folder, output_filename.replace(".png", ".rgb565le"))
    
    # Convert the image and save it with the new file extension
    convert_image_to_rgb565_le(input_path, output_path)


#main_menu = convert_to_bgra("mainmenu.png")
#path = os.path.join(output_folder,"sfcdr.cpl")
#print("saving " + path)
#main_menu.save(path)
