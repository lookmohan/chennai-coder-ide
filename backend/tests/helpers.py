from app.models import User


PASSWORD = "correct-horse-9"


def register(client, email="student@example.com", username="student_one", password=PASSWORD):
    return client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "username": username,
            "display_name": "Student One",
        },
    )


def login(client, email="student@example.com", password=PASSWORD):
    return client.post("/api/v1/auth/login", json={"email": email, "password": password})


def set_user_field(session_factory, email: str, **fields) -> None:
    db = session_factory()
    try:
        user = db.query(User).filter(User.email == email).one()
        for key, value in fields.items():
            setattr(user, key, value)
        db.commit()
    finally:
        db.close()
