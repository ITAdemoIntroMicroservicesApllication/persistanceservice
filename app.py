from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)
DATABASE = '/data/hello_world.db'  # This should match the volume in docker-compose.yml

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)')
        conn.execute("INSERT INTO messages (content) VALUES ('Hello, world!')")
        conn.commit()

@app.route('/')
def hello_world():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT content FROM messages WHERE id=1')
        message = cursor.fetchone()
        return jsonify(message=message[0])

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(host='0.0.0.0', port=80)
