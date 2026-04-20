# 🤖 Cline + Remote MCP Server: Complete Guide

## **Overview: What is Cline and How Does It Work?**

### **What is Cline?**
Cline is an **AI coding assistant for VS Code** that:
- Runs directly inside VS Code (no external tabs needed)
- **Can execute your MCP tools** through a chat interface
- Reads/writes code, runs terminals, and uses AI intelligence
- **Connects to your remote MCP servers** to extend capabilities

---

## **Architecture: How Everything Connects**

### **LOCAL SETUP (Development)**
```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR COMPUTER (Local)                    │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  VS Code + Cline Extension                           │  │
│  │  • Chat UI inside your editor                        │  │
│  │  • Sends requests to MCP server                      │  │
│  │  • Displays tool results                             │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                         │
│                   │ HTTP Request                            │
│                   │ GET /sse                                │
│                   ↓                                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  MCP Server (FastMCP)                                │  │
│  │  Port: 8001                                          │  │
│  │  • Exposes 4 CRM tools via /sse endpoint             │  │
│  │  • Routes requests to Backend                        │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                         │
│                   │ HTTP Requests                           │
│                   │ POST /signup, /login, /add-customer    │
│                   ↓                                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FastAPI Backend                                     │  │
│  │  Port: 8000                                          │  │
│  │  • User authentication                               │  │
│  │  • Customer management                               │  │
│  │  • Database operations                               │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### **REMOTE SETUP (Production)**
```
┌──────────────────────────────┐         ┌──────────────────────────────┐
│   Claude Desktop / Claude    │         │     Cline in VS Code         │
│   Chat Interface             │         │     (Your Local VS Code)     │
│   • Can call MCP tools       │         │     • Can call MCP tools     │
└────────────┬─────────────────┘         └────────────┬─────────────────┘
             │                                        │
             └────────────────┬─────────────────────┬─┘
                              │
                              │ HTTPS Request
                              │ /sse endpoint
                              ↓
                    ┌──────────────────────────┐
                    │  Render (Cloud Hosting)  │
                    │  • MCP Server deployed   │
                    │  • Port: automatic       │
                    │  • URL: your-app.        │
                    │    onrender.com/sse      │
                    └────────────┬─────────────┘
                                 │
                                 │ HTTP Requests
                                 ↓
                    ┌──────────────────────────┐
                    │  Backend (Render/Other)  │
                    │  • CRM API endpoints     │
                    └──────────────────────────┘
```

---

## **How Cline Works: Step-by-Step**

### **1️⃣ Launch Cline**
- Open VS Code
- Click the **Cline icon** on the left sidebar
- Chat panel opens at the bottom

### **2️⃣ Cline Detects MCP Servers**
- Cline reads `cline_mcp_settings.json`
- Finds your local MCP server at `http://127.0.0.1:8001/sse`
- Establishes connection via **Server-Sent Events (SSE)**

### **3️⃣ Available Tools Display**
- Cline shows a **"🔧 Tools"** or **"Available Models"** section
- Lists your 4 CRM tools:
  - `signup`
  - `login`
  - `add_customer`
  - `get_customers`

### **4️⃣ You Make a Request**
**Example natural language request:**
```
@crm-assistant Can you sign up a new user with email "john@example.com" and password "secure123"?
```

### **5️⃣ Cline Calls the Tool**
```
Cline Chat → MCP Server → Backend API → Database
  ↓            ↓            ↓               ↓
Process      Route to    Execute        Store
request      tool        endpoint       data
```

### **6️⃣ Results Display in Chat**
```
Response:
{
  "email": "john@example.com",
  "user_id": "user_123",
  "status": "success"
}
```

---

## **LOCAL SETUP: Getting Started**

