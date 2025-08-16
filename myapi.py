from fastapi import FastAPI,Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students={
    1: {"name": "John Doe", "age": 20},
    2: {"name": "Jane Smith", "age": 22}
}

class Student(BaseModel):
    name: str
    age: int

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None


@app.get("/")
def index():
    return {"message": "Hello World"}

@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(..., description="The ID of the student to retrieve", gt=0)):
    return students[student_id]

@app.get("/get-by-name/{student_id}")
def get_by_name(*,student_id:int,name: Optional[str] = None, test: int):
    if student_id in students:
        student = students[student_id]
        if name and student["name"] != name:
            return {"error": "Name does not match"}
        return student
    else:
        return {"error": "Student not found"}

@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"error": "Student already exists"}
    students[student_id] = student.dict()
    return students[student_id]

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: StudentUpdate):
    if student_id not in students:
        return {"error": "Student not found"}
    students[student_id].update(student.dict(exclude_unset=True))
    return students[student_id]

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"error": "Student not found"}
    del students[student_id]
    return {"message": "Student deleted successfully"}