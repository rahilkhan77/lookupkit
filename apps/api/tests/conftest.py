import os

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SESSION_SECRET", "test-secret-not-for-prod")
os.environ.setdefault("SIGNUP_CREDITS", "20")
os.environ.setdefault("STRIPE_SECRET_KEY", "")
os.environ.setdefault("STRIPE_LIVE", "0")
os.environ.setdefault("MILLIONVERIFIER_API_KEY", "")
os.environ.setdefault("TWILIO_ACCOUNT_SID", "")
os.environ.setdefault("TWILIO_AUTH_TOKEN", "")
os.environ.setdefault("MAXMIND_LICENSE_KEY", "")

import pytest
from fastapi.testclient import TestClient

from app.db import engine
from app.main import app
from app.models import Base


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    c.cookies.clear()


def signup(client: TestClient, email: str = "dev@example.com", password: str = "password123"):
    res = client.post("/auth/signup", json={"email": email, "password": password})
    assert res.status_code == 201, res.text
    return res.json()
