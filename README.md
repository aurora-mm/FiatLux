# Overview

This repository contains the source code and Python tools for the **Fiat Lux** experimental podcast series website. The podcast series experiments with sounds, format, and delivery, offering something unexpected every episode. Originally generated using [CD-R 700mb](https://github.com/thebaer/cdr), the HTML structure has been customized to meet the podcast's specific requirements.

# Repository Structure

`index.html`: The main HTML file for the website, including embedded audio player and playlist functionality.

`scripts/`: Contains Python scripts designed for validating MP3 files (to ensure they meet common podcast audio standards) and automating the process of adding new podcast episodes to the `index.html` file.

# Dependencies

`requests`, `mutagen`, `pydub`, `json`, `BeautifulSoup`, `os`, `re`, `subprocess`

# Usage

For detailed instructions on how to update the website, refer to the files in the `scripts/` folder.

# Author

Linn Friberg
