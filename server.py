from flask import Flask, request
from datastore import DataStore
from renderhtml import render_html
import re

data_store = DataStore('config.ini')

app = Flask(__name__)

@app.route('/')
def get_index():
    return app.send_static_file('index.html')

@app.route('/opensearch.xml')
def get_opensearch():
    return app.send_static_file('opensearch.xml')

word_regex = re.compile(r"\w+")

@app.route('/search')
def get_query():
    search_words = set(word_regex.findall(request.args['q'].lower()))
    results = data_store.search(search_words)
    return render_html(results, request.args['q'], search_words)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
