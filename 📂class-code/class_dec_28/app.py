from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException, status


# =============================================================================
# Pydantic Models - Data validation and serialization schemas
# =============================================================================

class UserBase(BaseModel):
    """Base user model with common fields shared across user schemas."""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    age: Optional[int] = Field(None, ge=0, le=150)


class UserCreate(UserBase):
    """Schema for creating a new user. Extends UserBase with password field."""
    password: str = Field(..., min_length=10) 


class UserUpdate(BaseModel):
    """Schema for updating user details. All fields are optional."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None 


class UserResponse(UserBase):
    """Schema for user responses. Excludes sensitive data like password."""
    id: int
    created_at: datetime
    is_active: bool = True 


# =============================================================================
# Application Setup
# =============================================================================

app = FastAPI()


# =============================================================================
# In-Memory Database & Helper Functions
# =============================================================================

# Simple in-memory storage for users (use a real database in production)
users_db: dict = {}
user_id_counter: int = 1


def get_next_id() -> int:
    """Generate and return the next unique user ID."""
    global user_id_counter
    current = user_id_counter
    user_id_counter += 1
    return current


# =============================================================================
# API Endpoints
# =============================================================================

@app.get("/")
def read_root():
    """Root endpoint - returns a simple welcome message."""
    return {"Hello": "World"}


@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    """
    Create a new user.
    
    - Validates user data using UserCreate schema
    - Checks for duplicate email addresses
    - Stores user in the database and returns the created user
    """
    # Check for duplicate email
    for existing in users_db.values():
        if existing["email"] == user.email:
            raise HTTPException(400, "Email exists")
    
    # Create the new user
    user_id = get_next_id()
    new_user = {
        "id": user_id,
        **user.model_dump(),
        "created_at": datetime.now(),
        "is_active": True
    }
    
    # Store in database and return the new user
    users_db[user_id] = new_user
    return new_user