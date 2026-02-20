# Backend Service

FastAPI backend service with PostgreSQL using asyncpg.

## Architecture

This backend follows a layered architecture pattern:

```
Controllers (FastAPI routers)
    ↓
Services (Business logic, singletons)
    ↓
Repositories (Data access, raw SQL, singletons)
    ↓
PostgreSQL Database
```

### Key Components

- **`utils.py`**: Contains `SingletonMeta` metaclass for singleton pattern
- **`db/postgres.py`**: `PostgresProvider` manages asyncpg connection pool
- **`auth/password.py`**: `PasswordManager` for bcrypt password hashing
- **`controllers/models/base.py`**: `AppBaseModel` for Pydantic models with camelCase
- **`domain/`**: Dataclasses representing business entities
- **`repositories/`**: Data access layer with raw SQL queries
- **`services/`**: Business logic layer
- **`controllers/`**: FastAPI routers for HTTP endpoints

## Development Setup

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. Start PostgreSQL (using Docker):
   ```bash
   docker-compose up -d postgres
   ```

5. Run migrations:
   ```bash
   psql -h localhost -U postgres -d app_db -f migrations/001_initial_schema.sql
   ```

6. Run the application:
   ```bash
   cd src
   python -m app.main
   ```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## Conventions

See the root `CLAUDE.md` file for detailed coding conventions including:

- Repository pattern (singleton, async, raw SQL)
- Service pattern (singleton, connection management)
- Controller pattern (FastAPI routers, Pydantic models)
- Domain model pattern (dataclasses with `from_db_row`)

## Testing

```bash
pytest
```

## Default Credentials

A default admin user is created by the initial migration:

- Email: `admin@example.com`
- Password: `admin123`

**⚠️ Change this password in production!**
