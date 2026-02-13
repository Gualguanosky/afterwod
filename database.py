import sqlite3
import os

DB_NAME = "afterword.db"

def connect_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            category TEXT
        )
    ''')

    # Users table for wallets
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            balance REAL DEFAULT 0.0
        )
    ''')
    
    # Updated Sales table to include user_id
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            user_id INTEGER,
            quantity INTEGER NOT NULL,
            total_price REAL NOT NULL,
            sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Payments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            method TEXT NOT NULL,
            payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    # Purchases table (Mercancía entrante / Gastos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            cost_price REAL NOT NULL,
            purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')

    # Recipes table (Composición de productos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            ingredient_id INTEGER NOT NULL,
            quantity REAL NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products (id),
            FOREIGN KEY (ingredient_id) REFERENCES products (id)
        )
    ''')

    # Migrations
    try:
        cursor.execute("ALTER TABLE sales ADD COLUMN user_id INTEGER REFERENCES users(id)")
    except Exception: pass

    try:
        # type: 'PRODUCTO' or 'INSUMO'
        cursor.execute("ALTER TABLE products ADD COLUMN type TEXT DEFAULT 'PRODUCTO'")
    except Exception: pass

    try:
        # unit: 'unid', 'ml', 'gr', etc.
        cursor.execute("ALTER TABLE products ADD COLUMN unit TEXT DEFAULT 'unid'")
    except Exception: pass

    conn.commit()
    conn.close()

# Product Functions
def add_product(name, price, stock, category="", p_type="PRODUCTO", unit="unid"):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price, stock, category, type, unit) VALUES (?, ?, ?, ?, ?, ?)", 
                   (name, price, stock, category, p_type, unit))
    conn.commit()
    conn.close()

def get_products():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

def update_product(product_id, name, price, stock, category="", p_type="PRODUCTO", unit="unid"):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET name = ?, price = ?, stock = ?, category = ?, type = ?, unit = ? WHERE id = ?", 
                   (name, price, stock, category, p_type, unit, product_id))
    conn.commit()
    conn.close()

def delete_product(prod_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=?", (prod_id,))
    conn.commit()
    conn.close()

# User Functions
def add_user(name, phone):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, phone) VALUES (?, ?)", (name, phone))
    conn.commit()
    conn.close()

def get_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def update_user_balance(user_id, amount):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

# Payment Functions
def record_payment(user_id, amount, method):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO payments (user_id, amount, method) VALUES (?, ?, ?)", 
                   (user_id, amount, method))
    cursor.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, user_id))
    conn.commit()
    conn.close()

# Recipe Functions
def add_recipe_item(product_id, ingredient_id, quantity):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO recipes (product_id, ingredient_id, quantity) VALUES (?, ?, ?)",
                   (product_id, ingredient_id, quantity))
    conn.commit()
    conn.close()

def get_recipe(product_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT r.ingredient_id, p.name, r.quantity 
        FROM recipes r
        JOIN products p ON r.ingredient_id = p.id
        WHERE r.product_id = ?
    ''', (product_id,))
    recipe = cursor.fetchall()
    conn.close()
    return recipe

