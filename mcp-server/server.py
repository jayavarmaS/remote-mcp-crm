from mcp.server import FastMCP
from fastapi import FastAPI
import requests
import os

mcp = FastMCP("CRM Assistant")
app = FastAPI()

BASE_URL = os.getenv("BACKEND_URL")  # ✅ FIXED

@mcp.tool()
def signup(email: str, password: str):
    res = requests.post(f"{BASE_URL}/signup", json={"email": email, "password": password})
    return res.json()

@mcp.tool()
def login(email: str, password: str):
    res = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
    return res.json()

@mcp.tool()
def add_customer(name: str, email: str, user_id: str):
    res = requests.post(
        f"{BASE_URL}/add-customer",
        json={"name": name, "email": email, "user_id": user_id}
    )
    return res.json()

@mcp.tool()
def get_customers(user_id: str):
    res = requests.get(f"{BASE_URL}/customers/{user_id}")
    return res.json()

app.mount("/", mcp.sse_app())