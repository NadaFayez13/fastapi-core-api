# FastAPI Core API (PostgreSQL + Docker Stack)

A RESTful Task Management API built with **FastAPI** and **PostgreSQL**, fully containerized using **Docker** and **Docker Compose**.

---

## 🛠️ Tech Stack & Prerequisites

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **Driver / ORM:** `psycopg` (v3) with `dict_row`
- **Environment Management:** `python-dotenv`
- **Containerization:** Docker & Docker Compose

---

## 🚀 Quick Start (Docker Compose)

The entire application stack (**FastAPI app + PostgreSQL database**) runs seamlessly with a single command:

```bash
docker compose up -d
```

### API Documentation
- Swagger UI: http://localhost:8000/docs
- API Base Endpoint: http://localhost:8000/tasks

### Stop the Application

To tear down the stack and remove the running containers:

```bash
docker compose down
```

---

## 💾 Data Persistence Verification

Data persistence across container teardowns was explicitly verified:

1. Executed `docker compose up -d` to build and launch the environment.
2. Verified the initial auto-seeded records using `GET /tasks` and Docker exec SQL queries.
3. Created new task items using `POST /tasks`.
4. Stopped and removed all running stack components using:
```bash
   docker compose down
```
5. Relaunched the stack using:
```bash
   docker compose up -d
```
6. Confirmed that all previously inserted task records persisted intact inside the mounted Docker volume:
postgres_data


This confirms that the PostgreSQL data remains persistent even after the containers are stopped and removed.

---

## 📌 API Endpoints & SQL Mapping

| Method | Endpoint      | Description             | PostgreSQL Query                                            |
|--------|---------------|--------------------------|--------------------------------------------------------------|
| GET    | `/tasks`      | Retrieve all tasks      | `SELECT * FROM tasks;`                                        |
| GET    | `/tasks/{id}` | Retrieve a task by ID   | `SELECT * FROM tasks WHERE id = %s;`                          |
| POST   | `/tasks`      | Create a new task       | `INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id;` |
| PUT    | `/tasks/{id}` | Update an existing task | `UPDATE tasks SET title = %s, done = %s WHERE id = %s;`       |
| DELETE | `/tasks/{id}` | Delete a task           | `DELETE FROM tasks WHERE id = %s;`                             |

---

## 🗄️ Database

The application uses PostgreSQL as the database system.

The database runs inside a Docker container and uses a persistent Docker volume:
postgres_data


This volume ensures that database records are preserved when the PostgreSQL container is stopped or recreated.

---

## 🐳 Docker Commands

**Start the Stack**
```bash
docker compose up -d
```

**Stop and Remove Containers**
```bash
docker compose down
```

**View Running Containers**
```bash
docker ps
```

**View Application Logs**
```bash
docker compose logs
```

**View PostgreSQL Logs**
```bash
docker compose logs postgres
```

---

## 📖 API Documentation

Once the application is running, interactive API documentation is available through Swagger UI:

http://localhost:8000/docs

Swagger UI can be used to test all available API endpoints directly from the browser.

---

## ✨ Features

- RESTful API architecture
- FastAPI backend
- PostgreSQL database integration
- CRUD operations for tasks
- Dockerized application environment
- Docker Compose orchestration
- Persistent PostgreSQL storage using Docker volumes
- Interactive Swagger API documentation
- Environment variable configuration

---

## 📂 API Operations

The API supports the following task operations:

- Create a new task
- Read all tasks
- Read a specific task by ID
- Update an existing task
- Delete a task

All database operations are executed through PostgreSQL using psycopg v3.
