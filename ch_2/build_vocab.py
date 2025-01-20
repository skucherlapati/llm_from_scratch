"""Functions to build vocab from a given text file."""
import urllib.request
import logging
import re

logger = logging.getLogger(__name__)
logging.basicConfig(encoding="utf-8", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

RE_TOKENIZER = re.compile(r"([,.:;?_!\"()\']|--|\s)")
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

def convert_text_to_words(raw_text: str) -> list[str]:
    """Splits raw text into tokens."""
    preprocessed: list[str] = RE_TOKENIZER.split(raw_text)
    preprocessed = [item.strip() for item in preprocessed if item.strip()]
    logger.debug(f"Length of text split into tokens: len(preprocessed)")
    logger.debug(preprocessed[:30])
    return preprocessed

def create_vocab(preprocessed: list[str], debug: bool = True):
    """Create vocab from list of words."""
    all_words = sorted(set(preprocessed))
    vocab_size = len(all_words)
    logger.info(f"Vocab size: {vocab_size}")
    vocab = {token: ii for ii, token in enumerate(all_words)}
    if debug:
        for ii, token in vocab.items():
            logger.debug(token)
            if ii >= 50:
                break
    return vocab


def main():
    """Build vocab from the verdict text."""
    download_text_data()
    raw_text = read_text_file()
    words = convert_text_to_words(raw_text)
    vocab = create_vocab(words)
    return vocab


if __name__ == "__main__":
    main()