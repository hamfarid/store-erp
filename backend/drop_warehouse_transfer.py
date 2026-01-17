import sqlite3
import os

# Path to database
db_path = os.path.join(os.path.dirname(__file__), "src", "inventory.db")

# Connect and drop tables
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("DROP TABLE IF EXISTS warehouse_transfer_items")
    cursor.execute("DROP TABLE IF EXISTS warehouse_transfers")
    conn.commit()
    print("✅ Successfully dropped warehouse_transfer tables")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    conn.close()
