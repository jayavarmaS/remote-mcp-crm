# 🤖 AI-Powered CRM Assistant

**Chat-driven CRM system using Claude, MCP Server, FastAPI, and Supabase**

An intelligent CRM assistant that allows users to manage customer data through natural language conversations with Claude. Instead of traditional interfaces, users interact via chat, and their requests are processed by a Python-based MCP (Model Context Protocol) server using FastMCP, which translates AI intent into API calls. These requests are handled by a FastAPI backend, where business logic and validation are performed, and user authentication is managed using Supabase Auth. Customer data is securely stored in a PostgreSQL database (via Supabase) with user-level isolation, ensuring each user accesses only their own data. The backend is deployed on Render, making the system accessible as a scalable cloud service.

This project demonstrates how AI, backend APIs, and cloud infrastructure can be integrated to build an intelligent, chat-driven CRM system.

---

## 🎯 Project Overview

### **Architecture**

```
┌─────────────────────┐
│ Claude Desktop      │
│ Natural Language    │
│ Chat Interface      │
└──────────┬──────────┘
           │ SSE Connection
           ↓
┌──────────────────────────────┐
│ MCP Server (FastMCP)         │
│ Port: 8001 (local)           │
│ Translates AI intent into    │
│ API calls                    │
└──────────┬───────────────────┘
           │ HTTP Requests
           ↓
┌──────────────────────────────┐
│ FastAPI Backend              │
│ Port: 8000                   │
│ • Supabase Auth              │
│ • Customer Management        │
│ • PostgreSQL Database        │
│ • User-level Isolation       │
└──────────────────────────────┘
           │
           ↓
┌──────────────────────────────┐
│ Supabase (Cloud)             │
│ • PostgreSQL Database        │
│ • Authentication             │
│ • Row Level Security         │
└──────────────────────────────┘
```

---

## ✨ Features

### **Natural Language CRM Management**
- **Chat-driven interface**: Manage customers through conversations with Claude
- **AI-powered operations**: No traditional UI - just natural language commands
- **Secure user isolation**: Each user can only access their own customer data
- **Real-time processing**: Instant responses through MCP protocol

### **Available MCP Tools**

1. **`signup`** - Create new user accounts with Supabase Auth
   - Input: email, password
   - Output: user_id, status

2. **`login`** - Authenticate users with Supabase
   - Input: email, password
   - Output: auth_token, user_id

3. **`add_customer`** - Add customer records with user isolation
   - Input: name, email, user_id
   - Output: customer_id, status

4. **`get_customers`** - Retrieve customer's personal customer list
   - Input: user_id
   - Output: Array of customers (filtered by user_id)

---

## 📁 Project Structure

```
remote_servermcp_CRM/
│
├── backend/                          ← FastAPI Backend (Port 8000)
│   ├── main.py                      ← FastAPI app & routes
│   ├── db.py                        ← Supabase connection
│   ├── .env                         ← Environment variables (create your own)
│   ├── requirements.txt
│   ├── routes/
│   │   ├── auth.py                  ← User authentication endpoints
│   │   └── customer.py              ← Customer management endpoints
│   └── models/
│       └── schemas.py               ← Pydantic data models
│
├── mcp-server/                      ← MCP Server (Port 8001)
│   ├── __init__.py                  ← Python package marker
│   ├── server.py                    ← MCP tools & SSE app
│   ├── requirements.txt
│   └── tools/                       ← (Optional: additional tool files)
│       ├── auth_tool.py
│       └── customer_tool.py
│
├── CLINE_SETUP_GUIDE.md             ← Detailed Cline configuration
├── README.md                        ← This file

Configuration Files:
C:\Users\{YourUser}\AppData\Roaming\Code\User\globalStorage\
  saoudrizwan.claude-dev\settings\
  cline_mcp_settings.json            ← Cline MCP configuration
```

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8+
- Windows/Mac/Linux
- VS Code with Cline extension (optional but recommended)
- Supabase account
- Two terminal windows

