from flask import Flask, jsonify, request, make_response
import sqlite3
import os

app = Flask(__name__)

# Path to SQLite database using environment variable
DATABASE = os.getenv('DATA_PATH', '/home/data') + '/your_database.db'

    

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)')
        conn.execute("INSERT INTO messages (content) VALUES ('Hello, world!')")
        conn.commit()

@app.route('/')
def hello_world():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT content FROM messages')
        messages = cursor.fetchall()
        return jsonify(messages=[message[0] for message in messages])


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
