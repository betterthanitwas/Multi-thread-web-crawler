import re
from collections import Counter

excerptMaxSize = 100

wordRegex = re.compile(r"\w+")
excerptRegex = re.compile(r"(?<=\s)\S((.*)\S)?(?=\s)", re.DOTALL)

def indexText(text):
    text = " " + text + " "
    lowercaseText = text.lower()
    words = Counter(wordRegex.findall(lowercaseText))
    def getExcerpt(word):
        if len(word) > excerptMaxSize:
            return ""
        wordStartIndex = lowercaseText.index(word)
        wordEndIndex = wordStartIndex + len(word)
        padding = (excerptMaxSize - len(word)) // 2
        startIndex = max(wordStartIndex - padding, 0)
        endIndex = wordEndIndex + padding
        excerpt = excerptRegex.search(text, startIndex, endIndex)
        return excerpt.group() if excerpt else ""
    return {word: (count, getExcerpt(word)) for (word, count) in words.items()}