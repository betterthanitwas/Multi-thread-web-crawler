from html import escape
import re

word_regex = re.compile(r"\w+")

def render_html(results, search):
    search_words = set(word_regex.findall(search.lower()))
    bold_regex = re.compile(fr"\b({'|'.join(re.escape(escape(word)) for word in search_words)})\b", re.IGNORECASE)
    def bold_search_terms(string):
        return bold_regex.sub(r"<mark>\1</mark>", string)
    return f"""<!doctype html>
<title>CLocKPJWaRP: {escape(search)}</title>
<style>
h1 {{
	margin: 0;
}}
h2 {{
	font-size: 1.25em;
	margin-bottom: 0;
}}
p {{
	margin-top: 0;
}}
</style>
<link rel="search" type="application/opensearchdescription+xml" title="CLocKPJWaRP" href="opensearch.xml">

<h1>CLocKPJWaRP</h1>
<form action="search" method="get">
	<input type="search" name="q" value="{escape(search)}">
	<input type="submit" value="Find it">
</form>
""" + '\n'.join(f'''<h2><a href="{escape(url)}">{bold_search_terms(escape(title))}</a></h2>
<p>{bold_search_terms(escape(excerpt))}</p>''' for (url, title, excerpt) in results)
