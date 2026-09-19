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