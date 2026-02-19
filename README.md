# Project Monorepo

Full-stack application with Python FastAPI backend and React frontend.

## Project Structure

```
.
├── backend/              # Python FastAPI service
│   ├── src/
│   │   └── app/         # Application code
│   │       ├── db/      # Database providers
│   │       ├── auth/    # Authentication utilities
│   │       ├── controllers/  # API endpoints
│   │       ├── services/     # Business logic
│   │       ├── repositories/ # Data access layer
│   │       └── domain/       # Domain models
│   ├── migrations/      # SQL migration files
│   ├── pyproject.toml   # Python dependencies
│   └── requirements.txt # Pip dependencies
│
└── frontend/            # React + Vite application
    ├── src/             # Source code
    ├── public/          # Static assets
    └── package.json     # Node dependencies
```

## Backend (Python 3.12 + FastAPI)

### Prerequisites

- Python 3.12+
- PostgreSQL 14+
- pip or uv

### Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and configure your environment variables

5. Run database migrations:
   ```bash
   psql -h localhost -U postgres -d your_database -f migrations/001_initial_schema.sql
   ```

6. Start the development server:
   ```bash
   cd src
   python -m app.main
   ```

The API will be available at http://localhost:8000

### API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Frontend (React + Vite + Tailwind CSS)

### Prerequisites

- Node.js 18+
- npm or yarn

### Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Copy `.env.example` to `.env` and configure your environment variables

4. Start the development server:
   ```bash
   npm run dev
   ```

The application will be available at http://localhost:5173

### Build for Production

```bash
npm run build
```

## Development

### Backend Architecture

The backend follows a layered architecture:

- **Controllers**: FastAPI routers handling HTTP requests/responses
- **Services**: Business logic layer (singletons)
- **Repositories**: Data access layer (singletons, raw SQL)
- **Domain**: Pure data classes representing business entities

See `CLAUDE.md` for detailed conventions.

### Frontend Structure

- Uses React with TypeScript
- Styled with Tailwind CSS
- Vite for fast development and building

## License

Proprietary