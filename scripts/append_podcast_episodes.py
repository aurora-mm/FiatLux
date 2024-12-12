# Script for updating the podcast webpage

import os
import json
import subprocess
from bs4 import BeautifulSoup

def fetch_ardrive_data(drive_id):
    """
    Runs the ardrive list-drive command and returns the parsed JSON output.
    """
    # Setup the environment explicitly
    # (Specify your path to ardrive manually, and in PyCharm in the configuration)
    env = os.environ.copy()
    env["PATH"] = os.path.dirname("/Users/lrf/.nvm/versions/node/v23.4.0/bin/ardrive") + ":" + env.get("PATH", "")

    # Run the ardrive command
    command = ["/Users/lrf/.nvm/versions/node/v23.4.0/bin/ardrive", "list-drive", "-d", drive_id]
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        env=env
    )
    if result.returncode != 0:
        raise RuntimeError(f"Error running ardrive command: {result.stderr}")

    return json.loads(result.stdout)

def load_existing_episodes(file_path):
    """
    Loads existing episode numbers from the local file.
    """
    with open(file_path, "r") as file:
        return {line.strip() for line in file.readlines()}

def load_description(file_path):
    """
    Loads the description for new episode from the local file.
    """
    with open(file_path, "r") as file:
        return file.read().strip()

def construct_new_episodes(ardrive_data, existing_episodes, description):
    """
    Constructs the list of new episodes from ArDrive data.
    """
    new_episodes = []
    for item in ardrive_data:
        if item["entityType"] == "file" and item["path"].endswith(".mp3"):
            episode_number = item["path"].split("/")[-1].split(".")[0]
            if episode_number not in existing_episodes:
                new_episodes.append({
                    "number": episode_number,
                    "title": episode_number,
                    "link": f"https://arweave.net/{item['dataTxId']}",
                    "description": description
                })
    return new_episodes

# Function to append new podcast episodes to the HTML file
def append_podcast_episodes(html_file, new_episodes, output_file):
    """
    Appends new podcast episodes to an existing HTML file, updating the playlist and player.
    """

    # Load the HTML file
    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Find the playlist <ol> element by its id
    playlist = soup.find("ol", id="playlist")

    if not playlist:
        raise ValueError("<ol id='playlist'> element not found in the HTML file")

    # Remove "active" class from any existing <li> elements
    for li in playlist.find_all("li", class_="active"):
        li.attrs.pop("class", None)

    # Append new episodes to the playlist
    for episode in new_episodes:
        li = soup.new_tag("li")
        a_tag = soup.new_tag("a", href=episode["link"], **{
            "class": "track",
            "data-artist": "Fiat Lux",
            "data-title": episode["title"]
        })
        a_tag.string = f"Fiat Lux - {episode['number']}"
        li.append(a_tag)

        p_tag = soup.new_tag("p", align="justify")
        description_soup = BeautifulSoup(episode["description"], "html.parser")
        for child in description_soup.contents:
            p_tag.append(child)  # Append parsed HTML content to the <p>
        li.append(p_tag)

        playlist.append(li)

    # Mark the latest episode as active
    latest_li = playlist.find_all("li")[-1]
    latest_li["class"] = "active"

    # Update the audio player source
    audio_tag = soup.find("audio", id="player")
    if audio_tag and latest_li:
        latest_a_tag = latest_li.find("a", class_="track")
        if latest_a_tag:
            source_tag = audio_tag.find("source")
            if source_tag:
                source_tag["src"] = latest_a_tag["href"]

    # Save the updated HTML to a new file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(str(soup))

def update_episode_list(file_path, new_episodes):
    """
    Updates the episode_list.txt file with new episode numbers.
    """
    with open(file_path, "a") as file:
        for episode in new_episodes:
            file.write(f"{episode['number']}\n")

# Variables
DRIVE_ID = "cb43e8af-be46-4f22-9530-11875a213008"
EXISTING_EPISODES_FILE = "episode_list.txt"
DESCRIPTION_FILE = "new_episode_description.txt"
HTML_FILE = "index.html"
OUTPUT_HTML_FILE = "fiat_lux_updated.html"

try:
    # Fetch data from ArDrive
    ardrive_data = fetch_ardrive_data(DRIVE_ID)

    # Load existing episodes and description
    existing_episodes = load_existing_episodes(EXISTING_EPISODES_FILE)
    description = load_description(DESCRIPTION_FILE)

    # Construct new episodes list
    new_episodes = construct_new_episodes(ardrive_data, existing_episodes, description)

    if new_episodes:
        append_podcast_episodes(HTML_FILE, new_episodes, OUTPUT_HTML_FILE)
        update_episode_list(EXISTING_EPISODES_FILE, new_episodes)
    else:
        print("No new episodes found. Nothing to update.")

    print(f"HTML updated successfully with {len(new_episodes)} new episodes.")

except Exception as e:
    print(f"Error: {e}")