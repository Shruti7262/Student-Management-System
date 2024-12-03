from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId



app = FastAPI()


MONGODB_URI = "mongodb+srv://shrutijain7262:ET91uOhMLgmsmebb@studentdata.2n47h.mongodb.net/"


client = AsyncIOMotorClient(MONGODB_URI)
db = client["students_db"]
students_collection = db["students"]



class Address(BaseModel):
    city: str
    country: str


class AddressOptional(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None


class Student(BaseModel):
    name: str
    age: int
    address: Address

class StudentGet(BaseModel):
    name: str
    age: int

class StudentListResponse(BaseModel):
    data: List[StudentGet]

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[AddressOptional] = None

class StudentCreateResponse(BaseModel):
    id: str


def str_objectid(id):
    if isinstance(id, ObjectId):
        return str(id)
    return id


@app.post("/students",
 summary='Create Students', 
 response_model=StudentCreateResponse, 
 status_code=201,
 response_description="A JSON response sending back the ID of the newly created student record.",
 description="API to create a student in the system. All fields are mandatory and required while creating the student in the system.",
 )
async def create_student(student:Student):
    student_list = student.model_dump(exclude_unset=True)
    result = await students_collection.insert_one(student_list)
    student_list['id'] = str(result.inserted_id)
    return student_list


@app.get("/students", 
         summary='List students', 
         response_model=StudentListResponse,
         response_description="sample response",
         description="An API to find a list of students. You can apply filters on this API by passing the query parameters as listed below.")
async def get_students(
  country: Optional[str] = Query(None, description= "To apply filter of country. If not given or empty, this filter should be applied."),
  age: Optional[int] = Query(None, description="Only records which have age greater than equal to the provided age should be present in the result. If not given or empty, this filter should be applied.")
  ):
  query = {}
  if country:
      query['address.country'] = country
  if age:
      query['age'] = {'$gte' : age}
  student_cursor = students_collection.find(query)
  students = [{"name": student["name"], "age": student["age"]} for student in await student_cursor.to_list(length=100)]
  return {"data": students}


@app.get("/students/{id}", summary='Fetch student', response_model=Student)
async def get_student_id(
  id: str 
  ):
     student = await students_collection.find_one({'_id': ObjectId(id)})
     if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
     student['_id'] = str_objectid(student['_id'])
     return student
    


@app.patch("/students/{id}",
  summary='Update student',
  status_code=204,
  response_description="No content",
  responses={
        204: {
            "description": "No content",
            "content": {
                "application/json": {
                    "example": {}
                }
            }
        }},
  description="API to update the student's properties based on information provided. Not mandatory that all information would be sent in PATCH, only what fields are sent should be updated in the Database.")
async def update_student(id: str, student: UpdateStudent):
    old_student_data = await students_collection.find_one({'_id': ObjectId(id)})

    if not old_student_data:
        raise HTTPException(status_code=404, detail="Student not found.")
    
    old_student_data['_id'] = str(old_student_data['_id'])

    new_student_data = student.model_dump(exclude_unset=True)

    if new_student_data.get("address"):
        address = new_student_data["address"]
        if isinstance(address, dict):
            old_student_address = old_student_data.get("address", {})
            new_student_address = {**old_student_address, **address}
            new_student_data["address"] = new_student_address

    result = await students_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": new_student_data}
        )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=500, detail="Error updating student.")
    
    return {"id" : id, **new_student_data}
        




@app.delete("/students/{id}", summary='Delete student', response_model=dict)
async def rodelete_studentot(id:str):
    result = await students_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        
        raise HTTPException(status_code=404, detail="Student not found.")
  
    return{"message": "Student deleted successfully.", "student id": id}
