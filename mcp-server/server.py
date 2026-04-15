from mcp.server import FastMCP
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import requests
import os

mcp = FastMCP("CRM Assistant")

app = FastAPI()

# ✅ FIX: allow external hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]
)

# backend URL (use env or fallback)
BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


@mcp.tool()
def signup(email: str, password: str):
    return requests.post(f"{BASE_URL}/signup", json={"email": email, "password": password}).json()


@mcp.tool()
def login(email: str, password: str):
    return requests.post(f"{BASE_URL}/login", json={"email": email, "password": password}).json()


@mcp.tool()
def add_customer(name: str, email: str, user_id: str):
    return requests.post(
        f"{BASE_URL}/add-customer",
        json={"name": name, "email": email, "user_id": user_id}
    ).json()


@mcp.tool()
def get_customers(user_id: str):
    return requests.get(f"{BASE_URL}/customers/{user_id}").json()


# ✅ mount MCP
app.mount("/", mcp.sse_app())