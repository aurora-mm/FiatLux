# Script for converting an audio file to the desired format for Fiat Lux

import os
import subprocess
from datetime import datetime

def read_next_track_number(filename):
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1].strip()
                if last_line.isdigit():
                    return f"{int(last_line) + 1:03}"
            return "000"
    except FileNotFoundError:
        return "000"

def write_new_track_number(filename, track_number):
    with open(filename, "a") as f:
        f.write(track_number + "\n")

def convert_to_mp3(input_file, output_file, track_number):
    metadata = {
        "artist": "Fiat Lux",
        "album": "Fiat Lux",
        "title": f"{track_number}",
        "date": datetime.now().year,
        "genre": "Podcast",
    }

    metadata_args = []
    for key, value in metadata.items():
        metadata_args.extend(["-metadata", f"{key}={value}"])

    command = [
        "ffmpeg",
        "-i", input_file,  # Input audio file
        "-codec:a", "libmp3lame",
        "-qscale:a", "5",  # VBR V5 quality
        "-ar", "44100",
        *metadata_args,
        "-id3v2_version", "3",  # Use ID3v2.3 for better compatibility
        output_file
    ]

    subprocess.run(command, check=True)

def main():
    episode_list_file = "episode_list.txt"

    # Input and output files
    input_file = input("Enter the input audio file path: ").strip()
    if not os.path.isfile(input_file):
        print("Input file does not exist.")
        return

    # Get the next track number
    next_track_number = read_next_track_number(episode_list_file)

    # Define output file
    output_file = f"{next_track_number}.mp3"

    # Convert to MP3 with metadata and artwork
    try:
        convert_to_mp3(input_file, output_file, next_track_number)
        write_new_track_number(episode_list_file, next_track_number)
        print(f"Conversion complete. File saved as: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

if __name__ == "__main__":
    main()
