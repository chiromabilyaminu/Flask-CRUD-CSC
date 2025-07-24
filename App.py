from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL
import re
import json
from config import Config

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')
app.config.from_object(Config)

mysql = MySQL(app)

# Simulated OCR function to extract text from image
def extract_text_from_image(image_data):
    sample_text = "HTML, CSS, Flask, MySQL DB, Read, Create, Update, Delete, Inventory"
    return re.split(',|\n', sample_text)

# Routes
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM inventory")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', inventory=data)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s)", (name, quantity))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        cur.execute("UPDATE inventory SET name = %s, quantity = %s WHERE id = %s", (name, quantity, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    cur.execute("SELECT * FROM inventory WHERE id = %s", (id,))
    data = cur.fetchone()
    cur.close()
    return render_template('update.html', inventory=data)

@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM inventory WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/api/inventory')
def get_inventory():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM inventory")
    data = cur.fetchall()
    cur.close()
    return jsonify([{"id": row[0], "name": row[1], "quantity": row[2]} for row in data])

if __name__ == '__main__':
    cur = mysql.connection.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS inventory (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), quantity INT)''')
    mysql.connection.commit()
    cur.close()
    app.run(debug=True)
