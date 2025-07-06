from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# Connect to Postgres
conn = psycopg2.connect(
    dbname="grocerydb",
    user="admin",
    password="adminpass",
    host="postgres-service",  # Use "localhost" on Linux
    port="5432"
)
cur = conn.cursor()

# Create table if not exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        price FLOAT NOT NULL
    );
""")
conn.commit()

@app.route('/')
def index():
    cur.execute("SELECT id, name, price FROM products;")
    products = cur.fetchall()
    return render_template('index.html', products=products)

@app.route('/add', methods=['POST'])
def add_product():
    name = request.form['name']
    price = request.form['price']
    cur.execute("INSERT INTO products (name, price) VALUES (%s, %s);", (name, price))
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

