from typing import List
from fastapi import FastAPI, HTTPException
from .schemas import Student

app = FastAPI(title="Students API", version="1.0.0")

DB: list[Student] = [Student(id=1, name="Aluno Exemplo", email="aluno@example.com")]


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/students", response_model=List[Student], summary="Listar todos os alunos")
def list_students():
    return DB


@app.get(
    "/students/{student_id}", response_model=Student, summary="Buscar aluno por ID"
)
def get_student(student_id: int):
    for s in DB:
        if s.id == student_id:
            return s
    raise HTTPException(status_code=404, detail="Student not found")


@app.post(
    "/students", response_model=Student, status_code=201, summary="Criar novo aluno"
)
def create_student(student: Student):
    if any(s.id == student.id for s in DB):
        raise HTTPException(
            status_code=409, detail="Student with this ID already exists"
        )
    DB.append(student)
    return student
