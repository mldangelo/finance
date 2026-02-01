# Double-Entry Accounting Implementation Plan

**Created:** January 3, 2026
**Status:** Planning Phase

---

## Executive Summary

Current system is **single-entry bookkeeping** - transactions are tracked but not balanced with debits/credits. For proper double-entry accounting, we need to implement a Chart of Accounts, journal entries, and balance tracking.

---

## Current State Analysis

### Database Statistics (as of Jan 3, 2026)

| Source | Transactions | Net Amount | Date Range |
|--------|--------------|------------|------------|
| Chase Visa | 2,016 | $3,852.17 | Dec 2024 - Nov 2025 |
| Amex | 226 | $124,805.52 | Jan 2025 - Dec 2025 |
| Bank of America | 177 | $41,685.93 | Dec 2024 - Dec 2025 |
| Expense CSV | 375 | $94,974.49 | Aug 2025 - Dec 2025 |
| Ramp Reimbursements | 310 | $83,468.87 | Jun 2024 - Jul 2025 |

### Current Capabilities
- Multi-source transaction import
- Fuzzy matching between sources
- Discrepancy detection
- Basic reporting

### Critical Gaps

| Gap | Impact | Priority |
|-----|--------|----------|
| **No Chart of Accounts** | Can't categorize by accounting standard | HIGH |
| **No debit/credit entries** | Can't verify balances | HIGH |
| **No payment tracking** | CC payments not linked to liabilities | HIGH |
| **Stale data** | Expense CSV has 794 items, DB has 375 | HIGH |
| **No reimbursement receipts** | A/R balance unknown | MEDIUM |
| **No period closing** | Can't generate financial statements | MEDIUM |
| **No trial balance** | Can't verify books balance | MEDIUM |

---

## Double-Entry Accounting Requirements

### 1. Chart of Accounts

```
1000-1999: ASSETS
  1000 - Cash & Bank Accounts
    1010 - Bank of America Checking
    1020 - Other Bank Accounts
  1100 - Accounts Receivable
    1110 - A/R from Ramp (Pending Reimbursements)
    1120 - A/R from Promptfoo (if applicable)

2000-2999: LIABILITIES
  2000 - Credit Card Payables
    2010 - Chase Visa ****2030
    2020 - American Express
    2030 - Other Credit Cards

3000-3999: EQUITY
  3000 - Owner's Equity / Retained Earnings

4000-4999: REVENUE (for completeness)
  4000 - Reimbursements Received

5000-5999: EXPENSES
  5100 - Travel
    5110 - Airfare
    5120 - Hotels
    5130 - Ground Transportation (Uber/Lyft)
    5140 - Meals - Travel
  5200 - Software & Subscriptions
    5210 - AI/ML Tools (Anthropic, OpenAI, etc.)
    5220 - Video Conferencing (Zoom)
    5230 - Recruiting (Wellfound)
    5240 - Security/Compliance (Vanta, Sentry)
    5250 - Other SaaS
  5300 - Infrastructure
    5310 - Cloud Services (GCP)
    5320 - API Services
    5330 - Internet/Telecom
  5400 - Equipment
    5410 - Computer Hardware
    5420 - Office Equipment
    5430 - Supplies
  5500 - Meals & Entertainment
    5510 - Team Meals
    5520 - Client Entertainment
  5600 - Events & Conferences
    5610 - Conference Registration
    5620 - Conference Travel
  5900 - Other Expenses
```

### 2. Journal Entry Examples

**Example 1: Credit Card Purchase**
```
Date: 2025-12-10
Description: Zoom Annual Subscription
  Debit:  5220 - Video Conferencing    $2,418.90
  Credit: 2010 - Chase Visa Payable    $2,418.90
```

**Example 2: Credit Card Payment**
```
Date: 2025-12-14
Description: Chase Autopay
  Debit:  2010 - Chase Visa Payable    $9,167.13
  Credit: 1010 - BoA Checking          $9,167.13
```

**Example 3: Expense Submitted for Reimbursement**
```
Date: 2025-12-10
Description: Submit Zoom for reimbursement
  Debit:  1110 - A/R from Ramp         $2,418.90
  Credit: 5220 - Video Conferencing    $2,418.90
  (This reclassifies from expense to receivable)
```

