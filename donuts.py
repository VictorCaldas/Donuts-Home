from flask import Flask, request, jsonify
import sqlite3
from flask import json

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        return "Hello World! POST"

    else:
        return "Hello World! GET"


@app.route('/rotas', methods=['POST', 'GET'])
def api_rotas():
    conn = sqlite3.connect("rotas.db")
    cur = conn.cursor()
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'text/plain':
            return "Text Message: " + request.data
        elif request.headers['Content-Type'] == 'application/json':
            d = json.loads(request.data)
            row = (d['latitude'], d['longitude'], d['time'], d['speed'], d['rvc_name'])
            cur.execute("INSERT INTO ROTAS(LATITUDE, LONGITUDE, TIME, SPEED, RVC_NAME) VALUES (?,?,?,?,?)", row)
            conn.commit()
            conn.close()
            return "OK!"
        elif request.headers['Content-Type'] == 'application/octet-stream':
            f = open('./binary', 'wb')
            f.write(request.data)
            f.close()
            return "Binary message written!"
        else:
            return "415 Unsupported Media Type ;)"
    else:
        cur.execute("SELECT * FROM ROTAS")
        conn.close()
        json_string = json.dumps(dict(cur.fetchall()))
        return json_string


if __name__ == "__main__":
    app.run()
