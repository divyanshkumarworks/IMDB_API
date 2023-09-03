import sqlite3

try:
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT CHECK (role IN ('Admin', 'User'))
        );
    ''')

    conn.commit()
    print("tables created successfully")
except Exception as error:
    print(error)
finally:
    conn.close()