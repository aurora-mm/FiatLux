# Script for updating the podcast web page

from bs4 import BeautifulSoup

# Define new episodes to be added
new_episodes = [
    {
        "number": "010",
        "title": "010",
        "link": "https://archive.org/download/fiat-lux-podcast/10.%20Fiat%20Lux%20010.mp3",
        "description": "Fiat Lux 010 offers an incredible mix of experimental sounds and unique tunes. Don\'t miss this installment!"
    }
]

# Function to append new podcast episodes to the HTML file
def append_podcast_episodes(html_file, new_episodes, output_file):
    """
    Appends new podcast episodes to an existing HTML file, updating the playlist and player.

    Args:
    - html_file (str): Path to the input HTML file to modify.
    - new_episodes (list): A list of dictionaries containing the new episodes to add.
    - output_file (str): Path to the output HTML file where the updated content will be saved.
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
        p_tag.string = episode["description"]
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

# Call the function
append_podcast_episodes("index.html", new_episodes, "fiat_lux_updated.html")