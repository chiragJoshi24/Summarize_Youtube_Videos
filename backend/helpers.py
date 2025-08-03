import re
import requests
from bs4 import BeautifulSoup

def extract_video_id(url):
    match = re.search(r'(?:v=|\/)([0-9A-za-z_-]{11})', url)
    return match.group(1) if match else None


def get_video_title(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        title_tag = soup.find('title')
        return title_tag.text if title_tag else "Unknown Title"
    except Exception as e:
        print(f"Error fetching video title: {e}")
        return "Unknown Title"

