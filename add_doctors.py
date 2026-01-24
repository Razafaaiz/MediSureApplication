import sqlite3

doctors = [
    ("Dr. A Kumar", "Cardiologist", "dr.kumar@gmail.com"),
    ("Dr. S Mehta", "Diabetologist", "dr.mehta@gmail.com"),
    ("Dr. R Sharma", "Neurologist", "dr.sharma@gmail.com"),
]

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.executemany(
    "INSERT INTO doctors (name, specialization, email) VALUES (?, ?, ?)",
    doctors
)

conn.commit()
conn.close()

print("✅ Doctors added")
