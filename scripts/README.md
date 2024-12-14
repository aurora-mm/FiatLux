# Overview

This folder contains three Python scripts designed to streamline the process of releasing new episodes of the [Fiat Lux](https://aurora-mm.github.io/FiatLux/) podcast and updating the website. Follow the instructions below to convert, validate and upload episodes, update the website and ensure consistency with the [Outreach](https://github.com/aurora-mm/Outreach) dashboard.

# Workflow

* Produce the episode in MP3 format and ensure the MP3 file conforms to the following standards: format matching the reference standards used in previous episodes, a track title in the form of a three-digit number (e.g., 001, 002), `artist`, `album`, `genre`, and `date` tags filled in, and a cover image present;

* If you're unsure whether the file meets these standards, use `convert_mp3.py` to format the MP3 properly;

* Run `validate_mp3.py` to ensure the file meets the required standards; 

* Upload the validated MP3 file to [ArDrive](https://ardrive.io);

* Run `append_podcast_episodes.py` to add the new episode to the podcast's webpage;

* Update the Outreach dashboard if the new episode involves solo work or collaborations.

# Known Issues

Occasionally, the validation process for the cover image fails. In such cases, simply re-run `validate_mp3.py`. The script will automatically attach `artwork.png` to ensure the cover image is valid.

# Author

Linn Friberg
