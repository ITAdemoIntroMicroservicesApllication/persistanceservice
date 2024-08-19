from flask import Flask, jsonify, request, make_response
import sqlite3
import os

app = Flask(__name__)
DATABASE = '/data/hello_world.db'

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

@app.route('/add_message', methods=['POST'])
def add_message():
    content = request.json.get('content')
    if not content:
        return make_response(jsonify({"error": "Content is required"}), 400)
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (content) VALUES (?)", (content,))
        conn.commit()
        new_id = cursor.lastrowid
        return jsonify({"id": new_id, "content": content})

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(host='0.0.0.0', port=80)
