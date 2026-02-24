"""CLI commands for administrative tasks."""

import argparse
import asyncio
import sys

from app.db.postgres import PostgresProvider
from app.services.user_service import UserService


async def create_super_admin_command(email: str, password: str, full_name: str):
    """Create a super-admin user via CLI."""
    print(f"Creating super-admin user: {email}")

    # Initialize database connection
    postgres = PostgresProvider()
    try:
        await postgres.init()

        # Create super-admin
        user_service = UserService()
        try:
            user = await user_service.create_super_admin(email, password, full_name)
            print(f"✓ Super-admin user created successfully!")
            print(f"  Email: {user.email}")
            print(f"  Name: {user.full_name}")
            print(f"  ID: {user.id}")
            return 0
        except Exception as e:
            error_msg = str(e)
            if "duplicate key" in error_msg.lower() or "unique constraint" in error_msg.lower():
                print(f"✗ Error: A user with email '{email}' already exists.", file=sys.stderr)
            else:
                print(f"✗ Error creating super-admin: {error_msg}", file=sys.stderr)
            return 1
    finally:
        await postgres.shutdown()


async def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Admin CLI for managing the application")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # create-super-admin command
    create_sa_parser = subparsers.add_parser(
        "create-super-admin", help="Create a new super-admin user"
    )
    create_sa_parser.add_argument("--email", required=True, help="Super-admin email address")
    create_sa_parser.add_argument("--password", required=True, help="Super-admin password")
    create_sa_parser.add_argument("--full-name", required=True, help="Super-admin full name")

    args = parser.parse_args()

    if args.command == "create-super-admin":
        exit_code = await create_super_admin_command(args.email, args.password, args.full_name)
        sys.exit(exit_code)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
