"""Functions to build vocab from a given text file."""
import urllib.request
import logging
import re

logger = logging.getLogger(__name__)
logging.basicConfig(encoding="utf-8", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# STATIC VARS
RE_TOKENIZER = re.compile(r"([,.:;?_!\"()\']|--|\s)")
THE_VERDICT_URL = "https://raw.githubusercontent.com/rasbt/LLMs-from-scratch/refs/heads/main/ch02/01_main-chapter-code/the-verdict.txt"
THE_VERDICT_FILE_PATH = "the-verdict.txt"
UNK_TOKEN = "<|unk|>"
DOC_SEP_TOKEN = "<|endoftext|>"


def download_text_data(url: str, filepath: str):
    """Download a text file from given url."""
    if not url.endswith(".txt"):
        raise ValueError("URL must be a valid text file endpoint. It must end with '.txt'")
    urllib.request.urlretrieve(url, filepath)

def read_text_file(filepath: str) -> str:
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
    logger.debug(f"Length of text split into tokens: {len(preprocessed)}")
    logger.debug(preprocessed[:30])
    return preprocessed

def create_vocab(preprocessed: list[str], debug: bool = True):
    """Create vocab from list of words."""
    all_words = sorted(set(preprocessed))
    vocab_size = len(all_words)
    logger.info(f"Vocab size: {vocab_size}")
    vocab = {token: ii for ii, token in enumerate(all_words)}
    if debug:
        for token, i in vocab.items():
            logger.debug(token)
            if i >= 50:
                break
    return vocab


def create_vocab_with_spl_tokens(preprocessed: list[str], debug: bool = True):
    """Create vocab from list of words."""
    all_words = sorted(set(preprocessed))
    all_words.extend([DOC_SEP_TOKEN, UNK_TOKEN])
    vocab_size = len(all_words)
    logger.info(f"Vocab size: {vocab_size}")
    vocab = {token: ii for ii, token in enumerate(all_words)}
    if debug:
        for token, i in vocab.items():
            logger.debug(token)
            if i >= 50:
                break
    return vocab

def main(url: str = THE_VERDICT_URL, filepath: str = THE_VERDICT_FILE_PATH, add_special_tokens: bool = False):
    """Build vocab from the verdict text."""
    download_text_data(url, filepath)
    raw_text = read_text_file(filepath)
    words = convert_text_to_words(raw_text)
    if add_special_tokens:
        return create_vocab_with_spl_tokens(words)
    else:
        return create_vocab(words)


if __name__ == "__main__":
    main()