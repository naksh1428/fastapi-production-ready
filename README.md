# Task Management API

A RESTful Task Management application built with **Python 3**, **FastAPI**, **SQLAlchemy**, and **MySQL**. It supports full CRUD operations for tasks and users, with secure **JWT-based authentication and authorization**, database schema versioning via **Alembic**, and a clean, router-based project structure.

## Features

- **Task Management (CRUD)** — Create, read, update, and delete tasks.
- **User Management (CRUD)** — Create, read, update, and delete user accounts.
- **Authentication & Authorization** — Secure endpoints using JSON Web Tokens (JWT); protected routes require a valid access token.
- **Database Migrations** — Schema changes are managed and versioned using Alembic.
- **Modular Routing** — API endpoints are organized using FastAPI's `APIRouter` for clean URL structuring and separation of concerns.
- **Environment-based Configuration** — Sensitive credentials (DB URL, JWT secret, etc.) are managed through a `.env` file, keeping secrets out of source control.
- **ORM & Database** — SQLAlchemy is used as the ORM layer with a MySQL database backend.
- **Version Control** — Project is tracked using Git.

## Tech Stack

| Component        | Technology       |
|-------------------|------------------|
| Language          | Python 3         |
| Framework         | FastAPI          |
| ORM               | SQLAlchemy       |
| Database          | MySQL            |
| Migrations        | Alembic          |
| Auth              | JWT (OAuth2)     |
| Config Management | python-dotenv    |
| Version Control   | Git              |

## Project Structure

```
PyBase/
├── migration/                  # Alembic migration environment
│   ├── versions/              # Individual migration scripts
│   └── env.py
├── alembic.ini                 # Alembic configuration
├── src/
│   ├──                  
│   ├── tasks/
│   │   ├── __init__.py           
│   │   └── controller.py
|   |   |  
│   ├── user/
│   │   ├──              
│   │   └──          
│   ├── utils/
│   │   ├──             
│   │   └──           
├── .env                        # Environment variables (not committed)
├── main.py                     # FastAPI app entry point
├── .gitignore
├── requirements.txt
└── README.md
```

> Note: Adjust the tree above to match your actual folder layout if it differs.

## Prerequisites

- Python 3.9+
- MySQL Server running locally or remotely
- Git

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd task-management-api
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root (see `.env.example`):
   ```env
   DATABASE_URL=mysql+pymysql://<db_user>:<db_password>@<host>:<port>/<db_name>
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Create the MySQL database**
   ```sql
   CREATE DATABASE task_management_db;
   ```

6. **Run Alembic migrations**
   ```bash
   alembic upgrade head
   ```

7. **Start the application**
   ```bash
   uvicorn app.main:app --reload
   ```

8. **Access the API docs**

   - Swagger UI: `http://127.0.0.1:8000/docs`
   - ReDoc: `http://127.0.0.1:8000/redoc`

## Authentication Flow

1. Register a user via `POST /users/`.
2. Obtain a JWT access token via `POST /auth/login` (username & password).
3. Include the token in the `Authorization` header for protected routes:
   ```
   Authorization: Bearer <access_token>
   ```

## API Endpoints

### Auth
| Method | Endpoint         | Description              | Auth Required |
|--------|------------------|---------------------------|----------------|
| POST   | `/auth/login`    | Obtain JWT access token   | No             |

### Users
| Method | Endpoint         | Description         | Auth Required |
|--------|------------------|----------------------|----------------|
| POST   | `/users/`        | Create a new user    | No             |
| GET    | `/users/`        | List all users       | Yes            |
| GET    | `/users/{id}`    | Get a user by ID     | Yes            |
| PUT    | `/users/{id}`    | Update a user        | Yes            |
| DELETE | `/users/{id}`    | Delete a user         | Yes            |

### Tasks
| Method | Endpoint         | Description          | Auth Required |
|--------|------------------|------------------------|----------------|
| POST   | `/tasks/`        | Create a new task     | Yes            |
| GET    | `/tasks/`        | List all tasks        | Yes            |
| GET    | `/tasks/{id}`    | Get a task by ID      | Yes            |
| PUT    | `/tasks/{id}`    | Update a task         | Yes            |
| DELETE | `/tasks/{id}`    | Delete a task          | Yes            |

> Update this table with your exact route paths/methods if they differ.

## Database Migrations (Alembic)

Generate a new migration after changing models:
```bash
alembic revision --autogenerate -m "description of change"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback the last migration:
```bash
alembic downgrade -1
```

## Environment Variables

| Variable                      | Description                              |
|--------------------------------|-------------------------------------------|
| `DATABASE_URL`                 | MySQL connection string                  |
| `SECRET_KEY`                   | Secret key used to sign JWT tokens        |
| `ALGORITHM`                     | JWT signing algorithm (e.g., HS256)       |
| `ACCESS_TOKEN_EXPIRE_MINUTES`  | Token expiry duration in minutes          |

## Running Tests

```bash
pytest
```

## Future Improvements

- Add role-based access control (RBAC)
- Add task filtering, sorting, and pagination
- Add unit/integration test coverage
- Dockerize the application
- Add refresh token support

## License

This project is licensed under the MIT License.
