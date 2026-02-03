# Task Management API

A backend-only Task Management API inspired by tools like Trello and Todoist.

Built to practice and demonstrate backend fundamentals such as REST API design, authentication, and relational database modeling.

## Tech Stack

- **Python**
- **FastAPI**
- **PostgreSQL**
- **SQLModel**
- **Alembic**
- **Pytest**

## Features

- JWT-based authentication
- Filtering tasks by status and priority
- Project roles:
  - Owner
  - Member 

### Database Design
[![task_management_api_dark.png](https://i.postimg.cc/L5shBM6x/task_management_api_dark.png)](https://postimg.cc/1nL9s2FF)

### REST API Design
- Proper HTTP methods and status codes
- Versioned API (`/api/v1`)
- Input validation with Pydantic
- Pagination with `limit` and `offset`

## Future Improvements
- Background jobs for notifications
- Rate limiting and caching
- Onboarding and password reset via email

## Running the project

### Requirements
- [uv](https://docs.astral.sh/uv/) (package manager)
- Python 3.10+
- PostgreSQL

### Setup

```bash
git clone <repo-url>
cd task-management-api/

uv sync # Install all the packages
alembic upgrade head # Run migrations
fastapi dev # Run the API in development
```

API docs available at `http://localhost:8000/docs`.