def get_user_purchases(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.id, p.name, s.quantity, s.total_price, s.sale_date 
        FROM sales s 
        JOIN products p ON s.product_id = p.id
        WHERE s.user_id = ?
        ORDER BY s.sale_date DESC
    ''', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_recipe(product_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recipes WHERE product_id = ?", (product_id,))
    conn.commit()
    conn.close()

def update_ingredient_unit_cost(item_id, total_cost, quantity):
    if quantity <= 0: return
    conn = connect_db()
    cursor = conn.cursor()
    unit_cost = total_cost / quantity
    cursor.execute("UPDATE products SET price = ? WHERE id = ?", (unit_cost, item_id))
    conn.commit()
    conn.close()

def get_user_financial_history(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    # Combine Sales and Payments for a specific user
    # Columns: ID, Type (COMPRA/ABONO), Detail (Product/Method), Info (Qty/-), Amount, Date
    cursor.execute('''
        SELECT s.id, 'COMPRA' as type, p.name as detail, CAST(s.quantity AS TEXT) as info, s.total_price as amount, s.sale_date as date
        FROM sales s
        JOIN products p ON s.product_id = p.id
        WHERE s.user_id = ?
        UNION ALL
        SELECT pay.id, 'ABONO' as type, pay.method as detail, '-' as info, pay.amount as amount, pay.payment_date as date
        FROM payments pay
        WHERE pay.user_id = ?
        ORDER BY date DESC
    ''', (user_id, user_id))
    history = cursor.fetchall()
    conn.close()
    return history

def get_user_financial_totals(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(total_price) FROM sales WHERE user_id = ?", (user_id,))
    total_bought = cursor.fetchone()[0] or 0.0
    
    cursor.execute("SELECT SUM(amount) FROM payments WHERE user_id = ?", (user_id,))
    total_paid = cursor.fetchone()[0] or 0.0
    
    conn.close()
    return total_bought, total_paid

# Sale Functions
def deduct_recipe_recursive(cursor, product_id, quantity):
    """Recursively deducts ingredients if product has a recipe."""
    cursor.execute("SELECT ingredient_id, quantity FROM recipes WHERE product_id = ?", (product_id,))
    recipe = cursor.fetchall()
    
    if recipe:
        for ing_id, ing_qty in recipe:
            # Recursive call: an ingredient could itself have a recipe
            deduct_recipe_recursive(cursor, ing_id, ing_qty * quantity)
    else:
        # Base case: no recipe, deduct from stock directly
        cursor.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (quantity, product_id))

def record_sale(product_id, quantity, total_price, user_id=None, method="Efectivo"):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Process stock deduction recursively
    deduct_recipe_recursive(cursor, product_id, quantity)
    
    # Insert sale record
    cursor.execute("INSERT INTO sales (product_id, user_id, quantity, total_price) VALUES (?, ?, ?, ?)", 
                   (product_id, user_id, quantity, total_price))
    if user_id:
        cursor.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (total_price, user_id))
    conn.commit()
    conn.close()

def get_sales_history():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.id, p.name, u.name, s.quantity, s.total_price, s.sale_date 
        FROM sales s 
        JOIN products p ON s.product_id = p.id
        LEFT JOIN users u ON s.user_id = u.id
        ORDER BY s.sale_date DESC
    ''')
    sales = cursor.fetchall()
    conn.close()
    return sales

def get_combined_history():
    conn = connect_db()
    cursor = conn.cursor()
    # Combine Sales and Payments using UNION
    # We'll normalize columns: ID, Type (Sale/Payment), Entity (Product/User), Info (Qty/Method), Amount, Date
    cursor.execute('''
        SELECT s.id, 'VENTA' as type, p.name as detail, s.quantity as info, s.total_price as amount, s.sale_date as date
        FROM sales s
        JOIN products p ON s.product_id = p.id
        UNION ALL
        SELECT pay.id, 'PAGO' as type, u.name as detail, pay.method as info, pay.amount as amount, pay.payment_date as date
        FROM payments pay
        JOIN users u ON pay.user_id = u.id
        ORDER BY date DESC
    ''')
    history = cursor.fetchall()
    conn.close()
    return history

# Purchase Functions
def record_purchase(product_id, quantity, cost_price):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET stock = stock + ? WHERE id = ?", (quantity, product_id))
    cursor.execute("INSERT INTO purchases (product_id, quantity, cost_price) VALUES (?, ?, ?)", 
                   (product_id, quantity, cost_price))
    conn.commit()
    conn.close()

def get_financial_summary():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Total Sales Inflow
    cursor.execute("SELECT SUM(total_price) FROM sales")
    total_sales = cursor.fetchone()[0] or 0.0
    
    # Total Purchase Outflow
    cursor.execute("SELECT SUM(cost_price) FROM purchases")
    total_purchases = cursor.fetchone()[0] or 0.0
    
    # Sales by User (Including ID and Balance)
    cursor.execute('''
        SELECT u.id, u.name, SUM(s.total_price), u.balance
        FROM sales s 
        JOIN users u ON s.user_id = u.id 
        GROUP BY u.id
    ''')
    user_sales = cursor.fetchall()
    
    conn.close()
    return total_sales, total_purchases, user_sales

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
