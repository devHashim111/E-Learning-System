# Asynchronous E-Learning Management System (LMS) API

A high-performance, asynchronous REST and WebSocket backend for an **E-Learning Management System** built using **FastAPI** and **Fapix**.

This application implements strict Role-Based Access Control (RBAC), multi-room WebSocket communications, structured course/quiz management, and an automated asynchronous testing suite built with `pytest-asyncio`.

---

## Live Demo

A deployed instance of the application is available at:

**Live Application:**
https://lms-4475.de.deplexo.com

The deployed instance includes a frontend interface for authentication and testing the real-time WebSocket chat functionality.

### Demo Account

A dedicated testing account is available for exploring the deployed application:

```text
Email: testing@gmail.com
Password: testing123
```

After logging in, you can access the available communication rooms and test the **real-time multi-room WebSocket chat** directly through the deployed application.

> **Note:** The credentials above are provided for demonstration and testing purposes only.

### API Documentation

The deployed API provides interactive documentation through FastAPI:

* **Swagger UI:** https://lms-4475.de.deplexo.com/docs
* **ReDoc:** https://lms-4475.de.deplexo.com/redoc
* **OpenAPI Schema:** https://lms-4475.de.deplexo.com/openapi.json

The public repository contains the backend source code and this README. The deployed frontend is part of the hosted application and is not included in this repository.

---

## Key Features

### Role-Based Access Control (RBAC)

* Fine-grained permission guards (`admin`, `supervisor`, `teacher`, `student`).
* Action-level security mapping across domain endpoints.

### Core Domain Modules

* **Authentication & User Management:** JWT-based signup, login, password updates, token refreshes, and paginated user lists.
* **Courses & Enrollments:** Course catalog creation, instructor assignments, and enrollment lifecycle management.
* **Assessments:** Quiz authoring, time-bound submissions, and automated grading pipelines.
* **Real-time Communications:** WebSocket-driven multi-room chat with explicit connection state handling, messaging triggers, and live communication between connected users.

### Architectural Foundations

* **Fapix Toolkit Integration:** Rapid CRUD viewsets, CLI scaffolding, action-specific schemas, and modular routing.
* **Asynchronous Persistence:** Async Tortoise ORM with eager relation loading (`select_related`) to prevent ORM-level lazy-load validation errors.
* **Comprehensive Test Suite:** Fully automated asynchronous integration tests located in the `tests/` directory using `pytest-asyncio` and `httpx.AsyncClient`.

---

## Tech Stack & Core Dependencies

| Technology                  | Purpose                                                                                                                 |
| :-------------------------- | :---------------------------------------------------------------------------------------------------------------------- |
| **Python 3.11+**            | Core runtime environment                                                                                                |
| **FastAPI**                 | Modern, high-performance web framework                                                                                  |
| **Fapix**                   | Open-source asynchronous FastAPI toolkit for scaffolding, viewsets, WebSockets, authentication, and modular development |
| **Tortoise ORM**            | Async ORM built on top of asyncio                                                                                       |
| **Pydantic v2**             | Data validation and schema enforcement                                                                                  |
| **Pytest & Pytest-Asyncio** | Asynchronous test execution framework                                                                                   |
| **HTTPX**                   | Async HTTP client for end-to-end integration testing                                                                    |

---

## Local Setup & Installation

### Prerequisites

* Python `3.11` or higher
* Git

### 1. Clone the Repository

```bash
git clone https://github.com/devHashim111/E-learning-System.git
cd E-learning-System
```

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

> **Note:** Ensure `fapix` is installed in your virtual environment with `pip install fapix`.

### 4. Database Migrations

Run schema migrations directly through the Fapix CLI:

```bash
# Generate database migrations
fapix makemigrations

# Apply migrations
fapix migrate
```

---

## Running the Application

Start the development server using the Fapix CLI:

```bash
fapix runserver --log-level info
```

Once running, access the interactive API documentation at:

* **Swagger UI:** `http://127.0.0.1:8000/docs`
* **ReDoc:** `http://127.0.0.1:8000/redoc`
* **OpenAPI Schema:** `http://127.0.0.1:8000/openapi.json`

---

## WebSocket Communication

The application provides real-time multi-room communication through WebSocket connections.

### Production Endpoint

```text
wss://lms-4475.de.deplexo.com/communications/ws/chat/
```

### Local Development Endpoint

```text
ws://127.0.0.1:8000/communications/ws/chat/
```

The production frontend establishes the WebSocket connection automatically, allowing the chat functionality to be tested directly through the live application.

### Top-Level Payload Envelope

All WebSocket requests and responses follow a structured envelope:

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

The WebSocket layer supports real-time message delivery and connection state handling across multiple communication rooms.

---

## Running Automated Tests

All automated unit and integration tests are organized inside the `tests/` directory.

### Run the Complete Test Suite

```bash
pytest
```

### Run Tests with Verbose Output

```bash
pytest -v
```

### Run a Specific Test Module

```bash
pytest tests/test_courses.py
```

### Test Directory Structure

```text
tests/
├── test_user.py
├── test_courses.py
├── test_communications.py
├── test_assessments.py
└── conftest.py
```

* `tests/test_user.py`: Authentication, JWT generation, password hashing, and user pagination.
* `tests/test_courses.py`: Course CRUD flow, foreign key validation, and enrollment flows.
* `tests/test_communications.py`: Chat room instantiation and messaging actions.
* `tests/test_assessments.py`: Quiz publishing, submission lifecycle, and input schema verification.

---

## Project Structure

The project follows a modular FastAPI/Fapix architecture separating domain applications, routing, database configuration, migrations, and automated tests.

```text
E-learning-System/
├── apps/
├── tests/
├── migrations/
├── main.py
├── router.py
├── db_config.py
├── requirements.txt
└── README.md
```

---

## License

This project is provided as an open-source software project for educational, development, and demonstration purposes.
