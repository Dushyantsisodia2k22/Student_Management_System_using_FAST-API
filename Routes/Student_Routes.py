from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from Models import Student, StudentUpdate  # Assuming models are in models.py
from Database import students_collection  # Assuming helpers in database.py

router = APIRouter()

def student_helper(student) -> dict:
   return {
        "id": str(student["_id"]),
        "name": student["name"],
        "age": student["age"],
        "address": student["address"],
    }

#Add New Student 
@router.post("/", status_code=201)
async def addStudent(student: Student):
    newStudent = await students_collection.insert_one(student.dict())
    createdStudent = await students_collection.find_one({"_id": newStudent.inserted_id})  # Fix here
    return student_helper(createdStudent)


#Get All Student
@router.get("/", response_model=List[Student])
async def getAllStudents(age: int = None, country: str = None):
    query = {}
    if age:
        query["age"] = {"$gte": age}
    if country:
        query["address.country"] = country
    
    students = await students_collection.find(query).to_list(100)
    return [student_helper(student) for student in students]

#Get Student by ID
@router.get("/{id}")
async def getStudentById(id: str):
    student = await students_collection.find_one({"_id": ObjectId(id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_helper(student)

# Update a student
@router.patch("/{id}", status_code=200)
async def updateStudent(id: str, student_update: StudentUpdate):
    update_data = {k: v for k, v in student_update.dict(exclude_unset=True).items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    result = await students_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    updated_student = await students_collection.find_one({"_id": ObjectId(id)})
    return student_helper(updated_student)


# Delete a student
@router.delete("/{id}", status_code=204)
async def deleteStudent(id: str):
    result = await students_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
