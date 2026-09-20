# Asynchronous E-Learning Management System (LMS) API

A high-performance, asynchronous REST and WebSocket backend for an E-Learning Management System built using **FastAPI** and **Fapix**.

This application implements strict Role-Based Access Control (RBAC), multi-room WebSocket communications, structured course/quiz management, and an automated testing suite built on `pytest-asyncio`.

---

## Key Features

### Role-Based Access Control (RBAC)
- Fine-grained permission guards (`admin`, `supervisor`, `teacher`, `student`).
- Action-level security mapping across domain endpoints.

### Core Domain Modules
- **Authentication & User Management:** JWT-based signup, login, password updates, token refreshes, and paginated user lists.
- **Courses & Enrollments:** Course catalog creation, instructor assignments, and enrollment lifecycle management.
- **Assessments:** Quiz authoring, time-bound submissions, and automated grading pipelines.
- **Real-time Communications:** WebSocket-driven chat rooms with explicit connection state handling and messaging triggers.

### Architectural Foundations
- **Fapix Toolkit Integration:** Rapid CRUD viewsets, CLI scaffolding, action-specific schemas, and modular routing.
- **Asynchronous Persistence:** Async Tortoise ORM with eager relation loading (`select_related`) to prevent ORM-level lazy-load validation errors.
- **Comprehensive Test Suite:** Fully automated async integration tests located in the `tests/` directory using `pytest-asyncio` and `httpx.AsyncClient`.

---

## Tech Stack & Core Dependencies

| Technology | Purpose |
| :--- | :--- |
| **Python 3.11+** | Core runtime environment |
| **FastAPI** | Modern, high-performance web framework |
| **Fapix** | Open-source asynchronous FastAPI toolkit for scaffolding, viewsets, websockets, authentication |
| **Tortoise ORM** | Async ORM built on top of asyncio |
| **Pydantic v2** | Data validation and schema enforcement |
| **Pytest & Pytest-Asyncio** | Asynchronous test execution framework |
| **HTTPX** | Async HTTP client for end-to-end integration testing |

---

## Local Setup & Installation

### Prerequisites
- Python `3.11` or higher
- Git

### 1. Clone the Repository
```bash
git clone [https://github.com/devHashim111/E-learning-System.git](https://github.com/devHashim111/E-learning-System.git)
cd E-learning-System

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv enviro

# Activate environment (Linux/macOS)
source enviro/bin/activate

# Activate environment (Windows PowerShell)
# .\enviro\Scripts\Activate.ps1

```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt

```

> **Note:** Ensure `fapix` is installed in your virtual environment via `pip install fapix`.

### 4. Database Migrations

Run schema migrations directly via Fapix CLI:

```bash
# Generate database migrations
fapix makemigrations

# Apply migrations to database
fapix migrate

```

---

## Running the Application

Start the development server using the Fapix CLI:

```bash
fapix runserver --log-level info

```

Once running, access the interactive API documentations at:

* **Swagger UI:** `http://127.0.0.1:8000/docs`
* **ReDoc:** `http://127.0.0.1:8000/redoc`
* **OpenAPI Schema:** `http://127.0.0.1:8000/openapi.json`

---

## WebSocket Communication Protocol

Real-time chat rooms operate over standard WebSocket connections (`ws://127.0.0.1:8000/ws/chat`).

### Top-Level Payload Envelope

All WebSocket requests and responses follow a strict envelope structure:

```json
{
  "action": "send_message",
  "request_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "timestamp": "2026-09-19T21:00:00Z",
  "payload": {
    "course_id": "2285fe7c-44fe-44d9-b134-9fd80584210a",
    "content": "Welcome to the course discussion."
  }
}

```

---

## Running Automated Tests

All automated unit and integration tests are organized inside the `tests/` directory.

```bash
# Run all test suites inside tests/
pytest

# Run tests with verbose output
pytest -v

# Run a specific test module
pytest tests/test_courses.py

```

### Test Directory Structure (`tests/`)

* `tests/test_user.py`: Authentication, JWT generation, password hashing, and user pagination.
* `tests/test_courses.py`: Course CRUD flow, foreign key validation, and enrollment flows.
* `tests/test_communications.py`: Chat room instantiation and messaging actions.
* `tests/test_assessments.py`: Quiz publishing, submission lifecycle, and input schema verification.

```

```
