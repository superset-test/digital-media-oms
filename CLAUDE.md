NEVER read .env files or any files containing secrets. Ask the user to describe the contents instead.

Always explore the project structure before creating new files — understand the layout first.

## Planning Rules

IMPORTANT: When creating implementation plans, NEVER write vague steps like "create a repository" or "add a service layer." Every step in the plan MUST reference the specific conventions from this file by name. For example:
- NOT: "Create a users repository"
- YES: "Create `UserRepository(metaclass=SingletonMeta)` with async methods taking `connection` as first arg, raw SQL with `$1` params, returning `User` dataclass via `from_db_row(row)` with position-based unpacking"
- NOT: "Add a service for users"
- YES: "Create `UserManagementService(metaclass=SingletonMeta)`, instantiate `UserRepository` and `PostgresProvider` in `__init__`, each method acquires connection via `get_default_connection()`, wraps writes in `async with connection.transaction()`, releases in `finally`"
- NOT: "Create API endpoints"
- YES: "Create `controllers/users.py` with module-level `APIRouter`, `Depends(get_current_user)` for auth, `_user_from_request()` private function for Pydantic→domain conversion, service instantiated per handler, responses via `UserResponse.from_domain()`"

The plan is what drives implementation in accept-all mode. If a convention isn't spelled out in the plan, it won't end up in the code.

## Python/FastAPI Backend Conventions

When building FastAPI backends, follow this layered architecture. When starting a new project, create the foundational pieces first, then build resources on top.

### Foundation (create these first in any new project)

**`utils.py` — SingletonMeta metaclass:**
```python
class SingletonMeta(type):
    _instances: dict[type, Any] = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
```

**`db/postgres.py` — PostgresProvider (singleton, asyncpg pool):**
- Reads POSTGRES_DB_USER, POSTGRES_DB_PASSWORD, POSTGRES_DB_HOST, POSTGRES_DB_PORT, POSTGRES_DATABASE, POSTGRES_SCHEMA, POSTGRES_SSL_MODE from env vars
- `async init()` creates `asyncpg.create_pool()` with `server_settings={'search_path': schema}` and JSONB codec via `set_type_codec`
- `async get_default_connection()` → acquires from pool (lazy-inits if needed)
- `async release_connection(connection)` → returns to pool
- `async shutdown()` → closes pool
- Used in FastAPI lifespan: init on startup, shutdown on teardown

**`controllers/models/base.py` — AppBaseModel:**
```python
def to_lower_camel(string: str) -> str:
    words = string.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])

class AppBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_lower_camel,
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
    def dict(self, *args, **kwargs) -> dict[str, Any]:
        kwargs.pop("exclude_none", None)
        return super().model_dump(*args, exclude_none=True, **kwargs)
```

**`auth/password.py` — PasswordManager:** Static methods `get_password_hash(password) -> str` and `verify_password(plain, hashed) -> bool` using bcrypt with 12 rounds.

### Layers: Controller → Service → Repository

- **Repository**: Singleton via SingletonMeta. All methods async, take `connection` as first arg. Raw SQL with `$1, $2` params. Return domain dataclasses via `from_db_row(row)` (position-based unpacking). Error handling: try/except, `traceback.print_exc()`, re-raise.
- **Service**: Singleton via SingletonMeta. Instantiates own repositories and PostgresProvider in `__init__`. Each method: acquire connection → try (transaction for writes) → finally release. Business logic lives here.
- **Controller**: FastAPI `APIRouter` at module level. `Depends()` for auth only. Instantiates service singletons in each handler. Private `_thing_from_request()` functions convert Pydantic → domain.

### Domain Models
`@dataclass` classes. `from_db_row(row)` static factory with position-based row unpacking. `clone_with_id()` for post-INSERT copies. Optional fields default to `None`.

### Pydantic Request/Response Models
Inherit AppBaseModel. Every field uses `Field(description=..., examples=[...])`. Response models have `@staticmethod from_domain(obj)`. UUIDs → `str` in responses. Collection responses: wrapper with `list[ItemResponse]` + `num_records: int`.

### Auth
JWT via python-jose. HTTPBearer security scheme. Dependency functions: `get_current_user`, `ensure_current_user_super_admin`. Fine-grained checks via `verify_*()` utility functions called in handlers.

### App Server
`AppServer.get_app()` static method returns FastAPI app. Lifespan context manager for PostgresProvider init/shutdown. CORSMiddleware. Routers registered via `app.include_router(resource.router, tags=[...])`.

### Rules
- Always explore the project structure before creating new files — understand the layout first
- In monorepo/workspace projects, put foundational pieces (SingletonMeta, PostgresProvider, AppBaseModel, PasswordManager) in the shared/common package, not in each service
- Never put SQL in services or controllers
- Never put business logic in controllers or repositories
- Never use an ORM or query builder — raw SQL only
- Never return raw dicts from endpoints — always Pydantic response models
- Services manage their own connections — never pass connections via Depends()
- Routes follow `/v1/<resource>/{id}/<action>` pattern