### **1. Set up Supabase Database**

1. **Create a Supabase project** at [supabase.com](https://supabase.com)
2. **Go to SQL Editor** and run this query to create the customers table:

```sql
-- Create customers table
CREATE TABLE customers (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    user_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;

-- Create policy for user isolation
CREATE POLICY "Users can only access their own customers" ON customers
    FOR ALL USING (auth.uid() = user_id);

-- Create index for better performance
CREATE INDEX idx_customers_user_id ON customers(user_id);
```

3. **Get your project credentials**:
   - Go to Settings → API
   - Copy `Project URL` and `anon public` key
   - Update `backend/.env` file with these values
   - **Note**: The provided credentials in `.env` are for demonstration. Replace with your own Supabase project credentials for actual functionality.

### **2. Install Dependencies**

**Backend:**
```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

**MCP Server:**
```bash
cd mcp-server
python -m venv .venv
.\.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

### **2. Start Backend (Terminal 1)**
```bash
cd backend
.\.venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### **3. Start MCP Server (Terminal 2)**
```bash
# From project root directory
uvicorn mcp-server.server:app --host 127.0.0.1 --port 8001
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8001
INFO:     Application startup complete
```

### **4. Verify Connection**
```bash
curl http://127.0.0.1:8001/sse -v
```

Should return `200 OK`.

### **5. Test API Endpoints (Optional)**
```bash
# Test backend root
curl http://127.0.0.1:8000/

# Test signup (requires valid Supabase credentials)
curl -X POST http://127.0.0.1:8000/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

### **5. Test with Cline**
1. Open VS Code
2. Click Cline icon → Chat panel opens
3. Type: `@crm-assistant Sign up a new user with email "test@example.com" and password "test123"`
4. See the response! ✅

---

## 🔌 Using with Different Clients

### **Option 1: Cline (VS Code) - Local Development**

**Configuration:**
```json
{
  "mcpServers": {
    "crm-assistant": {
      "url": "http://127.0.0.1:8001/sse"
    }
  }
}
```

**Usage in Chat:**
```
@crm-assistant Get all customers for user "user-123"
```

### **Option 2: Claude Desktop - Local & Remote**

**Configuration ($HOME/.claude/config.json):**
```json
{
  "mcpServers": {
    "crm": {
      "url": "http://127.0.0.1:8001/sse"
    }
  }
}
```

### **Option 3: Render Cloud - Production**

**Deploy MCP Server to Render:**
1. Push code to GitHub
2. Create Render service
3. Set `BACKEND_URL` environment variable
4. Update client config:

```json
{
  "mcpServers": {
    "crm-assistant": {
      "url": "https://your-app.onrender.com/sse"
    }
  }
}
```

---

## 📊 How It Works: Complete Flow

### **Natural Language → AI Processing → Database**

```
1. User chats with Claude:
   "Add a new customer named John Smith with email john@company.com"

2. Claude understands intent:
   Uses MCP tool 'add_customer' via SSE connection

3. MCP Server receives request:
   Translates natural language to API call

4. Tool makes HTTP request to FastAPI:
   POST http://127.0.0.1:8000/add-customer
   {"name": "John Smith", "email": "john@company.com", "user_id": "user-123"}

5. FastAPI Backend processes:
   • Validates input with Pydantic models
   • Authenticates user via Supabase
   • Inserts customer with user isolation
   • Returns success response

6. Response flows back:
   MCP Server → SSE → Claude → User sees result

7. Result displays in chat:
   "✅ Customer John Smith added successfully!"
```

### **Security & Isolation**
- **User Authentication**: Supabase Auth manages user sessions
- **Data Isolation**: Row Level Security ensures users only see their data
- **API Validation**: FastAPI validates all inputs before database operations

---

## 🛠 Natural Language Commands

### **User Management**
```
@crm-assistant Create a new account for john@example.com with password "secure123"
@crm-assistant Sign me in with email alice@company.com and password "mypassword"
```

### **Customer Management**
```
@crm-assistant Add a customer named "Bob Johnson" with email "bob@techcorp.com"
@crm-assistant Show me all my customers
@crm-assistant Get my customer list
```

### **Conversational Examples**
```
@crm-assistant I need to add Sarah Wilson as a new customer, her email is sarah@startup.io
@crm-assistant Can you show me my current customers?
@crm-assistant Please create an account for me with email test@example.com and password "test123"
```

---

## 🌐 Deployment to Render

### **Deploy Backend to Render**
1. **Create Render account** at [render.com](https://render.com)
2. **Create new Web Service** for the backend:
   - Connect your GitHub repo
   - Set build command: `pip install -r backend/requirements.txt`
   - Set start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - Add environment variables: `SUPABASE_URL` and `SUPABASE_KEY`

### **Deploy MCP Server to Render**
1. **Create another Web Service** for the MCP server:
   - Set build command: `pip install -r mcp-server/requirements.txt`
   - Set start command: `uvicorn mcp-server.server:app --host 0.0.0.0 --port $PORT`
   - Add environment variable: `BACKEND_URL` (pointing to your backend service)

### **Update Client Configuration**
```json
{
  "mcpServers": {
    "crm-assistant": {
      "url": "https://your-mcp-server.onrender.com/sse"
    }
  }
}
```

---

## 📝 Configuration

### **MCP Server Settings**
Edit `cline_mcp_settings.json`:

**Local:**
```json
{
  "mcpServers": {
    "crm-assistant": {
      "url": "http://127.0.0.1:8001/sse",
      "autoApprove": []
    }
  }
}
```

**Remote:**
```json
{
  "mcpServers": {
    "crm-assistant": {
      "url": "https://your-app.onrender.com/sse",
      "autoApprove": []
    }
  }
}
```

---

## 🔍 Debugging

### **Check if servers are running**
```bash
# Backend
netstat -ano | findstr :8000

# MCP Server
netstat -ano | findstr :8001
```

### **Test MCP endpoint**
```bash
curl http://127.0.0.1:8001/sse -v
```

### **View backend logs**
```bash
# In backend terminal, check for errors
```

### **Cline isn't showing tools?**
1. Close VS Code completely
2. Wait 5 seconds
3. Reopen VS Code
4. Check: Settings → MCP Servers → Should show 1 active

---

## 📚 Additional Resources

- **MCP Protocol**: [Model Context Protocol Docs](https://modelcontextprotocol.io)
- **FastAPI**: [FastAPI Documentation](https://fastapi.tiangolo.com)
- **Cline**: [Cline Extension for VS Code](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)
- **Render**: [Render Deployment Guide](https://render.com/docs)

---

## 🤝 Support

For detailed setup and usage, see [CLINE_SETUP_GUIDE.md](./CLINE_SETUP_GUIDE.md)

---

## 📄 License

MIT License - Feel free to use this project as a foundation for your own MCP servers!

---

## 🎉 Project Complete!

✅ **AI-powered CRM system** with natural language interface  
✅ **MCP Server** translating AI intent to API calls  
✅ **FastAPI Backend** with business logic and validation  
✅ **Supabase Integration** for auth and PostgreSQL storage  
✅ **User-level Isolation** ensuring data security  
✅ **Render Deployment** ready for cloud hosting  

### **Ready for Production**
- ✅ Local development setup
- ✅ Error handling and validation
- ✅ Secure user authentication
- ✅ Database schema with RLS
- ✅ MCP protocol implementation
- ✅ Deployment configuration

### **Next Steps**
- 🔄 Replace demo Supabase credentials with your own
- 🚀 Deploy to Render for production use
- 🤖 Connect with Claude Desktop
- 📈 Add more CRM features (edit, delete, search)
- 🔒 Implement additional security measures

**Happy coding! 🎯**