**Example 4: Reimbursement Received**
```
Date: 2025-12-20
Description: Ramp deposit received
  Debit:  1010 - BoA Checking          $2,418.90
  Credit: 1110 - A/R from Ramp         $2,418.90
```

---

## Schema Changes Required

### New Tables

```sql
-- Chart of Accounts
CREATE TABLE accounts (
    id TEXT PRIMARY KEY,           -- '5220'
    name TEXT NOT NULL,            -- 'Video Conferencing'
    account_type TEXT NOT NULL,    -- 'asset', 'liability', 'equity', 'revenue', 'expense'
    parent_id TEXT REFERENCES accounts(id),
    normal_balance TEXT NOT NULL,  -- 'debit' or 'credit'
    is_active BOOLEAN DEFAULT TRUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Journal Entries (header)
CREATE TABLE journal_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_date DATE NOT NULL,
    description TEXT NOT NULL,
    reference_type TEXT,           -- 'cc_charge', 'cc_payment', 'reimbursement', 'manual'
    reference_id TEXT,             -- Links to transactions.id
    is_posted BOOLEAN DEFAULT FALSE,
    posted_at TIMESTAMP,
    period_id INTEGER REFERENCES accounting_periods(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Journal Entry Lines (debit/credit)
CREATE TABLE journal_entry_lines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    journal_entry_id INTEGER NOT NULL REFERENCES journal_entries(id),
    account_id TEXT NOT NULL REFERENCES accounts(id),
    debit_amount DECIMAL(12,2) DEFAULT 0,
    credit_amount DECIMAL(12,2) DEFAULT 0,
    memo TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (debit_amount >= 0 AND credit_amount >= 0),
    CHECK (NOT (debit_amount > 0 AND credit_amount > 0))  -- Can't have both
);

-- Accounting Periods
CREATE TABLE accounting_periods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    period_name TEXT NOT NULL,     -- '2025-12'
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_closed BOOLEAN DEFAULT FALSE,
    closed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Credit Card Statements (for balance verification)
CREATE TABLE cc_statements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT NOT NULL REFERENCES sources(id),
    statement_date DATE NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    opening_balance DECIMAL(12,2),
    purchases DECIMAL(12,2),
    payments DECIMAL(12,2),
    credits DECIMAL(12,2),
    fees DECIMAL(12,2),
    interest DECIMAL(12,2),
    closing_balance DECIMAL(12,2),
    minimum_payment DECIMAL(12,2),
    due_date DATE,
    file_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Account Balances (denormalized for performance)
CREATE TABLE account_balances (
    account_id TEXT NOT NULL REFERENCES accounts(id),
    period_id INTEGER NOT NULL REFERENCES accounting_periods(id),
    opening_balance DECIMAL(12,2) DEFAULT 0,
    total_debits DECIMAL(12,2) DEFAULT 0,
    total_credits DECIMAL(12,2) DEFAULT 0,
    closing_balance DECIMAL(12,2) DEFAULT 0,
    PRIMARY KEY (account_id, period_id)
);
```

### Views for Double-Entry

```sql
-- Trial Balance
CREATE VIEW v_trial_balance AS
SELECT
    a.id as account_id,
    a.name as account_name,
    a.account_type,
    SUM(jel.debit_amount) as total_debits,
    SUM(jel.credit_amount) as total_credits,
    SUM(jel.debit_amount) - SUM(jel.credit_amount) as balance
FROM accounts a
LEFT JOIN journal_entry_lines jel ON a.id = jel.account_id
LEFT JOIN journal_entries je ON jel.journal_entry_id = je.id
WHERE je.is_posted = TRUE
GROUP BY a.id, a.name, a.account_type
ORDER BY a.id;

-- Account Ledger
CREATE VIEW v_account_ledger AS
SELECT
    a.id as account_id,
    a.name as account_name,
    je.entry_date,
    je.description,
    jel.debit_amount,
    jel.credit_amount,
    jel.memo
FROM journal_entry_lines jel
JOIN journal_entries je ON jel.journal_entry_id = je.id
JOIN accounts a ON jel.account_id = a.id
WHERE je.is_posted = TRUE
ORDER BY a.id, je.entry_date;

-- Expense by Category
CREATE VIEW v_expenses_by_category AS
SELECT
    a.parent_id as category_id,
    p.name as category_name,
    a.id as account_id,
    a.name as account_name,
    strftime('%Y-%m', je.entry_date) as month,
    SUM(jel.debit_amount) as total_expense
FROM journal_entry_lines jel
JOIN journal_entries je ON jel.journal_entry_id = je.id
JOIN accounts a ON jel.account_id = a.id
LEFT JOIN accounts p ON a.parent_id = p.id
WHERE a.account_type = 'expense' AND je.is_posted = TRUE
GROUP BY a.parent_id, p.name, a.id, a.name, strftime('%Y-%m', je.entry_date)
ORDER BY category_id, account_id, month;
```

