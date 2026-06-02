import sqlite3
import os

def create_db():
    conn = sqlite3.connect('database/breached_passwords.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS breached_passwords
                 (password TEXT PRIMARY KEY)''')
    # Read sample breached passwords
    if os.path.exists('database/breached_passwords.txt'):
        with open('database/breached_passwords.txt', 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
        c.executemany('INSERT OR IGNORE INTO breached_passwords VALUES (?)',
                      [(pw,) for pw in passwords])
        conn.commit()
        print(f"Inserted {len(passwords)} breached passwords.")
    else:
        print("No breached_passwords.txt found, skipping insert.")
    conn.close()

if __name__ == '__main__':
    create_db()