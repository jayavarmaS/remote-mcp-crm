# 🤖 Remote MCP CRM Server

**AI-powered CRM assistant using Model Context Protocol (MCP), FastAPI, and Cloud Deployment**

A production-ready system that bridges AI clients (Claude Desktop, Cline, etc.) with a FastAPI backend through an MCP server, enabling intelligent CRM operations through natural language.

---

## 🎯 Project Overview

### **Architecture**

```
┌─────────────────────┐
│ AI Clients          │
│ • Claude Desktop    │
│ • Cline (VS Code)   │
└──────────┬──────────┘
           │ SSE Connection
           ↓
┌──────────────────────────────┐
│ MCP Server (FastMCP)         │
│ Port: 8001 (local)           │
│ Exposes 4 CRM Tools          │
└──────────┬───────────────────┘
           │ HTTP Requests
           ↓
┌──────────────────────────────┐
│ FastAPI Backend              │
│ Port: 8000                   │
│ • Authentication             │
│ • Customer Management        │
│ • Database Operations        │
└──────────────────────────────┘
```

---

## ✨ Features

### **Available MCP Tools**

1. **`signup`** - Create new user accounts
   - Input: email, password
   - Output: user_id, status

2. **`login`** - Authenticate users
   - Input: email, password
   - Output: auth_token, user_id

3. **`add_customer`** - Add customer records
   - Input: name, email, user_id
   - Output: customer_id, status

4. **`get_customers`** - Retrieve customer list
   - Input: user_id
   - Output: Array of customers

---

## 📁 Project Structure

```
remote_servermcp_CRM/
│
├── backend/                          ← FastAPI Backend (Port 8000)
│   ├── main.py                      ← FastAPI app & routes
│   ├── db.py                        ← Database connection
│   ├── requirements.txt
│   ├── routes/
│   │   ├── auth.py                  ← User authentication endpoints
│   │   └── customer.py              ← Customer management endpoints
│   └── models/
│       └── schemas.py               ← Data models & validation
│
├── mcp-server/                      ← MCP Server (Port 8001)
│   ├── server.py                    ← MCP tools definition
│   ├── requirements.txt
│   └── tools/
│       ├── auth_tool.py             ← Authentication logic
│       └── customer_tool.py         ← Customer logic
│
├── README.md                        ← This file
└── CLINE_SETUP_GUIDE.md            ← Setup & usage guide

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
- Two terminal windows

### **1. Install Dependencies**

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
cd mcp-server
.\.venv\Scripts\activate
uvicorn server:app --host 127.0.0.1 --port 8001
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

### **User Request → AI Response**

```
1. User in Cline Chat:
   "@crm-assistant Sign up john@example.com"

2. Cline detects tool mention:
   Sends to MCP Server via /sse

3. MCP Server receives request:
   Routes to 'signup' tool

4. Tool makes HTTP request:
   POST http://127.0.0.1:8000/signup
   {"email": "john@example.com", "password": "..."}

5. Backend processes:
   • Validates input
   • Creates user in database
   • Returns user_id

6. MCP routes response back:
   Response → SSE → Cline Chat

7. Result displays:
   "✅ User created! ID: user-12345"
```

---

## 🛠 Cline Commands

### **Sign Up**
```
@crm-assistant Sign up: email="alice@company.com", password="secure456"
```

### **Login**
```
@crm-assistant Log in: email="alice@company.com", password="secure456"
```

### **Add Customer**
```
@crm-assistant Add customer named "Bob" with email "bob@company.com" to user "user-123"
```

### **Get Customers**
```
@crm-assistant Show all customers for user "user-123"
```

---

## 🌐 Deployment to Render

### **Step 1: Push to GitHub**
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### **Step 2: Create Render Service**
1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect GitHub repo
4. Set build command: `pip install -r mcp-server/requirements.txt`
5. Set start command: `uvicorn mcp-server.server:app --host 0.0.0.0 --port $PORT`

### **Step 3: Environment Variables**
- `BACKEND_URL` = Your backend URL (or another Render service)

### **Step 4: Update Cline Config**
```json
{
  "mcpServers": {
    "crm-assistant": {
      "url": "https://your-crm-mcp.onrender.com/sse"
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

## 🎉 Next Steps

- ✅ Run locally with Cline
- ✅ Test all 4 tools
- ✅ Deploy to Render
- ✅ Connect Claude Desktop
- ✅ Build more tools!

Happy coding! 🚀
