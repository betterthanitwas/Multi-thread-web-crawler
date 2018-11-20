class DataStore:
    # (url, title, Dict<word, (wordCount, excerpt)>) -> Void
    def indexPage(url, title, words): pass

    # List<word> -> List<(url, title, excerpt)>
    def search(words): pass
