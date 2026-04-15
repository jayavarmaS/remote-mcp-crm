from mcp.server import FastMCP
from fastapi import FastAPI
import requests

# Create MCP instance
mcp = FastMCP("CRM Assistant")

# FastAPI app
app = FastAPI()

BASE_URL = "http://127.0.0.1:8000"  # change later after backend deploy

# 🔹 TOOL: Signup
@mcp.tool()
def signup(email: str, password: str):
    res = requests.post(
        f"{BASE_URL}/signup",
        json={"email": email, "password": password}
    )
    return res.json()

# 🔹 TOOL: Login
@mcp.tool()
def login(email: str, password: str):
    res = requests.post(
        f"{BASE_URL}/login",
        json={"email": email, "password": password}
    )
    return res.json()

# 🔹 TOOL: Add Customer
@mcp.tool()
def add_customer(name: str, email: str, user_id: str):
    res = requests.post(
        f"{BASE_URL}/add-customer",
        json={"name": name, "email": email, "user_id": user_id}
    )
    return res.json()

# 🔹 TOOL: Get Customers
@mcp.tool()
def get_customers(user_id: str):
    res = requests.get(f"{BASE_URL}/customers/{user_id}")
    return res.json()

# Mount MCP into FastAPI
app.mount("/", mcp.sse_app())