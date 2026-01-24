import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("ALTER TABLE appointments ADD COLUMN zoom_link TEXT")

conn.commit()
conn.close()

print("✅ Zoom link column added")
