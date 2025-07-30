import sqlite3

conn = sqlite3.connect("project_19_sql_querying_agent/sample.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT
);
""")

cursor.execute("""
INSERT INTO users (name, email) VALUES
    ('John Doe', 'john.doe@example.com'),
    ('Jane Smith', 'jane.smith@example.com');
""")

cursor.execute("""
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price REAL
);
""")

cursor.execute("""
INSERT INTO products (name, price) VALUES
    ('Laptop', 1200.00),
    ('Smartphone', 800.00);
""")

conn.commit()
conn.close()
