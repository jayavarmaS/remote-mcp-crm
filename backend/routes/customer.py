from fastapi import APIRouter, HTTPException
from backend.db import supabase
from backend.models.schemas import Customer

router = APIRouter()

@router.post("/add-customer")
def add_customer(customer: Customer):
    try:
        response = supabase.table("customers").insert({
            "name": customer.name,
            "email": customer.email,
            "user_id": customer.user_id
        }).execute()

        if response.data:
            return {
                "success": True,
                "customer_id": response.data[0]["id"],
                "message": f"Customer {customer.name} added successfully"
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to add customer")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/customers/{user_id}")
def get_customers(user_id: str):
    try:
        response = supabase.table("customers") \
            .select("*") \
            .eq("user_id", user_id) \
            .execute()

        return {
            "success": True,
            "customers": response.data,
            "count": len(response.data)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))