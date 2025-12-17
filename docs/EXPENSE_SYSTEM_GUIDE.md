# Expense Tracking System Guide

## Overview

This system tracks business expenses for reimbursement from Promptfoo. The primary tracking file is `expenses_to_submit.csv` which consolidates expenses from multiple payment sources and receipt emails.

---

## Key Files

| File | Purpose |
|------|---------|
| `expenses_to_submit.csv` | Main expense tracking file (387 entries, $107,451.28) |
| `expense_reconciliation.md` | Credit card statement analysis and reconciliation |
| `michael_dangelo_expenses.csv` | Ramp export of previously reimbursed expenses |
| `docs/EXPENSE_RULES.md` | Business rules for expense inclusion |
| `docs/MERCHANT_CATEGORIES.md` | Merchant categorization reference |

---

## CSV Structure

The `expenses_to_submit.csv` file has 17 columns:

```
id,date,merchant,description,amount,category,subcategory,source_card,receipt_status,receipt_email_id,receipt_email_subject,receipt_file,email_search_query,submission_status,priority,business_purpose,notes
```

### Column Definitions

| Column | Type | Description |
|--------|------|-------------|
| `id` | String | Unique ID format: `EXP-YYYY-MM-DD-NNN` |
| `date` | Date | Transaction date (YYYY-MM-DD) |
| `merchant` | String | Vendor/merchant name |
| `description` | String | Brief description of expense |
| `amount` | Decimal | Amount in USD |
| `category` | String | Primary category (see below) |
| `subcategory` | String | Subcategory (see below) |
| `source_card` | String | Payment source: `Chase`, `Amex` |
| `receipt_status` | String | `found`, `has_receipt`, `pending`, `not_needed` |
| `receipt_email_id` | String | Gmail message ID if found |
| `receipt_email_subject` | String | Email subject line |
| `receipt_file` | String | Local file path if downloaded |
| `email_search_query` | String | Gmail search query used |
| `submission_status` | String | `pending`, `submitted`, `reimbursed` |
| `priority` | String | `critical`, `high`, `medium`, `low` |
| `business_purpose` | String | Business justification |
| `notes` | String | Additional notes |

---

## Categories and Subcategories

### Infrastructure
- `Cloud Services` - Google Cloud Platform charges
- `API Services` - Anthropic API, OpenAI API usage
- `Remote Work` - Internet service (Comcast/Xfinity)
- `Coworking` - WeWork day passes
- `Security` - Vanta security platform

### Travel
- `Flights` - Delta Air Lines
- `Hotels` - Business travel accommodations
- `Ground Transportation` - Uber, Lyft, transit, taxi
- `Parking` - Business parking

### Equipment
- `Computer` - MacBooks, laptops
- `Computer Monitors` - Displays
- `Computer Peripherals` - Keyboards, mice, cables
- `Office Furniture` - Desks, chairs, standing desks
- `Office Tech` - Streaming devices, AV equipment
- `Office Supplies` - General supplies
- `Office Appliances` - Coffee makers, etc.
- `Office Security` - Locks, safes

### Software
- `AI Tools` - Cursor, Replicate, Perplexity, Claude.ai, ChatGPT
- `HR Tools` - Recruit Pro
- `Cloud Storage` - Google One
- `Communication` - Zoom

### Meals
- `Working Meals` - Individual meals during work
- `Team Meals` - Group/team dinners
- `Coffee` - Coffee shops
- `Groceries` - San Mateo office groceries only

### Professional Development
- `Conferences` - GitHub Universe, tech conferences
- `Books` - Technical books

---

## Payment Sources

### Chase Visa (ending 2030)
- Primary card for most expenses
- Used for: Equipment, meals, software subscriptions, ground transportation
- Statement identifier: Transactions appear with full merchant names

### American Express
- Used for: Large infrastructure costs, travel
- Key charges:
  - Google Cloud Platform (monthly ~$14,500)
  - Anthropic API ($1,500-2,500 monthly)
  - Delta Air Lines flights
  - Claude.ai subscription ($217.75/month)
  - Vanta ($3,500)
  - Recruit Pro ($149/month)

---

## Key Locations

### San Mateo Office (Primary)
```
Promptfoo
107 S B St #200
San Mateo, CA 94401
```
- ALL expenses in San Mateo area are business expenses
- Includes: meals, coffee, groceries, office supplies

### Bay Area (Business)
- Burlingame, Palo Alto, SF - all business when working
- Coffee shops: Philz, Blue Bottle, Verve, Peet's, Backhaus

