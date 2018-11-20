from flask import Flask



app = Flask(__name__)


@app.route('/web_crawl/v1/get_query', methods=['GET'])
def get_query():
    return "Hello World!\n"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