### **Prerequisites**
✅ MCP server code in `d:\learnTASK\remote_servermcp_CRM\mcp-server\`
✅ Backend running on port 8000
✅ Cline installed in VS Code

---

### **Step 1: Start Your Backend (Terminal 1)**

```bash
cd d:\learnTASK\remote_servermcp_CRM\backend
# Activate virtual environment (if needed)
python -m venv .venv
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend
uvicorn main:app --reload --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

---

### **Step 2: Start Your MCP Server (Terminal 2)**

```bash
cd d:\learnTASK\remote_servermcp_CRM\mcp-server

# Create virtual environment (first time only)
python -m venv .venv
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start MCP server
uvicorn server:app --host 127.0.0.1 --port 8001
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8001
INFO:     Application startup complete
```

---

### **Step 3: Verify Connection**

**In a new terminal, test the SSE endpoint:**
```bash
curl http://127.0.0.1:8001/sse -v
```

Should return `200 OK`, not 404.

---

### **Step 4: Cline Configuration**

Your Cline settings file is already configured at:
```
C:\Users\DS\AppData\Roaming\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json
```

**Current content:**
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

✅ **This is ready to use!**

---

### **Step 5: Restart VS Code**

1. **Close VS Code completely** (not just minimizing)
2. **Wait 3 seconds**
3. **Reopen VS Code**

---

### **Step 6: Open Cline Chat**

1. Click the **Cline icon** in the left sidebar
2. You should see a chat interface
3. Look for a **"Tools"** section
4. Should show: **crm-assistant** ✅

---

### **Step 7: Test Your First Tool Call**

In the Cline chat, type:

```
@crm-assistant Use the signup tool to create a new user with email "test@example.com" and password "test123"
```

**Expected result:**
```
✅ Tool execution successful

Response:
{
  "id": "user-12345",
  "email": "test@example.com",
  "message": "User created successfully"
}
```

---

## **Common Cline Commands**

### **Sign Up a User**
```
@crm-assistant Sign up user: email="alice@company.com", password="secure456"
```

### **Login User**
```
@crm-assistant Log in user: email="alice@company.com", password="secure456"
```

### **Add a Customer**
```
@crm-assistant Add customer named "Bob Johnson" with email "bob@example.com" to user "user-12345"
```

### **Get All Customers**
```
@crm-assistant Retrieve all customers for user ID "user-12345"
```

---

## **UI Breakdown: Where Things Are in Cline**

```
┌─────────────────────────────────────────────────────────────┐
│  VS Code Window                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [≡] File Explorer  | Search | Source | Run | Extensions  │
│                                                             │
│  Your Code Editor Area                                      │
│  ┌────────────────────────────────────────────────┐        │
│  │                                                │        │
│  │  server.py (your MCP server code)             │        │
│  │  ...code here...                              │        │
│  │                                                │        │
│  └────────────────────────────────────────────────┘        │
│                                                             │
│ ┌────────────────────────── CLINE CHAT ──────────────────┐ │
│ │  CRM Assistant                              [×] [↻]    │ │
│ │  ╔════════════════════════════════════════════════════╗ │
│ │  ║ You: @crm-assistant Get customers for user-123   ║ │
│ │  ║                                                    ║ │
│ │  ║ Cline: I'll fetch the customers...              ║ │
│ │  ║ [🔧 Calling tool: get_customers]                ║ │
│ │  ║                                                    ║ │
│ │  ║ Response:                                          ║ │
│ │  ║ {                                                  ║ │
│ │  ║   "customers": [                                  ║ │
│ │  ║     {"name": "John", "email": "john@..."}        ║ │
│ │  ║   ]                                                ║ │
│ │  ║ }                                                  ║ │
│ │  ╚════════════════════════════════════════════════════╝ │
│ │                                                         │
│ │  💬 Message input: @crm-assistant [Your prompt]        │
│ │                                                         │
│ │  🔧 Tools: crm-assistant ✅                            │
│ │                                                         │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## **Troubleshooting**

### **Issue: "crm-assistant" not showing in Tools**
- ❌ MCP server isn't running (port 8001)
- ❌ Configuration file has wrong URL
- ❌ VS Code hasn't been restarted

**Solution:**
```bash
# Check if server is running
netstat -ano | findstr :8001

