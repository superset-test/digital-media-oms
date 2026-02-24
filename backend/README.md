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

## Authentication & Authorization

### User Roles

The application supports three main user roles:

1. **Super-Admin**: Has access to all tenants, can manage tenants, and create tenant admins
2. **Tenant Admin**: Can manage users within their own tenant
3. **User**: Regular users with tenant-scoped access

### Creating a Super-Admin

Super-admins must be created via CLI command:

```bash
cd src
python -m app.cli create-super-admin \
  --email admin@system.com \
  --password YourSecurePassword123! \
  --full-name "System Administrator"
```

**Note**: Run migration `008_add_super_admin_role.sql` before creating super-admins.

### Authentication Flows

#### Super-Admin Login
```bash
POST /auth/super-admin/login
{
  "email": "admin@system.com",
  "password": "YourSecurePassword123!"
}
```

#### Tenant User Login
```bash
POST /auth/login/{tenant_slug}
{
  "email": "user@tenant.com",
  "password": "password123"
}
```

### Role-Based Access Control

#### Super-Admins Can:
- Access all tenants and their resources
- Create, read, update, and delete tenants
- Create admin users for any tenant
- Invite users to any tenant

#### Tenant Admins Can:
- Manage users within their tenant
- Invite new users to their tenant
- Access tenant-scoped resources

#### Regular Users Can:
- Access resources within their tenant
- Change their own password
- View their own profile

### User Invitation System

Admins can invite users with temporary passwords:

```bash
POST /tenants/{tenant_id}/users/invite
{
  "email": "newuser@tenant.com",
  "fullName": "New User",
  "role": "user"
}
```

Response includes a temporary password. Users must change this password on first login.

### Password Management

Users can change their password:

```bash
POST /auth/change-password
{
  "oldPassword": "current_password",
  "newPassword": "new_secure_password"
}
```

When `must_change_password` is `true` (after invitation), users are required to change their password before accessing other features.

## Default Credentials

A default admin user is created by the initial migration:

- Email: `admin@example.com`
- Password: `admin123`

**⚠️ Change this password in production!**
