from fastapi import APIRouter
from db import supabase

router = APIRouter()

@router.post("/signup")
def signup(data: dict):
    response = supabase.auth.sign_up({
        "email": data["email"],
        "password": data["password"]
    })
    return {"data": response}

@router.post("/login")
def login(data: dict):
    response = supabase.auth.sign_in_with_password({
        "email": data["email"],
        "password": data["password"]
    })
    return {"data": response}