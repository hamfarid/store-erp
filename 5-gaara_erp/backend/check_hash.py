import sqlite3
conn = sqlite3.connect('instance/inventory.db')
cur = conn.cursor()
cur.execute("SELECT password_hash, length(password_hash) FROM users WHERE username='admin'")
result = cur.fetchone()
print(f"Hash: {result[0]}")
print(f"Length: {result[1]}")
conn.close()
