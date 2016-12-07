import os

from flask import Flask, request, jsonify, json
import sqlite3

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello():
    if request.method == 'GET':
        return "Projeto Donuts!"
    else:
        return "Hello World! This is My POST"


def query_db(query, args=(), one=False):
    conn = sqlite3.connect("rotas.db")
    cur = conn.cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
              for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r


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
        else:
            return "415 Unsupported Media Type ;)"
    else:
        my_query = query_db("SELECT * FROM ROTAS")
        json_output = json.dumps(my_query)
        return json_output


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
