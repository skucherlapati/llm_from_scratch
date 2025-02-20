"""Toeknizer classes."""
import re
import logging
from build_vocab import convert_text_to_words

logger = logging.getLogger(__name__)
logging.basicConfig(encoding="utf-8", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# STATIC VARS
RE_RMV_PUNCT_SPACES = re.compile(r"\s+([,.?!\"()\'])")


class SimpleTokenizerV1:
    def __init__(self, vocab: dict[str, int]):
        """Init vocab."""
        self.str_to_int = vocab
        self.int_to_str = {i:s for s, i in vocab.items()}
    
    def encode(self, text: str) -> list[int]:
        """Text to token ints."""
        preprocessed = convert_text_to_words(text)
        ids = [self.str_to_int[s] for s in preprocessed]
        return ids
    
    def decode(self, ids: list[int]) -> str:
        """Token ints to texts."""
        text = " ".join([self.int_to_str[i] for i in ids])
        text = RE_RMV_PUNCT_SPACES.sub(r"\1", text)
        return text


class SimpleTokenizerV2:
    """Handles unseen words in text that are not present in vocab."""
    def __init__(self, vocab: dict[str, int], unk_token: str):
        """Init vocab."""
        self.str_to_int = vocab
        self.int_to_str = {i:s for s, i in vocab.items()}
        self.unk_token = unk_token
    
    def encode(self, text: str) -> list[int]:
        """Text to token ints."""
        preprocessed = convert_text_to_words(text)
        ids = [self.str_to_int[s] if s in self.str_to_int else self.str_to_int[self.unk_token] for s in preprocessed]
        return ids
    
    def decode(self, ids: list[int]) -> str:
        """Token ints to texts."""
        text = " ".join([self.int_to_str[i] for i in ids])
        text = RE_RMV_PUNCT_SPACES.sub(r"\1", text)
        return text



if __name__ == "__main__":
    from build_vocab import main, UNK_TOKEN, DOC_SEP_TOKEN
    vocab = main()
    tokenizer = SimpleTokenizerV1(vocab=vocab)
    text = """"It's the last he painted you know,"
           Mrs. Gisburn said with pardonable pride."""
    ids = tokenizer.encode(text)
    logger.debug(f"Input: {text}")
    logger.debug(f"Tokenized output: {ids}")
    logger.debug(f"Decoder output: {tokenizer.decode(ids)}")

    logger.debug("-"*80)
    text1 = "Hello, do you like tea?"
    text2 = "In the sunlit terraces of the palace."
    text = f" {DOC_SEP_TOKEN} ".join([text1, text2])

    vocab = main(add_special_tokens=True)
    tokenizer = SimpleTokenizerV2(vocab=vocab, unk_token=UNK_TOKEN)

    ids = tokenizer.encode(text)
    logger.debug(f"Input: {text}")
    logger.debug(f"Tokenized output: {ids}")
    logger.debug(f"Decoder output: {tokenizer.decode(ids)}")
