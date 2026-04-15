from fastapi import APIRouter
from db import supabase

router = APIRouter()

@router.post("/add-customer")
def add_customer(data: dict):
    response = supabase.table("customers").insert({
        "name": data["name"],
        "email": data["email"],
        "user_id": data["user_id"]
    }).execute()

    return {"data": response.data}


@router.get("/customers/{user_id}")
def get_customers(user_id: str):
    response = supabase.table("customers") \
        .select("*") \
        .eq("user_id", user_id) \
        .execute()

    return {"data": response.data}