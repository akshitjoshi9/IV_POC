import sys
import os
import uuid
import getpass
from datetime import datetime, timezone
from sqlmodel import select

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.models import User
from core.db import get_session_ml_engine
from core.auth import get_password_hash


def create_user(username: str, email: str, password: str, first_name: str, last_name: str):
    """This script is used to create users."""

    session_generator = get_session_ml_engine()
    session = next(session_generator)

    # Check if email already exists
    existing_user = session.exec(select(User).where(User.email == email)).first()
    if existing_user:
        print(f"Error: Email '{email}' is already registered.")
        return
    
    hashed_pwd = get_password_hash(password)

    user = User(
        id=uuid.uuid4(),
        username=username,
        email=email,
        hashed_password=hashed_pwd,
        first_name=first_name,
        last_name=last_name,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        is_active=True
    )

    session.add(user)
    session.commit()
    print(f"User '{username}' created successfully.")

if __name__ == "__main__":
    print("=== Create User ===")
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = getpass.getpass("Enter password: ")
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")

    create_user(username, email, password, first_name, last_name)
