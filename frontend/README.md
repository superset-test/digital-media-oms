# Frontend Application

React + Vite + TypeScript + Tailwind CSS

## Development

1. Install dependencies:
   ```bash
   npm install
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env to point to your backend API
   ```

3. Start development server:
   ```bash
   npm run dev
   ```

   The app will be available at http://localhost:5173

## Build

```bash
npm run build
```

Build output will be in the `dist/` directory.

## Preview Production Build

```bash
npm run preview
```

## Tech Stack

- **React 18**: UI library
- **TypeScript**: Type safety
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework

## Project Structure

```
src/
├── assets/          # Static assets (images, fonts, etc.)
├── components/      # Reusable React components
├── pages/           # Page components
├── hooks/           # Custom React hooks
├── services/        # API client services
├── types/           # TypeScript type definitions
├── utils/           # Utility functions
├── config.ts        # Application configuration
├── App.tsx          # Root component
└── main.tsx         # Application entry point
```

## Configuration

Environment variables are prefixed with `VITE_` and accessed via `import.meta.env`:

```typescript
import.meta.env.VITE_API_URL
```

See `src/config.ts` for centralized configuration management.
