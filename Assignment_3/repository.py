import os
import psycopg

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:dev@localhost:5432/tasks"
    )

def get_connection():
    return psycopg.connect(DATABASE_URL)

def init_db():
    conn = get_connection()

    try:
        cur = conn.cursor()
        cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                        id SERIAL PRIMARY KEY,
                        title TEXT NOT NULL,
                        done BOOLEAN NOT NULL DEFAULT FALSE
                );
            """)

        cur.execute("SELECT COUNT(*) FROM tasks;")
        count = cur.fetchone()[0]

        if count == 0:
            cur.execute(""" 
                INSERT INTO tasks (title, done) VALUES
                ('Setup PostgreSQL Container', true),
                ('Configure Environment Variables', true),
                ('Complete Assignment 3', false);
        """)
        conn.commit()
        cur.close()
    finally:
        # Always close connection when finished
        conn.close()


def get_all_tasks():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, title, done FROM tasks ORDER BY id ASC;")
        rows = cur.fetchall()
        cur.close()

        tasks = []
        for row in rows:
            tasks.append({
                "id": row[0],
                "title": row[1],
                "done": row[2]
            })
        return tasks
    finally:
        conn.close()

        
def get_task_by_id(task_id: int):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, title, done FROM tasks WHERE id = %s;", (task_id,))
        row = cur.fetchone()
        cur.close()

        if row is None:
            return None

        return{
            "id": row[0],
            "title": row[1],
            "done": row[2]
            }
    finally:
        conn.close()