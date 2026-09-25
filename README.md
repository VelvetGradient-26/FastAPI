# FastAPI Masterclass

My working repository for the FastAPI Masterclass course. It holds the main course project, follow-up sections built on it, and a few small standalone practice APIs. Each subproject is self-contained, with its own `pyproject.toml`, `uv.lock` and virtual environment.

## Repository Layout

```
fast-api-masterclass/
├── 1_rent-a-room/            # Main course project (sections 1-10)
├── 2_authentication/         # Authentication section (in progress)
├── 3_database-management/    # Database migrations with Alembic (in progress)
├── 4_other_projects/         # Standalone practice APIs
│   ├── BurgerPoint/
│   ├── PincodeLookup/
│   └── TheatreReviews/
└── slide-decks/              # Course slide PDFs (git-ignored)
```

## Prerequisites

- [uv](https://docs.astral.sh/uv/) for dependency and environment management
- Python 3.13+ (`1_rent-a-room` requires 3.14+; each project's `requires-python` is authoritative)

## Running a Project

Every subproject is run the same way:

```bash
cd <project-folder>
uv sync
uv run fastapi dev main.py
```

Then open `http://localhost:8000/docs` for the interactive Swagger UI (`/redoc` for ReDoc).

---

## 1. Rent-A-Room (`1_rent-a-room/`)

The main course project: an API for browsing and booking rooms. It covers the core FastAPI topics from the first ten course sections.

**Stack:** FastAPI, SQLModel, SQLite (`dev.db`, git-ignored), Pydantic v2, Alembic, aiosqlite, Ruff.

**Files**

| File | Purpose |
|------|---------|
| `main.py` | App setup (lifespan, metadata, tags), static file mount and routes |
| `models.py` | `Room` table model plus Pydantic models for cookies, headers and query params |
| `database.py` | SQLite engine, table creation, `SessionDependency` |
| `annotated.py` | Scratch script showing how `Annotated` metadata works |
| `assets/` | Static files served under `/assets` |

**Endpoints**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Localised greeting from the `language` cookie, plus the `User-Agent` header and a DB check |
| GET | `/rooms` | List all rooms |
| GET | `/rooms/search` | Search by name (`search`, 3-10 chars) with an optional `max_price` filter |
| GET | `/rooms/faq` | Check-in and check-out FAQ |
| GET | `/rooms/{id}` | Get one room, 404 if it doesn't exist |
| GET | `/preferences` | Sets the `theme` and `language` cookies |
| GET | `/example` | Dependency injection demo |

**Concepts practised:** path and query parameters, Pydantic query/cookie/header models, `Annotated` types, custom validators, static files, lifespan events, dependencies, and SQLModel sessions.

## 2. Authentication (`2_authentication/`)

Starting point for the authentication section (JWTs, password handling and so on). So far it has:

- `main.py`: FastAPI app with a lifespan hook and a `GET /` health route
- `database.py`: SQLite engine (`auth.db`), table creation and a `SessionDep` dependency

Auth models and routes are still to be added.

## 3. Database Management (`3_database-management/`)

A small sandbox for practising **database migrations with Alembic**.

- `models.py`: a `Movie` table (`id`, `title`, `in_theaters`) with a SQLAlchemy naming convention, so constraint names stay stable across migrations
- `database.py`: SQLite engine (`movies.db`)

Dependencies: `sqlmodel`, `alembic`.

---

## 4. Other Projects (`4_other_projects/`)

Small standalone APIs used to practise the fundamentals.

### BurgerPoint

A burger menu API backed by an in-memory list (`data.py`).

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Welcome message |
| GET | `/burgers` | Full menu |
| GET | `/burgers/search?category=` | Filter by category (case-insensitive), 404 if none match |
| GET | `/burgers/{id}` | Get one item |

Practises: query and path parameters, `HTTPException`, response models.

### PincodeLookup

Looks up Indian postal codes (city, district, state), singly or in bulk (up to 20). It has custom exceptions with JSON error handlers and Pydantic validation, and uses an in-memory dataset of 12 pincodes. See [`4_other_projects/PincodeLookup/README.md`](4_other_projects/PincodeLookup/README.md) for the full API reference.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/pincode/{code}` | Single lookup (400 for bad format, 404 if not found) |
| POST | `/pincode/bulk` | Bulk lookup with `found`, `not_found` and `missing` reporting |

### TheatreReviews

Just scaffolded (a `main.py` stub and dependencies: FastAPI, Uvicorn, Ruff). No routes yet.

---

## Learning Path

The course sections map onto the projects roughly like this:

| Course sections | Where it lives |
|-----------------|----------------|
| Servers, routes, path/query parameters, cookies and headers | `1_rent-a-room`, `BurgerPoint`, `PincodeLookup` |
| Databases and ORMs, database operations, app organization | `1_rent-a-room` |
| Async operations, database relationships | `1_rent-a-room` |
| Database management (migrations) | `3_database-management` |
| Authentication and authorization | `2_authentication` |

## Notes

- `*.db` files, `.venv`, `.env` and `slide-decks/` are git-ignored.
- Custom exception handling is practised in `PincodeLookup`.
- Subproject READMEs other than `PincodeLookup` are empty placeholders.
