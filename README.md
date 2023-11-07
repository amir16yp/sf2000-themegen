# Datafrog SF2000 Theme Generator (Pre-alpha)

## What is this?
The Datafrog SF2000 Theme Generator is a tool designed for creating custom themes for the Datafrog SF2000 retro handheld console. It compiles PNG images and RGB color presets into a theme that can be applied to the console's user interface.

## How does it work?
The program includes a set of Python scripts and a configuration file that work together to generate and compile a theme.

### Important Files in the Root Folder
- `theme.json`: The main configuration file for the theme, written in JSON format.
- `gen_theme.py` (or `gen_theme.exe`): This script processes the PNG files according to the settings in `theme.json` to create a series of image files.
- `compile_to_Resources.py` (or `compile_to_Resources.exe`): This script compiles the images into a format compatible with the Datafrog SF2000. The compiled files are placed in the `output/bin` folder, which can then be transferred to the `Resources` directory on your SD card.
- `PressStart2P-Regular.ttf`: The font file used in the theme generation process.

### The Input Folder
The `input` folder should contain PNG files specific to each console:

- Console initials (e.g., `gb.png`, `snes.png`, `md.png`): These are the logos displayed in the stock ROM selection menu, appearing in the top-left corner.
- Background images (e.g., `snes_c.png`): These images are used inside the backgrounds on the home screen for each system.

### Using Subfolders for Boxart
You can replace the default boxart images for each system by using subfolders within the `input` directory:

1. Create a subfolder named after the system in lowercase (e.g., `snes`).
2. Place four PNG files inside this subfolder, named according to their position from left to right (e.g., `1.png`, `2.png`, `3.png`, `4.png`).

Included in this pre-alpha release is an example set of boxart for the NES system.

## Instructions for Use
1. Arrange your theme elements according to the folder structure described above.
2. Run `gen_theme.py` to generate the image files from your PNGs and `theme.json`.
3. Run `compile_to_Resources.py` to compile the generated images into a format recognized by the Datafrog SF2000.
4. Copy the output from the `output/bin` folder to the `Resources` folder on your SD card.
5. Insert the SD card into your Datafrog SF2000 and enjoy the new theme!

## Notes
- Ensure that all PNG files are formatted correctly and that the `theme.json` file is properly configured before running the scripts.
- This software is in pre-alpha stage, and feedback on its functionality is welcome.

## License
Licensed under the Unlicense
see LICENSE.md
