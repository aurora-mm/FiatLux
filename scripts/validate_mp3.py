# Script for validating a mp3 file according to the requirements

import requests
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3
from pydub.utils import mediainfo
import os
import re

def download_mp3(transaction_id, output_file):
    url = f"https://arweave.net/{transaction_id}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
    else:
        raise ValueError(f"Failed to download file: {response.status_code}")

def extract_mp3_metadata(file_path):
    tags = EasyID3(file_path)
    audio = ID3(file_path)
    attached_picture = None
    for tag in audio.getall("APIC"):
        attached_picture = tag.data
        break
    format_info = mediainfo(file_path).get("format", "")
    return {
        "tags": tags,
        "attached_picture": attached_picture,
        "format": format_info
    }

def attach_artwork(file_path, artwork_path):
    audio = MP3(file_path, ID3=ID3)
    try:
        audio.add_tags()
    except:
        pass  # Tags already exist
    with open(artwork_path, "rb") as img:
        audio.tags.add(
            APIC(
                encoding=3,  # UTF-8
                mime="image/png",  # MIME type of the image
                type=3,  # Front cover
                desc="Cover",
                data=img.read()
            )
        )
    audio.save()

def validate_input_file(input_metadata, reference_metadata, input_file):
    errors = []

    # Validate specific tags
    for key in ["artist", "album", "genre"]:
        if input_metadata["tags"].get(key) != reference_metadata["tags"].get(key):
            errors.append(f"Tag '{key}' does not match.")

    # Validate presence of "track title" and "date"
    if "title" not in input_metadata["tags"]:
        errors.append("Tag 'track title' is missing.")
    elif not re.fullmatch(r"\d{3}", input_metadata["tags"]["title"][0]):
        errors.append("Tag 'track title' is not a three-digit number.")

    if "date" not in input_metadata["tags"]:
        errors.append("Tag 'date' is missing.")

    # Validate attached pictures
    if input_metadata["attached_picture"] != reference_metadata["attached_picture"]:
        errors.append("Attached pictures do not match.")
        print("Cover artwork does not match. Replacing with local artwork.")
        attach_artwork(input_file, "artwork.png")

    # Validate format
    if input_metadata["format"] != reference_metadata["format"]:
        errors.append(f"File format '{input_metadata['format']}' does not match reference '{reference_metadata['format']}'.")

    return errors

def main():
    # Input
    input_file = input("Enter the path to the input MP3 file: ").strip()
    transaction_id = "gs5uwKrGOy2TdBJyvG26dhhq1mjpTq4tgDm2NoRPU1k" # Fiat Lux 003

    # Download reference file
    reference_file = "reference.mp3"
    download_mp3(transaction_id, reference_file)

    try:
        # Extract metadata
        input_metadata = extract_mp3_metadata(input_file)
        reference_metadata = extract_mp3_metadata(reference_file)

        # Validate input file
        errors = validate_input_file(input_metadata, reference_metadata, input_file)

        if errors:
            for error in errors:
                print(f"Error: {error}")
        else:
            print("All requirements are satisfied. You can upload the file to ArDrive.")

    finally:
        # Clean up
        if os.path.exists(reference_file):
            os.remove(reference_file)

if __name__ == "__main__":
    main()
