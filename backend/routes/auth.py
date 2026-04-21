from fastapi import APIRouter, HTTPException
from backend.db import supabase

router = APIRouter()

@router.post("/signup")
def signup(data: dict):
    try:
        response = supabase.auth.sign_up({
            "email": data["email"],
            "password": data["password"]
        })
        if response.user:
            return {"success": True, "user_id": str(response.user.id), "message": "User created successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to create user")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(data: dict):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": data["email"],
            "password": data["password"]
        })
        if response.user and response.session:
            return {
                "success": True,
                "user_id": str(response.user.id),
                "access_token": response.session.access_token,
                "message": "Login successful"
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Login failed")