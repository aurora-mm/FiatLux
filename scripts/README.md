# Overview

This repository contains two Python scripts to assist in releasing new episodes of the [Fiat Lux](https://aurora-mm.github.io/FiatLux/) podcast and updating the website. Follow the instructions below to validate and upload episodes, update the website and ensure consistency with the [Outreach](https://github.com/aurora-mm/Outreach) dashboard.

# Workflow

* Produce the episode in MP3 format and ensure the MP3 file conforms to the following standards: format matching reference standards (see old episodes), a track title in the form of a three-digit number (e.g., 001, 002), `artist`, `album`, `genre`, and `date` tags filled in, and a cover image present;

* Run `validate_mp3.py` to ensure the file meets the required standards;

* Upload the validated MP3 file to [ArDrive](https://ardrive.io);

* Run `append_podcast_episodes.py` to add the new episode to the podcast's webpage;

* Update the Outreach dashboard if the new episode involves solo work or collaborations.

# Roadmap

The third script is to be produced, which coerces the input file to reference standards using `ffmpeg`.

# Author

Linn Friberg
