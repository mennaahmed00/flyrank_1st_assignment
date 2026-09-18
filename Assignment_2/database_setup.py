import sqlite3
connection = sqlite3.connect("tasks.db")
cursor = connection.cursor()
cursor.execute("SELECT COUNT(*) FROM tasks")
row_count = cursor.fetchone()[0]
if row_count ==0:
    print("table is empty. Inserting example tasks....")

    examples = [
        ("studying my IBM course", False),
        ("studying my flyrank assignmemnt", False),
        ("watering my flowers", False)
    ]

    cursor.executemany("INSERT INTO tasks (title,done) VALUES(?, ?)", examples)

    connection.commit()
    print("Examples inserted successfully.")
else:
    print(f"The table already has {row_count} task(s). Skipping insertion.")

connection.close()

