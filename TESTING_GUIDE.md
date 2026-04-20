# 🧪 Testing & Troubleshooting Guide

## Quick Test Checklist

### Phase 1: Server Startup ✅

**Backend Server (Port 8000)**
```bash
cd d:\learnTASK\remote_servermcp_CRM\backend
.\.venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

✅ Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**MCP Server (Port 8001)**
```bash
cd d:\learnTASK\remote_servermcp_CRM\mcp-server
.\.venv\Scripts\activate
uvicorn server:app --host 127.0.0.1 --port 8001
```

✅ Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8001
INFO:     Application startup complete
```

---

### Phase 2: Connection Tests 🔌

**Test Backend**
```bash
curl http://127.0.0.1:8000/ -v
```

✅ Expected: `200 OK` with message "CRM Backend Running 🚀"

**Test MCP Server SSE Endpoint**
```bash
curl http://127.0.0.1:8001/sse -v
```

✅ Expected: `200 OK` with SSE stream

**Test MCP Server Health**
```bash
curl http://127.0.0.1:8001/health -v  # if available
curl http://127.0.0.1:8001/ -v
```

---

### Phase 3: Tool Testing 🔧

#### **Test 1: Signup Tool**

```bash
# From MCP Server terminal, manually test:
# Or use Cline: @crm-assistant signup test@example.com

curl -X POST http://127.0.0.1:8000/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

✅ Expected response:
```json
{
  "id": "user_123",
  "email": "test@example.com",
  "message": "User created successfully"
}
```

#### **Test 2: Login Tool**

```bash
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

✅ Expected:
```json
{
  "token": "some_auth_token",
  "user_id": "user_123",
  "message": "Login successful"
}
```

#### **Test 3: Add Customer**

```bash
curl -X POST http://127.0.0.1:8000/add-customer \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","user_id":"user_123"}'
```

✅ Expected:
```json
{
  "customer_id": "cust_456",
  "name": "John Doe",
  "message": "Customer added successfully"
}
```

#### **Test 4: Get Customers**

```bash
curl http://127.0.0.1:8000/customers/user_123
```

✅ Expected:
```json
{
  "customers": [
    {"customer_id": "cust_456", "name": "John Doe", "email": "john@example.com"}
  ]
}
```

---

### Phase 4: Cline Integration 🤖

1. **Open VS Code**
2. **Click Cline icon** (left sidebar)
3. **Chat panel opens**
4. **Check "Tools" section** → Should show `crm-assistant`

#### **Test Command in Cline Chat:**

```
@crm-assistant Can you sign up a new user with email "alice@example.com" and password "secure123"?
```

✅ Expected in Cline chat:
```
✅ Tool execution successful

Response:
{
  "id": "user_alice",
  "email": "alice@example.com",
  "message": "User created successfully"
}
```

---

## 🐛 Common Issues & Solutions

### Issue 1: "Address already in use" on Port 8000 or 8001

**Problem:** Another process is using the port

**Solution:**
```bash
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Or change MCP server port
uvicorn server:app --host 127.0.0.1 --port 8002
```

---

### Issue 2: "Connection refused" from Cline

**Problem:** MCP server not running or wrong URL

**Checklist:**
- [ ] Is MCP server running? Check terminal for "Uvicorn running"
- [ ] Is port 8001 correct? `netstat -ano | findstr :8001`
- [ ] Is URL correct in config?
  ```json
  "url": "http://127.0.0.1:8001/sse"
  ```
- [ ] Did you restart VS Code after config change?

**Solution:**
```bash
# Restart MCP server
cd mcp-server
.\.venv\Scripts\activate
uvicorn server:app --host 127.0.0.1 --port 8001
```

---

### Issue 3: Cline shows "crm-assistant" but no tools

**Problem:** Connection established but tools not loading

**Solution:**
1. Close VS Code completely
2. Wait 5 seconds
3. Reopen VS Code
4. Open Cline again
5. Try a tool call: `@crm-assistant signup test@example.com`

---

### Issue 4: Tool calls fail with "Backend error"

**Problem:** MCP server connected but backend API failing

**Checklist:**
- [ ] Is backend running? `curl http://127.0.0.1:8000/`
- [ ] Is DB connection working? Check backend logs
- [ ] Are env variables set? Check `.env` file
- [ ] Is BACKEND_URL correctly set?
  ```bash
  echo %BACKEND_URL%  # Windows
  echo $BACKEND_URL    # Mac/Linux
  ```

**Solution:**
```bash
# Verify backend is accessible
curl http://127.0.0.1:8000/ -v

# Check backend logs for errors
# (watch the terminal where backend is running)
```

---

### Issue 5: "Module not found" or import errors

**Problem:** Dependencies not installed

**Solution:**
```bash
# Reinstall dependencies
cd backend
pip install -r requirements.txt --force-reinstall

cd ../mcp-server
pip install -r requirements.txt --force-reinstall
```

---

## 🔍 Debug Mode Steps

