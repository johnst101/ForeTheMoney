from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.users import Users
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserLoginResponse
from app.utils.security import hash_password, verify_password, create_jwt_token, decode_jwt_token
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import jwt

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_DAYS = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS"))

auth_router = APIRouter(prefix="/auth", tags=["auth"])

http_bearer = HTTPBearer()

def get_current_user_dependency(credentials: HTTPAuthorizationCredentials = Depends(http_bearer), db: Session = Depends(get_db)):
    token = credentials.credentials  # HTTPBearer strips the "Bearer " prefix automatically
    try:
        decoded_token = decode_jwt_token(token, SECRET_KEY, [ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_id = decoded_token.get("user_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user
    

# POST /register
@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
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
    return UserResponse.model_validate(db_user)
    
    ## Other error handling needed?


# POST /login
@auth_router.post("/login", status_code=status.HTTP_200_OK)
    ## Take UserLogin schema data and DB session as input
def login(user: UserLogin, db: Session = Depends(get_db)) -> UserLoginResponse:
    ## Find the user in the database by their email
    db_user = db.query(Users).filter(Users.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    ## Verify the password using the verify_password utility function in utils/security.py
    stored_hashed_password = db_user.password_hash
    password_is_valid = verify_password(user.password, stored_hashed_password)
    
    ## If the password is correct, return a success message and the user data through UserResponse schema and/or a JWT token for authentication
    if password_is_valid:
        access_token = create_jwt_token({"user_id": db_user.id, "exp": datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)}, SECRET_KEY, ALGORITHM)
        return UserLoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.model_validate(db_user)
        )
    ## If the password is incorrect, return an error message indicating invalid credentials
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    ## Other error handling needed?


@auth_router.get("/me")
def get_current_user(current_user: Users = Depends(get_current_user_dependency)):
    return UserResponse.model_validate(current_user)


# POST /refresh_token??