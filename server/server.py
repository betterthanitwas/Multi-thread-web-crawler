from flask import Flask, request
from renderhtml import render_html

app = Flask(__name__)

@app.route('/')
def get_index():
    return app.send_static_file('index.html')

@app.route('/opensearch.xml')
def get_opensearch():
    return app.send_static_file('opensearch.xml')

@app.route('/search')
def get_query():
    fake_results = [('https://google.com', 'Google', 'These are actually fake search results.'), ('<script>', '<script>Security test', '<script>alert("Security test")')]
    return render_html(fake_results, request.args['q'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
