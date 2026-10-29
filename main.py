from fastapi import FastAPI
import sqlite3
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#static files
app.mount("/static", StaticFiles(directory="static"), name="static")


#database :
conn = sqlite3.connect("mydatabae.db" , check_same_thread=False)
cusor = conn.cursor()

cusor.execute('''CREATE TABLE if not exists students(id integer primary key  , 
            name text  not null,
            age intger not null) ''')


@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.get("/students")
def display():
    cusor.execute('''SELECT * FROM students''')
    data = cusor.fetchall()
    return data


#namw
@app.get("/{name}")
def show_id(name: str):
    cusor.execute(''' SELECT * FROM students WHERE name = ?''' , (name,))
    student = cusor.fetchone()
    return student


@app.post("/product")
def add_student(name:str , age:int):
    cusor.execute('''
    INSERT INTO students (name , age) 
    VALUES (? , ?)
    ''' , (name , age))
    conn.commit()
    return {"add student": "Sucsess adding student"}


@app.delete("/delete/{id}")
def delete_student(id:int):
    cusor.execute('''DELETE FROM students WHERE id = ?''' , (id,))
    conn.commit()
    return {"delete student": "Sucsess deleting student"}

@app.put("/update/{id}")
def update_student(id:int , name:str , age:int):    
    cusor.execute('''UPDATE students SET name = ? , age = ? WHERE id = ?''' , (name , age , id))
    conn.commit()
    return {"update student": "Sucsess updating student"}