### NYC Home
```
61 W 8th St
New York, NY 10011
```
- Selective inclusion for meals (work hours, late night)
- EXCLUDE all grocery deliveries
- Include airport transit (LIRR, subway)

### Boston Apartment
```
280 Western Ave Apt 201
Allston, MA 02134
```
- Selective inclusion for work-related meals
- Include MBTA transit for business travel

---

## Data Sources for Receipts

### Gmail Senders
| Sender | Content |
|--------|---------|
| `auto-confirm@amazon.com` | Amazon order confirmations |
| `no-reply@doordash.com` | DoorDash order receipts |
| `messenger@messaging.squareup.com` | Square receipts (coffee shops) |
| `receipts@uber.com` | Uber ride receipts |
| `no-reply@lyftmail.com` | Lyft ride receipts |
| `deltaairlines@t.delta.com` | Delta flight confirmations |
| `@marriott.com` | Hotel confirmations |

### Gmail Search Patterns
```
# Amazon orders
from:auto-confirm@amazon.com subject:shipped

# DoorDash receipts
from:no-reply@doordash.com subject:receipt

# Coffee receipts
from:messenger@messaging.squareup.com

# Uber rides
from:receipts@uber.com

# Lyft rides
from:no-reply@lyftmail.com
```

---

## DoorDash Identification

### CA Orders (Include All)
- Merchant code contains: `855-431-0459 CA`
- Statement shows: `DD [Restaurant] CA`
- Examples: `DD Sweetgree CA`, `DD Risewoodf CA`

### Non-CA Orders (Selective)
- NYC/Boston orders: only include work-related meals
- Wegmans orders are NYC (no CA Wegmans locations)

---

## Priority Levels

| Priority | Criteria | Examples |
|----------|----------|----------|
| `critical` | >$1,000, infrastructure | Google Cloud, large equipment |
| `high` | $200-$1,000, important | Flights, hotels, major purchases |
| `medium` | $50-$200 | Team meals, software |
| `low` | <$50 | Coffee, small meals |

---

## Workflow

### Adding New Expenses

1. **Search Gmail** for receipts using MCP gmail tools
2. **Cross-reference** with credit card statements
3. **Categorize** using merchant reference
4. **Add to CSV** with unique ID
5. **Mark receipt status** (found/pending)

### Monthly Reconciliation

1. Download latest credit card statements
2. Compare against CSV entries
3. Identify missing transactions
4. Search for receipts
5. Update `expense_reconciliation.md`

### Submission

1. Filter by `submission_status=pending`
2. Prioritize by `priority` field
3. Gather all receipts
4. Submit through Ramp
5. Update status to `submitted`

---

## Key Monthly Recurring Expenses

| Merchant | Amount | Card | Category |
|----------|--------|------|----------|
| Google Cloud | ~$14,500 | Amex | Infrastructure |
| Anthropic API | ~$1,500-2,500 | Amex | Infrastructure |
| Claude.ai | $217.75 | Amex | Software |
| Recruit Pro | $149.00 | Amex | Software |
| Comcast/Xfinity | ~$220 | Chase | Infrastructure |
| OpenAI ChatGPT | $217.75 | Chase | Software |
| Perplexity.AI | $21.78 | Chase | Software |
| Google Colab | $10.88 | Chase | Software |
| Google One | $21.76 | Chase | Software |
| Cursor | $10.89 | Chase | Software |

---

## Analysis Commands

```bash
# Total expenses
awk -F',' 'NR>1 {sum += $5} END {printf "$%.2f\n", sum}' expenses_to_submit.csv

# Count by category
awk -F',' 'NR>1 {cat[$6]+=$5} END {for(c in cat) printf "%-20s: $%.2f\n", c, cat[c]}' expenses_to_submit.csv | sort -t'$' -k2 -rn

# Find specific merchant
grep -i "merchant_name" expenses_to_submit.csv

# Expenses by month
awk -F',' 'NR>1 {month=substr($2,1,7); sum[month]+=$5} END {for(m in sum) printf "%s: $%.2f\n", m, sum[m]}' expenses_to_submit.csv | sort
```

---

## Important Notes

1. **Date Discrepancy**: Credit card posting dates may differ from transaction dates by 1-2 days
2. **Duplicate Detection**: Match by amount when dates differ slightly
3. **Receipt Retention**: Keep Gmail receipts for 7 years
4. **Ramp History**: Check `michael_dangelo_expenses.csv` to avoid duplicate submissions
5. **Tax Implications**: All reimbursements are non-taxable business expenses
