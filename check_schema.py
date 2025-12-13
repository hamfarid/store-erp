import sqlite3

conn = sqlite3.connect('backend/instance/inventory.db')
cursor = conn.cursor()
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='warehouses'")
result = cursor.fetchone()
if result:
    print("Warehouses schema:")
    print(result[0])
    print("\nColumns:")
    cursor.execute("PRAGMA table_info(warehouses)")
    for row in cursor.fetchall():
        print(f"  {row[1]} ({row[2]})")
else:
    print("Table 'warehouses' does not exist")
conn.close()
