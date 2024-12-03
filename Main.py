from fastapi import FastAPI
from Routes.Student_Routes import router as Student_Routes


App = FastAPI()

App.include_router(Student_Routes, prefix="/students", tags=["Students"])

# Root endpoint
@App.get("/")
def root():
    return {"message": "Welcome to the Student Management System"}