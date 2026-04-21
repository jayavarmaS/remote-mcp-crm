from mcp.server import FastMCP
import requests
import os

mcp = FastMCP("CRM Assistant")

BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

@mcp.tool()
def signup(email: str, password: str):
    """Create a new user account"""
    try:
        response = requests.post(f"{BASE_URL}/signup", json={"email": email, "password": password})
        if response.status_code == 200:
            data = response.json()
            return f"✅ User created successfully! User ID: {data.get('user_id', 'Unknown')}"
        else:
            return f"❌ Failed to create user: {response.text}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
def login(email: str, password: str):
    """Authenticate a user"""
    try:
        response = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
        if response.status_code == 200:
            data = response.json()
            return f"✅ Login successful! User ID: {data.get('user_id', 'Unknown')}"
        else:
            return f"❌ Login failed: {response.text}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
def add_customer(name: str, email: str, user_id: str):
    """Add a new customer for the authenticated user"""
    try:
        response = requests.post(
            f"{BASE_URL}/add-customer",
            json={"name": name, "email": email, "user_id": user_id}
        )
        if response.status_code == 200:
            data = response.json()
            return f"✅ {data.get('message', 'Customer added successfully')}"
        else:
            return f"❌ Failed to add customer: {response.text}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
def get_customers(user_id: str):
    """Retrieve all customers for the authenticated user"""
    try:
        response = requests.get(f"{BASE_URL}/customers/{user_id}")
        if response.status_code == 200:
            data = response.json()
            customers = data.get("customers", [])
            if not customers:
                return "📝 No customers found for this user."
            
            result = f"📋 Found {len(customers)} customer(s):\n"
            for customer in customers:
                result += f"• {customer['name']} ({customer['email']})\n"
            return result
        else:
            return f"❌ Failed to retrieve customers: {response.text}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ✅ FINAL LINE
app = mcp.sse_app()