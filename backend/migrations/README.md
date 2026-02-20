# Database Migrations

This directory contains SQL migration files for the database schema.

## Running Migrations

Migrations should be run in numerical order. You can run them manually using `psql` or your preferred PostgreSQL client:

```bash
psql -h localhost -U postgres -d your_database -f 001_initial_schema.sql
```

## Migration Naming Convention

Migrations follow the pattern: `XXX_description.sql`

- `XXX`: Three-digit number (001, 002, 003, etc.)
- `description`: Brief description of what the migration does

## Creating New Migrations

1. Create a new file with the next available number
2. Add your SQL DDL statements
3. Include both `UP` migration (create/alter) and comments for rollback instructions
4. Test the migration on a local database before applying to production

## Current Migrations

- `001_initial_schema.sql`: Creates initial users table and related indexes/triggers
