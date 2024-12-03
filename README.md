# Student Management API
A simple FastAPI-based backend service for managing student data, connected to MongoDB Atlas for data storage. The API provides CRUD operations for students, allowing you to create, retrieve, update, and delete student records.

## Features
* Create a new student record
* Fetch all students or filter by country and age
* Retrieve a student by ID
* Update student information (partial update supported)
* Delete a student by ID

## Technologies Used
* FastAPI: A modern, fast web framework for building APIs with Python.
* MongoDB Atlas: A cloud-based database service for storing student data.
* Motor: Async driver for MongoDB to enable non-blocking operations with FastAPI.
  
## Requirements
* Python 3.8+
* MongoDB Atlas account (for cloud-based database storage)
* Dependencies (install using pip):
> pip install fastapi motor pymongo

## Installation
1. Clone the repository:
> git clone https://github.com/Shruti7262/Student-Management-System

> cd student-management-api

2. Install required dependencies:
> pip install -r requirements.txt


3. Configure MongoDB Atlas:

* Create an account on MongoDB Atlas.
* Create a new cluster and obtain the connection URI.

4. Run the application:
> uvicorn students:app --reload


## Deployment
This application can be deployed to any cloud platform such as Render or Heroku ( [mine is deployed on Render](https://student-management-system-b3in.onrender.com/) ) .

