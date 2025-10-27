import pytest
from fastapi.testclient import TestClient
from app.main import app, DB
from app.schemas import Student


@pytest.fixture(autouse=True)
def reset_db():
    DB.clear()
    DB.append(Student(id=1, name="Asher Novelli", email="asher@gmail.com"))
    yield


def test_list_students_success():
    client = TestClient(app)
    r = client.get("/students")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == 1


def test_get_student_success():
    client = TestClient(app)
    r = client.get("/students/1")
    assert r.status_code == 200
    assert r.json()["email"] == "asher@gmail.com"


def test_get_student_not_found():
    client = TestClient(app)
    r = client.get("/students/999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Student not found"


def test_create_student_success():
    client = TestClient(app)
    payload = {"id": 2, "name": "Maria", "email": "maria@example.com"}
    r = client.post("/students", json=payload)
    assert r.status_code == 201
    assert r.json() == payload

    r2 = client.get("/students/2")
    assert r2.status_code == 200


def test_create_student_duplicate_id_failure():
    client = TestClient(app)

    payload = {"id": 1, "name": "Outro", "email": "outro@example.com"}
    r = client.post("/students", json=payload)
    assert r.status_code == 409
    assert r.json()["detail"] == "Student with this ID already exists"
