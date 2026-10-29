"""Create the first admin from the server command line.

    python -m app.create_admin --email you@example.com --username mohanraj --display-name "Mohanraj"

The password is read from the ADMIN_PASSWORD env var, or prompted for (hidden).
There is deliberately no HTTP endpoint for this.
"""
import argparse
import getpass
import os
import sys

from app.core.database import get_session_factory
from app.core.errors import AppError
from app.models import Role
from app.repositories import user_repository as users
from app.schemas.auth import validate_password_strength, validate_username
from app.services import audit_service, auth_service


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Chennai Coder admin account")
    parser.add_argument("--email", required=True)
    parser.add_argument("--username", required=True)
    parser.add_argument("--display-name", required=True)
    parser.add_argument(
        "--promote",
        action="store_true",
        help="If the email already exists, promote that account to admin instead of failing",
    )
    args = parser.parse_args()

    try:
        username = validate_username(args.username)
        password = os.environ.get("ADMIN_PASSWORD")
        if not password:
            password = getpass.getpass("Admin password: ")
            if password != getpass.getpass("Confirm password: "):
                print("Passwords do not match.", file=sys.stderr)
                return 1
        validate_password_strength(password)
    except ValueError as exc:
        print(f"Invalid input: {exc}", file=sys.stderr)
        return 1

    db = get_session_factory()()
    try:
        existing = users.get_by_email(db, args.email.strip().lower())
        if existing:
            if not args.promote:
                print("An account with this email already exists. Use --promote to make it admin.", file=sys.stderr)
                return 1
            existing.role = Role.admin.value
            audit_service.record(
                db, "admin.promote_cli", entity_type="user", entity_id=str(existing.id)
            )
            db.commit()
            print(f"Promoted {existing.email} to admin.")
            return 0

        user = auth_service.register_user(
            db,
            email=args.email,
            password=password,
            username=username,
            display_name=args.display_name,
            role=Role.admin,
        )
        print(f"Created admin {user.email}.")
        return 0
    except AppError as exc:
        print(f"Error: {exc.message}", file=sys.stderr)
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
