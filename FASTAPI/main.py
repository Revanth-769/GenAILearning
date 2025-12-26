# uvicorn main:app --reload

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def test():
    return{"message": "Hello, world"}

@app.get("/rev/rev2")
def test1():
    return "Revanth is great"

# parametrizing the API
students ={1:"Revanth",2:"Shravya"}

@app.get("/students/{stud_id}")
def student_function(stud_id:int): #pidentic is required to validate the schema
    return {"id": stud_id, "name":students[stud_id]}


# this is one of the way but the better approach is described below to pass the data
# @app.get("/add_students/{stud_id}/{name}")
# def add_student(stud_id:int, name:str):
#     students[stud_id] = name
#     return students

@app.get("/add_students/") # localhost:8000/add_students?stud_id=3&name=Rohit
def add_student(stud_id:int, name:str):
    students[stud_id] = name
    return students

# post method
# the difference between get and post is in post method data is ent via body
# in get method data is sent via query parameters.

from pydantic import BaseModel

class newdata(BaseModel):
    stud_id:int
    name: str

@app.post("/add_student_new_value")
def add_new_value(newdata:newdata):
    students[newdata.stud_id]=newdata.name
    return students