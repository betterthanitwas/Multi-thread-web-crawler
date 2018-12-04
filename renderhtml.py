from html import escape
import re

def render_html(results, search, search_words):
    bold_regex = re.compile(fr"\b({'|'.join(re.escape(escape(word)) for word in search_words)})\b", re.IGNORECASE)
    def bold_search_terms(string):
        return bold_regex.sub(r"<mark>\1</mark>", string)
    return f"""<!doctype html>
<title>CLocKPJWaRP: {escape(search)}</title>
<style>
h1 {{
	margin: 0;
	font-family: monaco;
}}
h2 {{
	font-size: 1.25em;
	margin-bottom: 0;
}}
p {{
	margin-top: 0;
}}

input{{
	border-radius: 15px;
	border: solid;
	border-width: thin;
}}

#button{{
	background-color: blue;
	color: white;
}}

</style>
<link rel="search" type="application/opensearchdescription+xml" title="CLocKPJWaRP" href="opensearch.xml">

<h1>CLocKPJWaRP</h1>
<form action="search" method="get">
	<input type="search" name="q" value="{escape(search)}">
	<input type="submit" value="Find it" id="button">
</form>
""" + '\n'.join(f'''<h2><a href="{escape(str(url, encoding="UTF-8"))}">{bold_search_terms(escape(str(title, encoding="UTF-8")))}</a></h2>
<p>{bold_search_terms(escape(str(excerpt, encoding="UTF-8")))}</p>''' for (url, title, excerpt) in results)
