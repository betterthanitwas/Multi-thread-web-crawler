import re
from collections import Counter
from unicodedata import normalize

excerpt_max_size = 150

whitespace_regex = re.compile(r"\s+")
word_regex = re.compile(r"\w+")
excerpt_regex = re.compile(r"(?<=\s)\S((.*)\S)?(?=\s)", re.DOTALL)

def index_text(text):
    text = normalize("NFKC", text)
    text = whitespace_regex.sub(" ", text).strip()
    text = " " + text + " "
    lowercase_text = text.lower()
    word_list = word_regex.findall(lowercase_text)
    words = Counter(word_list)
    word_count = len(word_list)
    def get_excerpt(word):
        if len(word) > excerpt_max_size:
            return ""
        word_start_index = lowercase_text.index(word)
        word_end_index = word_start_index + len(word)
        padding = (excerpt_max_size - len(word)) // 2
        start_index = max(word_start_index - padding, 0)
        end_index = word_end_index + padding
        excerpt = excerpt_regex.search(text, start_index, end_index)
        return excerpt.group() if excerpt else ""
    return {word: (count / word_count, get_excerpt(word)) for (word, count) in words.items()}