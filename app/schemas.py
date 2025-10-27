from pydantic import BaseModel, EmailStr


class Student(BaseModel):
    id: int
    name: str
    email: EmailStr