---

## Implementation Phases

### Phase 1: Schema & Data Refresh (Priority: HIGH)
1. [ ] Create new double-entry tables
2. [ ] Re-import all data sources with current data:
   - [ ] Refresh expense CSV (794 items, $214K)
   - [ ] Import December Chase statement
   - [ ] Import Amex 90-day export
   - [ ] Update Ramp export (currently 6 months stale)
3. [ ] Create Chart of Accounts seed data
4. [ ] Map existing categories to accounts

### Phase 2: Journal Entry Generation (Priority: HIGH)
1. [ ] Auto-generate journal entries from transactions
2. [ ] Handle credit card purchases (Debit Expense, Credit CC Payable)
3. [ ] Track credit card payments from BoA statements
4. [ ] Implement posting workflow

### Phase 3: Reimbursement Tracking (Priority: MEDIUM)
1. [ ] Track expense submissions to Ramp
2. [ ] Track reimbursement deposits received
3. [ ] Maintain A/R balance for pending reimbursements
4. [ ] Reconcile A/R against Ramp reports

### Phase 4: Balance Verification (Priority: MEDIUM)
1. [ ] Import CC statement balances
2. [ ] Verify calculated CC payable matches statement
3. [ ] Generate trial balance report
4. [ ] Period closing workflow

### Phase 5: Reporting (Priority: LOW)
1. [ ] Income statement (P&L)
2. [ ] Balance sheet
3. [ ] Cash flow analysis
4. [ ] Expense reports by category/period

---

## Immediate Actions Required

### 1. Update Database with Current Data

```bash
# In reconciliation folder
python reconcile.py import expenses   # Will need to handle 794 items
python reconcile.py import chase /path/to/december/statement
python reconcile.py import amex /path/to/90day/export
```

### 2. Get Fresh Ramp Export

The Ramp data is 6 months stale (ends Jul 2025). Need to:
1. Export from Ramp: All reimbursements Jul 2025 - Jan 2026
2. Import to database

### 3. Track CC Payments

From BoA statements, identify payments to:
- Chase Visa (AUTOPAY entries in Chase statement)
- American Express

### 4. Calculate Current Balances

| Account | Should Be | Data Needed |
|---------|-----------|-------------|
| Chase Visa Payable | ~$17,269 | Dec statement |
| Amex Payable | ? | Need Jan statement |
| A/R from Ramp | ~$214K - $83K = ~$131K | Need updated Ramp export |

---

## Questions to Resolve

1. **Reimbursement Policy**: Are all expenses reimbursable, or only certain categories?
2. **Personal vs Business**: How to handle split transactions (e.g., travel with personal days)?
3. **Multi-entity**: Is this just for Promptfoo expenses, or personal tracking too?
4. **Tax Categories**: Do we need to track by tax-deductible status?
5. **Currency**: Any foreign currency transactions to handle?

---

## Files to Create/Modify

| File | Purpose | Status |
|------|---------|--------|
| `schema.sql` | Add double-entry tables | TODO |
| `chart_of_accounts.sql` | Seed data for accounts | TODO |
| `reconcile.py` | Add journal entry generation | TODO |
| `double_entry.py` | New module for GL operations | TODO |
| `reports.py` | Financial statement generation | TODO |

---

## Success Criteria

1. **Trial balance balances** - Total debits = Total credits
2. **CC payable matches statements** - Calculated liability = Statement balance
3. **A/R reconciles** - Submitted expenses - Received reimbursements = A/R balance
4. **Bank reconciles** - Calculated bank balance matches actual balance
5. **Period can be closed** - All entries posted, no unbalanced transactions
