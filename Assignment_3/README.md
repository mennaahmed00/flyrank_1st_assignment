# Assignment 3: Task Manager API (FastAPI + PostgreSQL + Docker Compose)

A containerized Task Management API built with FastAPI and PostgreSQL using raw SQL via `psycopg`.

## Quick Start

Run the entire application stack with a single command:

```bash
cp .env.example .env
docker compose up --build
```

The API will be available at `http://localhost:8000`.

---

## Environment Variables

| Variable | Description | Example Default |
| :--- | :--- | :--- |
| `POSTGRES_USER` | PostgreSQL superuser | `postgres` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `dev` |
| `POSTGRES_DB` | Default database name | `tasks` |
| `DATABASE_URL` | Full connection string | `postgresql://postgres:dev@db:5432/tasks` |

---

## API Endpoints Table

| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/tasks` | Retrieve all tasks | `200 OK` |
| `GET` | `/tasks/{id}` | Retrieve a task by ID | `200 OK` / `404 Not Found` |
| `POST` | `/tasks` | Create a new task | `201 Created` / `400 Bad Request` |
| `PUT` | `/tasks/{id}` | Update an existing task | `200 OK` / `404 Not Found` |
| `DELETE` | `/tasks/{id}` | Delete a task by ID | `204 No Content` / `404 Not Found` |

---

## Example Usage

### Get all tasks
```bash
curl -i http://localhost:8000/tasks
```

### Response
```json
HTTP/1.1 200 OK
content-type: application/json

[
  {"id": 1, "title": "Setup PostgreSQL Container", "done": true},
  {"id": 2, "title": "Configure Environment Variables", "done": true},
  {"id": 3, "title": "Complete Assignment 3", "done": false}
]
```

---

## Database Proof

Below is the database verification showing the `tasks` table schema and seeded rows:

```sql
docker exec -it assignment_3-db-1 psql -U postgres -d tasks -c "\dt"
docker exec -it assignment_3-db-1 psql -U postgres -d tasks -c "SELECT * FROM tasks;"
```