# FastAPI Core API with SQLite Integration

A RESTful Task Management API built with **FastAPI** and **SQLite3**, migrated from in-memory array storage to persistent database storage.

---

## 🛠️ Tech Stack & Setup

- **Framework:** FastAPI
- **Database:** SQLite3
- **Data Validation:** Pydantic

### Prerequisites & Installation
1. Install dependencies:
   ```bash
   pip install fastapi uvicorn pydantic

2. Run the server in development mode:
   ```bash
   fastapi dev server.py

   
## 📌 API Endpoints & Database Mapping

| Method | Endpoint | Description | SQL Query Executed |
| :--- | :--- | :--- | :--- |
| `GET` | `/tasks` | Retrieve all tasks | `SELECT * FROM tasks` |
| `GET` | `/tasks/{id}` | Retrieve a task by ID | `SELECT * FROM tasks WHERE id = ?` |
| `POST` | `/tasks` | Create a new task | `INSERT INTO tasks (title, done) VALUES (?, ?)` |
| `PUT` | `/tasks/{id}` | Update an existing task | `UPDATE tasks SET title = ?, done = ? WHERE id = ?` |
| `DELETE`| `/tasks/{id}` | Delete a task | `DELETE FROM tasks WHERE id = ?` |