import sqlite3

# Connect to the database
conn = sqlite3.connect("app.db")
cursor = conn.cursor()

# Create the users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    sex TEXT NOT NULL,
    age INTEGER NOT NULL,
    experience INTEGER NOT NULL
)
""")

# Save changes and close the connection
conn.commit()
conn.close()
