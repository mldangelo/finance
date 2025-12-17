# Personal Finance Data Repository

Personal financial data aggregation and expense management using Claude Code with MCP (Model Context Protocol) servers.

## Overview

This repository consolidates financial statements and expense data from multiple sources for Michael D'Angelo, enabling AI-assisted expense tracking, reconciliation, and analysis.

## Data Sources

### Credit Cards

#### Chase Sapphire Reserve (`chase/`)
- **Account**: XXXX XXXX XXXX 2030
- **Files**: 11 monthly PDF statements
- **Period**: January 2025 - November 2025
- **Credit Line**: $38,000
- **Contents**: Dining (3x points), travel, rideshare (Uber/Lyft), subscriptions, general purchases
- **Rewards**: ~930,000 Ultimate Rewards points

#### Amex Delta SkyMiles Reserve (`amex/`)
- **Account**: XXXX-XXXXXX-51003
- **Files**: 1 Excel export (`activity.xlsx`)
- **Period**: January 1, 2025 - December 17, 2025
- **Contents**: Delta flights, business services, Anthropic/Claude subscriptions, hotels
- **Format**: Transaction details with extended metadata (merchant address, category, reference)

### Bank Accounts

#### Bank of America (`boa/`)
- **Files**: 12 monthly PDF statements
- **Period**: January 2025 - December 2025
- **Accounts**:
  - Adv Relationship Banking (checking): ~$22,000
  - Advantage Savings: ~$3,200
- **Contents**: Payroll deposits (Promptfoo), credit card payments, utilities, transfers
- **Status**: Preferred Rewards Platinum Honors

### Expense Reimbursements

#### Ramp (`michael_dangelo_expenses.csv`)
- **Records**: 310 reimbursements
- **Total**: $83,468.87
- **Period**: June 2024 - July 2025
- **Categories**: SaaS/Software, Airlines, Restaurants, Taxi/Rideshare, Hotels, General Merchandise
- **Fields**: id, spend_type, spend_time, amount, category, memo, reimbursement_state, accounting_status

## MCP Server Configuration

The `.mcp.json` file configures Model Context Protocol servers for Claude Code integration:

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

### Gmail MCP
- Read, search, and manage emails for expense receipts
- Download attachments
- Manage labels and filters

### Ramp MCP
- View cards and transactions
- Check expense policies
- Submit memos and receipts
- Export spending data

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

## Usage

Start Claude Code in this directory:

```bash
cd /path/to/finance
claude
```

### Example Commands

- "Show my recent Ramp transactions"
- "Find expense receipts in my Gmail"
- "What's our company policy on travel expenses?"
- "Check which transactions are missing receipts"
- "Export all my Ramp reimbursements to a CSV"
- "Analyze my spending by category"

## File Structure

```
finance/
├── .mcp.json                      # MCP server configuration
├── .gitignore                     # Git ignore rules
├── README.md                      # This file
├── michael_dangelo_expenses.csv   # Ramp reimbursement export
├── amex/
│   └── activity.xlsx              # Amex transaction export
├── boa/
│   └── eStmt_YYYY-MM-DD.pdf       # Bank of America statements (12 files)
└── chase/
    └── YYYYMMDD-statements-*.pdf  # Chase statements (11 files)
```

## Security Notes

- OAuth credentials are stored in `~/.gmail-mcp/`
- Never commit credentials to version control
- Ramp access respects your account permissions
- PDF statements may contain sensitive account numbers (partially masked)

## Data Privacy

This repository contains personal financial data. Ensure:
- Repository is private
- Access is restricted to authorized users
- Sensitive data is not shared or exposed
