from pydantic import BaseModel, EmailStr

# UserCreate
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

# UserLogin
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# UserResponse
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    class Config:
        from_attributes = True