import os
import psycopg
import time


DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:dev@localhost:5432/tasks"
    )

def get_connection():
    return psycopg.connect(DATABASE_URL)

def init_db():
    conn = None
    retries = 5
    while retries > 0:

        try:
            conn = get_connection()
            break
        except psycopg.OperationalError:

            retries -= 1
            print("Database not ready yet. Retrying in 2 seconds...")
            time.sleep(2)
    if conn is None:
        raise Exception("Could not connect to PostgreSQL after multiple retries.")
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

def create_task(title:str,done: bool = False):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (title, done) VALUES (%s, %s) Returning id,title,done;",(title,done))
        row = cur.fetchone()
        conn.commit()
        cur.close()

        return{
            "id": row[0],
            "title": row[1],
            "done": row[2]
        }
    finally:
        conn.close()

def update_task(task_id: int, title: str,done: bool):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING id, title, done;", (title, done, task_id)) 
        row = cur.fetchone()
        conn.commit()
        cur.close()

        if row is None:
            return None

        return{
            "id":row[0],
            "title": row[1],
            "done":row[2]
        }
    
    finally:
        conn.close()

def delete_task(task_id: int):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id = %s RETURNING id;",(task_id,)) 
        row = cur.fetchone()
        conn.commit()
        cur.close()

        return row is not None
    finally:
        conn.close()