### Step 1: Verify Port Usage
```bash
# List all processes using network ports
netstat -ano | findstr LISTENING

# Look for:
# 127.0.0.1:8000  (Backend)
# 127.0.0.1:8001  (MCP Server)
```

### Step 2: Test Each Component

```bash
# 1. Test Backend
curl -X GET http://127.0.0.1:8000/ -v

# 2. Test MCP Server
curl -X GET http://127.0.0.1:8001/ -v

# 3. Test SSE Endpoint
curl -X GET http://127.0.0.1:8001/sse -v

# 4. Test Backend Signup
curl -X POST http://127.0.0.1:8000/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"debug@example.com","password":"debug123"}'
```

### Step 3: Check Configuration

```bash
# Verify Cline config exists
Test-Path "C:\Users\DS\AppData\Roaming\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json"

# View config content
Get-Content "C:\Users\DS\AppData\Roaming\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json"
```

### Step 4: Check Logs

**Backend logs** (in the terminal where it's running):
```
Look for:
- [INFO] requests logging
- [ERROR] for any exceptions
- Database connection status
```

**MCP Server logs** (in terminal):
```
Look for:
- [INFO] SSE connections
- [ERROR] tool execution errors
- HTTP request details
```

---

## ✅ Full Integration Test

### Copy-Paste Test Sequence

**Terminal 1 - Backend:**
```bash
cd d:\learnTASK\remote_servermcp_CRM\backend
.\.venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

**Terminal 2 - MCP Server:**
```bash
cd d:\learnTASK\remote_servermcp_CRM\mcp-server
.\.venv\Scripts\activate
uvicorn server:app --host 127.0.0.1 --port 8001
```

**Terminal 3 - Test API:**
```bash
# Test 1: Backend running?
curl http://127.0.0.1:8000/

# Test 2: MCP Server running?
curl http://127.0.0.1:8001/sse -v

# Test 3: Can we signup?
curl -X POST http://127.0.0.1:8000/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# Test 4: Can we get customers?
curl http://127.0.0.1:8000/customers/test-user
```

**VS Code - Test Cline:**
1. Open Cline chat
2. Look for "crm-assistant" in Tools section
3. Type: `@crm-assistant Get all customers for user "test-user"`
4. Should see response

---

## 📊 Health Check Script

Save as `health_check.ps1`:

```powershell
$backends = @{
    "Backend API" = "http://127.0.0.1:8000/"
    "MCP Server" = "http://127.0.0.1:8001/sse"
}

Write-Host "🔍 Checking system health..." -ForegroundColor Cyan
Write-Host ""

foreach ($name in $backends.Keys) {
    $url = $backends[$name]
    try {
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 2
        Write-Host "✅ $name - RUNNING ($($response.StatusCode))" -ForegroundColor Green
    } catch {
        Write-Host "❌ $name - FAILED (Check if running)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Port Usage:" -ForegroundColor Cyan
netstat -ano | findstr ":8000|:8001"
```

Run with:
```bash
powershell -ExecutionPolicy Bypass -File health_check.ps1
```

---

## 🚨 Emergency Restart

If everything breaks, do this:

```bash
# Kill all Python processes using MCP/FastAPI ports
taskkill /F /IM python.exe

# Wait 5 seconds
Start-Sleep -Seconds 5

# Restart in order:
# Terminal 1:
cd backend && .\.venv\Scripts\activate && uvicorn main:app --reload

# Terminal 2:
cd mcp-server && .\.venv\Scripts\activate && uvicorn server:app --host 127.0.0.1 --port 8001

# Restart VS Code
# Close and reopen
```

---

## ✨ Success Indicators

You'll know everything is working when:

✅ Backend terminal shows "Application startup complete"
✅ MCP Server terminal shows "Application startup complete"  
✅ `curl` commands return 200 OK
✅ Cline shows "crm-assistant" in Tools section
✅ `@crm-assistant` tool calls execute and return results
✅ Tool responses appear in Cline chat
✅ No red error messages in any terminal

---

## 🎯 Quick Command Reference

```bash
# Check ports
netstat -ano | findstr :8000
netstat -ano | findstr :8001

# Test backend
curl http://127.0.0.1:8000/

# Test MCP
curl http://127.0.0.1:8001/sse -v

# Test tool
curl -X POST http://127.0.0.1:8000/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# Restart backend
cd backend && .\.venv\Scripts\activate && uvicorn main:app --reload

# Restart MCP server
cd mcp-server && .\.venv\Scripts\activate && uvicorn server:app --host 127.0.0.1 --port 8001

# Check config
Get-Content "C:\Users\DS\AppData\Roaming\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json"
```

---

## Need Help?

1. **Check logs** in the terminal where each service runs
2. **Run curl tests** to isolate the problem
3. **Restart VS Code** if Cline config changed
4. **Check ports** with `netstat -ano`
5. **Verify URLs** in config match running servers

Good luck! 🚀
