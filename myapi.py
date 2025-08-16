from fastapi import FastAPI,Path

app = FastAPI()

students={
    1: {"name": "John Doe", "age": 20},
    2: {"name": "Jane Smith", "age": 22}
}


@app.get("/")
def index():
    return {"message": "Hello World"}

@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(..., description="The ID of the student to retrieve", gt=0)):
    return students[student_id]

@app.get("/get-by-name")
def get_by_name(name: str):
    for student in students.values():
        if student["name"] == name:
            return student
    return {"error": "Student not found"}
