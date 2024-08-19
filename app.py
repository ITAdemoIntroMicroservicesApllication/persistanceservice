import sqlite3
from flask import Flask, request, jsonify, g

DATABASE = 'products.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                brand TEXT NOT NULL,
                description TEXT NOT NULL,
                price REAL NOT NULL,
                title TEXT NOT NULL
            )
        ''')
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    brand = data['brand']
    description = data['description']
    price = data['price']
    title = data['title']
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO products (brand, description, price, title) VALUES (?, ?, ?, ?)',
        (brand, description, price, title)
    )
    db.commit()
    id = cursor.lastrowid
    new_product = {'id': id, 'brand': brand, 'description': description, 'price': price, 'title': title}
    return jsonify(new_product), 201

@app.route('/products', methods=['GET'])
def get_products():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    products_list = [{'id': row[0], 'brand': row[1], 'description': row[2], 'price': row[3], 'title': row[4]} for row in products]
    return jsonify(products_list), 200

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (id,))
    product = cursor.fetchone()
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    product_dict = {'id': product[0], 'brand': product[1], 'description': product[2], 'price': product[3], 'title': product[4]}
    return jsonify(product_dict), 200

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    brand = data.get('brand')
    description = data.get('description')
    price = data.get('price')
    title = data.get('title')
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (id,))
    product = cursor.fetchone()
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
        
    cursor.execute(
        'UPDATE products SET brand = ?, description = ?, price = ?, title = ? WHERE id = ?',
        (brand, description, price, title, id)
    )
    db.commit()
    updated_product = {'id': id, 'brand': brand, 'description': description, 'price': price, 'title': title}
    return jsonify(updated_product), 200

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (id,))
    product = cursor.fetchone()
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
        
    cursor.execute('DELETE FROM products WHERE id = ?', (id,))
    db.commit()
    return '', 204

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
