from pathlib import Path
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from supabase import create_client
from dotenv import load_dotenv


# Load .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


# Create FastAPI application
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


# Check credentials
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL or SUPABASE_KEY is missing!")


# Connect Python to Supabase
supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# HOME
@app.get("/")
def home():
    return {
        "message": "Student API is working!"
    }


# CREATE
@app.post("/students")
def create_student(
    name: str,
    course: str,
    marks: int
):

    student = {
        "name": name,
        "course": course,
        "marks": marks
    }

    response = (
        supabase
        .table("students")
        .insert(student)
        .execute()
    )

    return {
        "message": "Student created successfully",
        "data": response.data
    }


# READ
@app.get("/students")
def get_students():

    response = (
        supabase
        .table("students")
        .select("*")
        .execute()
    )

    return {
        "message": "Students fetched successfully",
        "data": response.data
    }


# UPDATE
@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    name: str,
    course: str,
    marks: int
):

    student = {
        "name": name,
        "course": course,
        "marks": marks
    }

    response = (
        supabase
        .table("students")
        .update(student)
        .eq("id", student_id)
        .execute()
    )

    return {
        "message": "Student updated successfully",
        "data": response.data
    }


# DELETE
@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    response = (
        supabase
        .table("students")
        .delete()
        .eq("id", student_id)
        .execute()
    )

    return {
        "message": "Student deleted successfully",
        "data": response.data
    }