import sqlite3
from datetime import datetime

conn = sqlite3.connect('steel_validation.db')
c = conn.cursor()
try:
    c.execute("INSERT OR IGNORE INTO material_categories (id, name, created_at) VALUES ('00000000-0000-0000-0000-000000000000', 'Uncategorized', ?)", (datetime.now(),))
    conn.commit()
    print("Success!")
except Exception as e:
    print(e)
conn.close()
