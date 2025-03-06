from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from typing import Annotated
import pytest

from ..database import Base
from ..models import Todos, Users
from ..main import app
from ..routers.auth import bcrypt_context



SQL_ALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQL_ALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass= StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
client = TestClient(app)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'yogesh', 'id': 1, 'user_role': 'admin'}



@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code",
        description="everyday",
        priority=5,
        complete=False,
        owner_id=1,
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

@pytest.fixture
def test_user():
    user = Users(
        username="yogesh",
        email="yogeshrajgure.vraj@gmail.com",
        first_name="Yogesh",
        last_name="Rajgure",
        hashed_password = bcrypt_context.hash("12345"),
        role = "admin",
        phone_number = "1111111111",
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM Users;"))
        connection.commit()
