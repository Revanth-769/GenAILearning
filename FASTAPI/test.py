from fastapi import FastAPI
# this si for schema validation when we are sending data via post method inside the body
from pydantic import BaseModel
import psycopg2 
from psycopg2.extras import RealDictCursor

app = FastAPI()

#pip install psycopg2-binary
db_url= "postgresql://neondb_owner:npg_Do0OBrzCHs2M@ep-gentle-meadow-aep04fgo-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

class Students(BaseModel):
    id : int
    name: str
    age : int

def get_connection_url():
    conn = psycopg2.connect(db_url, cursor_factory=RealDictCursor)
    return conn

def save_student_to_file(data):
    with open("students.txt", "a") as f:
        f.write(f"{data.id},{data.name},{data.age}\n")

@app.post("/students/")
def create_student(stud:Students):
    data = stud
    save_student_to_file(stud)
    return {"message": "Student data saved Successfully"}


@app.post("/students/db/")
def store_student_in_db(student:Students):
    conn = get_connection_url()
    cursor = conn.cursor() # cursor is nothing but a pointer
    insert_query = "INSERT INTO student (id, name, age) VALUES (%s, %s, %s)" # 
    cursor.execute(insert_query, (student.id, student.name, student.age))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Student data inserted into db Successfully"}