"""
pytest fixtures for the Task Management API tests.

Provides:
- Test database session
- Test client
- Sample data factories
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from api.main import app
from api.database import get_db


@pytest.fixture(name="engine")
def engine_fixture():
    """Create in-memory SQLite engine for testing."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine


@pytest.fixture(name="session")
def session_fixture(engine):
    """Create database session for testing."""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create test client with database dependency override."""
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# Sample data factories

@pytest.fixture
def sample_subject_data():
    """Sample subject creation data."""
    return {
        "name": "Data Structures and Algorithms",
        "description": "Fundamental computer science concepts"
    }


@pytest.fixture
def sample_topic_data():
    """Sample topic creation data."""
    return {
        "name": "Binary Search Trees",
        "description": "Tree-based data structure for efficient searching"
    }


@pytest.fixture
def sample_task_data():
    """Sample task creation data."""
    return {
        "material_type": "quiz",
        "topic_name": "Binary Search Trees",
        "input_params": {
            "clos": [
                "Analyze BST structure and properties",
                "Evaluate BST operation efficiency"
            ],
            "time_duration": 60,
            "total_questions": 5,
            "complexity_levels": ["Apply", "Analyze"]
        }
    }


@pytest.fixture
def created_subject(client, sample_subject_data):
    """Create and return a subject."""
    response = client.post("/api/subjects", json=sample_subject_data)
    return response.json()


@pytest.fixture
def created_topic(client, created_subject, sample_topic_data):
    """Create and return a topic."""
    data = {**sample_topic_data, "subject_id": created_subject["id"]}
    response = client.post("/api/topics", json=data)
    return response.json()
