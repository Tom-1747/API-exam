from fastapi import FastAPI, requests, Path, HTTPException
from dataclasses import dataclass, asdict
from typing import Dict
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse

app = FastAPI()


@app.get("/hello")
def say_hello():
    return {"message": "Hello world"}

@app.get("/welcome/{name}")
def root_welcome(name: str):
    return {"message": f"Welcome {name}"}

students_db = []

class StudentModel(BaseModel):
    id: str
    firstname: str
    lastname: str
    age: int

@app.post("/students", response_model=list[StudentModel], status_code=201)
def create_student(new_student: StudentModel):
    students_db.append(new_student)
    return students_db

@app.get("/students")
def show_all_students():
    return {"total": len(students_db)}

write_students = Dict[int, dict]

@app.put("/student")
def modify_content (modify_student: StudentModel, update_student: StudentModel) :
    if StudentModel.id not in students_db:
        raise HTTPException(status_code=404, detail="The student cannot be found")
    students_db[id] = asdict(update_student)
    write_students(students_db)
    return  update_student