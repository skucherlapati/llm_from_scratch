"""Functions to build vocab from a given text file."""
import urllib.request
import logging
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(encoding="utf-8", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

the_verdict_url = "https://raw.githubusercontent.com/rasbt/LLMs-from-scratch/refs/heads/main/ch02/01_main-chapter-code/the-verdict.txt"
the_verdict_file_path = "the-verdict.txt"

def download_text_data(url: str = the_verdict_url, filepath: str = the_verdict_file_path):
    """Download a text file from given url."""
    if not url.endswith(".txt"):
        raise ValueError("URL must be a valid text file endpoint. It must end with '.txt'")
    urllib.request.urlretrieve(url, filepath)

def read_text_file(filepath: str = the_verdict_file_path) -> str:
    """Read text file."""
    with open(filepath, "r", encoding="utf-8") as f:
        raw_text = f.read()
    
    logger.debug(f"Total number of characters in text: {len(raw_text)}")
    logger.debug(raw_text[:99])
    return raw_text


if __name__ == "__main__":
    download_text_data()
    raw_text = read_text_file()