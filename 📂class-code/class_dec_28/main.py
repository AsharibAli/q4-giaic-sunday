from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr

# create fastapi app instance
app = FastAPI(
title="Learning FastAPI",
description="A simple API for learning",
version="1.0.0"
)

# simple api endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"} 

# Path Parameters
@app.get("/users/{user_id}")
def get_user(user_id: int):
    """Get a specific user by their ID"""
    # user_id is extracted from the URL
    # GET /users/42 → user_id = 42
    return {"user_id": user_id}     

# Query Parameters
@app.get("/users/{user_id}")
def get_users(
    skip: int = 0, # Default value = optional
    limit: int = 10, # Pagination
    active: bool = True # Filter
):
    """Get users with optional filtering"""
    # GET /users/?skip=0&limit=5&active=true
    return {
        "skip": skip,
        "limit": limit,
        "active_only": active
    } 

# Combinig Both
@app.get("/users/{user_id}/posts")
def get_user_posts(
    user_id: int, # Path: required
    published: bool = True, # Query: optional
    limit: int = 10 # Query: optional
):
    """Get posts for a specific user"""
    # GET /users/42/posts?published=true&limit=5
    return {"user_id": user_id, "limit": limit}


# ■ WITHOUT Pydantic (tedious & error-prone)
@app.post("/users/")
def create_user_bad(data: dict):
    """Create a new user without Pydantic validation"""
    if "name" not in data:
        raise HTTPException(400, "Name required") 
    if not isinstance(data.get("age"), int):
        raise HTTPException(400, "Age must be int")
 # ... many more checks needed

# ■ WITH Pydantic (clean & automatic)
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    age: int = Field(..., ge=0, le=120)

@app.post("/users/")
def create_user_good(user: UserCreate):
    """Create a new user with Pydantic validation"""
    return user # Already validated!