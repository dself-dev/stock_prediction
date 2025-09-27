from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr  # Ensures a valid email format so everthing works as it    #should?? this is waht i am thinking from readin the docs
    country: str
    state: str
    password: str