from flask import Flask, request
import sqlite3

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        return "Hello World! POST"

    else:
        return "Hello World! GET"


if __name__ == "__main__":
    app.run()
