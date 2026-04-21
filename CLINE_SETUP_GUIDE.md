# Cline Setup Guide for CRM MCP Server

## Overview
This guide helps you configure Cline (VS Code extension) to work with the AI-powered CRM MCP server.

## Prerequisites
- VS Code with Cline extension installed
- CRM project running locally (backend on port 8000, MCP server on port 8001)

## Configuration

### 1. Open Cline Settings
1. Open VS Code
2. Click the Cline icon in the sidebar
3. Click the settings gear icon (⚙️)

### 2. Add MCP Server Configuration
Add this to your Cline MCP settings:

```json
{
  "mcpServers": {
    "crm-assistant": {
      "url": "http://127.0.0.1:8001/sse"
    }
  }
}
```

### 3. Restart VS Code
1. Close VS Code completely
2. Wait 5 seconds
3. Reopen VS Code

### 4. Verify Connection
1. Open Cline chat panel
2. Type: `@crm-assistant Hello`
3. You should see the MCP server respond

## Usage Examples

### Sign Up
```
@crm-assistant Create a new account for john@example.com with password "secure123"
```

### Login
```
@crm-assistant Log me in with email alice@company.com and password "mypassword"
```

### Add Customer
```
@crm-assistant Add a customer named "Bob Johnson" with email "bob@techcorp.com"
```

### Get Customers
```
@crm-assistant Show me all my customers
```

## Troubleshooting

### "MCP server not found"
- Ensure both backend (port 8000) and MCP server (port 8001) are running
- Check that the URL in settings matches exactly: `http://127.0.0.1:8001/sse`

### "No tools available"
- Restart VS Code after changing MCP settings
- Check VS Code developer console for errors (Help → Toggle Developer Tools)

### API Errors
- Verify Supabase credentials in `backend/.env`
- Check that the database table `customers` exists with correct schema
- Ensure Row Level Security is enabled on the customers table

## Next Steps
- Deploy to production using Render
- Configure Claude Desktop for remote access
- Add more CRM features (update customer, delete customer, etc.)