# Restart MCP server
uvicorn server:app --host 127.0.0.1 --port 8001
```

### **Issue: Tool calls fail**
- ❌ Backend not running (port 8000)
- ❌ `BACKEND_URL` environment variable not set

**Solution:**
```bash
# Ensure backend is running
uvicorn main:app --reload --port 8000
```

### **Issue: Connection timeout**
- ❌ VS Code isn't seeing the updated settings

**Solution:**
1. Close VS Code
2. Wait 5 seconds
3. Reopen VS Code
4. Trigger Cline to refresh

---

## **Next: Switch to Remote (Render)**

Once local testing works, deploying to Render is simple:

1. **Update Cline config** to use Render URL:
```json
{
  "mcpServers": {
    "crm-assistant": {
      "url": "https://your-app.onrender.com/sse"
    }
  }
}
```

2. **Restart VS Code**
3. **Same Cline interface**, same tools, now calling **cloud services**!

---

## **Summary: Cline Local Workflow**

| Step | What Happens | Where |
|------|--------------|-------|
| 1 | You type a prompt | Cline Chat (VS Code) |
| 2 | Cline detects tool mention | MCP connection ↔ Server |
| 3 | Tool sends formatted request | SSE → MCP Server |
| 4 | MCP routes to backend API | HTTP → Backend (8000) |
| 5 | Backend processes request | Database operations |
| 6 | Response flows back | Backend → MCP → Cline |
| 7 | Chat displays result | Cline Chat UI |

---

## **Your MCP Tools Available**

### **Tool 1: `signup`**
- **Purpose:** Create new user accounts
- **Inputs:** `email`, `password`
- **Returns:** User ID, status

### **Tool 2: `login`**
- **Purpose:** Authenticate users
- **Inputs:** `email`, `password`
- **Returns:** Auth token, user ID

### **Tool 3: `add_customer`**
- **Purpose:** Add customer record
- **Inputs:** `name`, `email`, `user_id`
- **Returns:** Customer ID, status

### **Tool 4: `get_customers`**
- **Purpose:** Retrieve customer list
- **Inputs:** `user_id`
- **Returns:** Array of customers

---

## **File Locations**

```
d:\learnTASK\remote_servermcp_CRM\
├── backend/                              ← Backend API (port 8000)
│   ├── main.py                          ← FastAPI app
│   ├── routes/
│   │   ├── auth.py                      ← Auth endpoints
│   │   └── customer.py                  ← Customer endpoints
│   └── requirements.txt
│
├── mcp-server/                          ← MCP Server (port 8001)
│   ├── server.py                        ← MCP tools definition
│   └── requirements.txt
│
└── CLINE_SETUP_GUIDE.md                 ← This file!

Cline Config:
C:\Users\DS\AppData\Roaming\Code\User\globalStorage\
  saoudrizwan.claude-dev\settings\
  cline_mcp_settings.json
```

---

## **Quick Reference**

**Start Development Environment:**
```bash
# Terminal 1: Backend
cd backend && .\.venv\Scripts\activate && uvicorn main:app --reload

# Terminal 2: MCP Server
cd mcp-server && .\.venv\Scripts\activate && uvicorn server:app --host 127.0.0.1 --port 8001

# Terminal 3: Test connection
curl http://127.0.0.1:8001/sse -v
```

**Then open VS Code and use Cline!** 🚀

---

## **Questions?**

- **Local not working?** Check both servers are running on ports 8000 and 8001
- **Cline not detecting tools?** Restart VS Code after editing the config
- **Tool calls failing?** Check backend logs for errors
- **Ready for Render?** Update the URL in `cline_mcp_settings.json` to your Render domain

Happy coding! 🎉
