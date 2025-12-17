# Finance Automation

Expense filing automation using Claude Code with Gmail and Ramp MCP servers.

## Overview

This project uses Model Context Protocol (MCP) servers to enable AI-assisted expense management:

- **Gmail MCP**: Read, search, and manage emails for expense receipts and notifications
- **Ramp MCP**: Query transactions, submit expenses, check policies, and manage cards

## Setup

### Prerequisites

1. A Ramp account (production or sandbox)
2. A Google Cloud project with Gmail API enabled
3. Claude Code CLI installed

### Gmail Authentication

1. Create OAuth 2.0 credentials in Google Cloud Console:
   - Go to APIs & Services > Credentials
   - Create OAuth client ID (Desktop app or Web application)
   - Download the JSON file and rename to `gcp-oauth.keys.json`

2. Authenticate:
   ```bash
   mkdir -p ~/.gmail-mcp
   mv gcp-oauth.keys.json ~/.gmail-mcp/
   npx @gongrzhe/server-gmail-autoauth-mcp auth
   ```

### Ramp Authentication

Ramp MCP uses OAuth via browser. On first use, you'll be prompted to authenticate with your Ramp account.

### MCP Configuration

The `.mcp.json` file in this directory configures both servers for Claude Code:

```json
{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": ["@gongrzhe/server-gmail-autoauth-mcp"]
    },
    "ramp": {
      "command": "npx",
      "args": ["mcp-remote", "https://mcp.ramp.com/mcp"]
    }
  }
}
```

## Usage

Start Claude Code in this directory and the MCP servers will be available:

```bash
cd /path/to/finance
claude
```

### Example Commands

- "Show my recent Ramp transactions"
- "Find expense receipts in my Gmail"
- "What's our company policy on travel expenses?"
- "Check which transactions are missing receipts"

## Available Tools

### Gmail Tools
- Send/draft emails
- Read and search emails
- Download attachments
- Manage labels and filters

### Ramp Tools
- View cards and transactions
- Check expense policies
- Submit memos and receipts
- Query spending data (admin only)

## Security Notes

- OAuth credentials are stored in `~/.gmail-mcp/`
- Never commit credentials to version control
- Ramp access respects your account permissions
