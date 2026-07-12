from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.users import Users
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.utils.security import hash_password, verify_password

auth_router = APIRouter(prefix="/auth", tags=["auth"])

# POST /register
@auth_router.post("/register")
    ## Take UserCreate schema data and DB session as input
def register(user: UserCreate, db: Session = Depends(get_db)):
    ## Check if user email already exists in the database
    existing_user = db.query(Users).filter(Users.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    
    ## Hash the password using the hash_password utility function in utils/security.py
    hashed_password = hash_password(user.password)
    
    ## Save the user to the database with the hashed password
    db_user = Users(
        email=user.email,
        password_hash=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
        
    ## Return the created user through UserResponse schema and a success message
    return {"message": "User registered successfully", "user": UserResponse.model_validate(db_user)}
    
    ## Other error handling needed?

# POST /login
@auth_router.post("/login")
    ## Take UserLogin schema data and DB session as input
def login(user: UserLogin, db: Session = Depends(get_db)):
    ## Find the user in the database by their email
    db_user = db.query(Users).filter(Users.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    ## Verify the password using the verify_password utility function in utils/security.py
    stored_hashed_password = db_user.password_hash
    password_is_valid = verify_password(user.password, stored_hashed_password)
    
    ## If the password is correct, return a success message and the user data through UserResponse schema and/or a JWT token for authentication
    if password_is_valid:
        return {"message": "Login successful", "user": UserResponse.model_validate(db_user)}
    ## If the password is incorrect, return an error message indicating invalid credentials
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    ## Other error handling needed?