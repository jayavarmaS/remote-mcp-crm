from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str

class Customer(BaseModel):
    name: str
    email: str
    user_id: str