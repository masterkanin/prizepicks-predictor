import sqlite3

# Connect to the database
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Get table info
cursor.execute("PRAGMA table_info(prediction)")
columns = cursor.fetchall()

print("Prediction table schema:")
for col in columns:
    print(f"Column {col[0]}: {col[1]} ({col[2]})")

conn.close()
