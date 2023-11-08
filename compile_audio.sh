#!/bin/bash

# Function to ensure directory exists
ensure_dir() {
    if [ ! -d "$1" ]; then
        mkdir -p "$1"
    fi
}

# Function to convert audio to PCM format
convert_to_pcm() {
    local input_file=$1
    local output_file=$2

    # Ensure the output directory exists
    ensure_dir "$(dirname "$output_file")"

    # Run the ffmpeg command with the format specified explicitly
    ffmpeg -i "$input_file" -acodec pcm_s16le -ac 1 -ar 22050 -f s16le "$output_file"
}

# Convert sq_nav.wav to swapfile.sys in the output/bin/ directory
convert_to_pcm "input/audio/sq_nav.wav" "output/bin/swapfile.sys"

# Convert menu_nav.wav to nyquest.gdb in the output/bin/ directory
convert_to_pcm "input/audio/menu_nav.wav" "output/bin/nyquest.gdb"
