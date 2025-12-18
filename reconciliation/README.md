# Expense Reconciliation System

A robust infrastructure for reconciling credit card statements, bank accounts, and expense tracking across multiple data sources.

## Overview

This system provides:
- **Multi-source transaction tracking** - Import from Chase, Amex, Bank of America, Ramp, and manual expense CSVs
- **Intelligent matching** - Fuzzy matching on amounts, dates, and merchant names
- **Discrepancy detection** - Find duplicates, missing entries, and already-reimbursed items
- **Comprehensive reporting** - Status reports, monthly comparisons, and category breakdowns

## Quick Start

```bash
# Initialize the database
python reconcile.py init

# Import all data sources
python reconcile.py import all

# Run reconciliation
python reconcile.py reconcile

# View status
python reconcile.py status

# Run analysis
python analyze.py summary
```

## Architecture

```
reconciliation/
├── schema.sql          # SQLite database schema
├── reconcile.py        # Main CLI tool
├── analyze.py          # Advanced analysis tool
├── data/
│   └── reconciliation.db   # SQLite database
└── README.md
```

## Database Schema

### Core Tables

| Table | Purpose |
|-------|---------|
| `sources` | Data sources (credit cards, bank accounts) |
| `transactions` | All transactions from all sources |
| `matches` | Matched transaction pairs |
| `reconciliation_runs` | Audit trail of reconciliation runs |
| `discrepancies` | Issues found during reconciliation |
| `import_batches` | Track what files have been imported |

### Views

| View | Purpose |
|------|---------|
| `v_unmatched_transactions` | Transactions not matched to anything |
| `v_source_summary` | Summary stats by source |
| `v_monthly_by_source` | Monthly spending by source |
| `v_open_discrepancies` | Unresolved issues |

## CLI Commands

### reconcile.py

```bash
# Initialize database
python reconcile.py init

# Import specific source
python reconcile.py import expenses    # Import expenses_to_submit.csv
python reconcile.py import ramp        # Import michael_dangelo_expenses.csv
python reconcile.py import chase FILE  # Import Chase CSV export
python reconcile.py import all         # Import all available sources

# Run reconciliation
python reconcile.py reconcile          # Run all reconciliation checks

# Generate reports
python reconcile.py status             # Quick status overview
python reconcile.py report status      # Detailed status
python reconcile.py report discrepancies  # Discrepancy report
python reconcile.py report full        # Complete report

# Direct SQL queries
python reconcile.py query "SELECT * FROM transactions LIMIT 10"
```

### analyze.py

```bash
# Full analysis summary
python analyze.py summary

# Find potential duplicates
python analyze.py duplicates

# Find overlapping amounts between sources
python analyze.py overlaps

# Monthly comparison across sources
python analyze.py monthly

# Top merchants by spend
python analyze.py merchants

# Category breakdown
python analyze.py categories

# Large unmatched expenses
python analyze.py large              # Default >$500
python analyze.py large -t 1000      # Custom threshold
```

## Data Sources

### Currently Supported

| Source | Type | File Pattern |
|--------|------|--------------|
| Expense CSV | Manual tracking | `expenses_to_submit.csv` |
| Ramp | Reimbursements | `michael_dangelo_expenses.csv` |
| Chase | Credit card CSV | `chase/*.csv` |

### Planned

| Source | Type | Notes |
|--------|------|-------|
| Chase PDF | Credit card statement | Requires PDF parsing |
| Amex | Credit card | Similar to Chase |
| Bank of America | Bank statement | PDF parsing |

## Matching Algorithm

The system uses a scoring algorithm to match transactions:

| Factor | Points | Criteria |
|--------|--------|----------|
| Amount | 40 | Exact match within $0.01 |
| Date | 30 | Same day or within 3 days |
| Merchant | 30 | Levenshtein similarity |

**Match threshold**: 60 points minimum

### Match Types

| Type | Description |
|------|-------------|
| `exact` | Confidence > 95% |
| `date_fuzzy` | Amount matches, date within tolerance |
| `amount_fuzzy` | Date matches, amount within tolerance |
| `manual` | User-confirmed match |
| `suggested` | System suggestion, unconfirmed |

## Reconciliation Types

### 1. Expenses vs Ramp
**Purpose**: Identify expenses that were already reimbursed

This prevents double-submission by flagging any expense that matches a Ramp reimbursement.

### 2. Credit Card vs Expenses (Planned)
**Purpose**: Ensure all credit card charges are tracked

Compares Chase/Amex statements against the expense CSV to find missing entries.

### 3. Bank vs Credit Card (Planned)
**Purpose**: Verify credit card payments

Ensures credit card bills are being paid from the bank account.

## Discrepancy Types

| Type | Severity | Meaning |
|------|----------|---------|
| `missing_in_target` | Medium | Exists in source but not target |
| `missing_in_source` | Medium | Exists in target but not source |
| `amount_mismatch` | Low | Matched but amounts differ |
| `date_mismatch` | Low | Matched but dates differ significantly |
| `duplicate` | High | Potential duplicate entry |
| `already_reimbursed` | High | Expense was already reimbursed |
| `needs_review` | Medium | Flagged for manual review |

## Workflow

### Monthly Reconciliation

1. **Export statements**
   - Download Chase CSV from chase.com
   - Export Ramp reimbursements
   - Update expense tracking CSV

2. **Import data**
   ```bash
   python reconcile.py import all
   ```

3. **Run reconciliation**
   ```bash
   python reconcile.py reconcile
   ```

4. **Review discrepancies**
   ```bash
   python reconcile.py report discrepancies
   ```

5. **Analyze**
   ```bash
   python analyze.py summary
   python analyze.py duplicates
   ```

6. **Resolve issues**
   - Investigate flagged items
   - Update expense CSV as needed
   - Re-run reconciliation

### Before Expense Submission

1. Check for already-reimbursed items:
   ```bash
   python reconcile.py reconcile
   python reconcile.py report discrepancies
   ```

2. Verify large expenses are tracked:
   ```bash
   python analyze.py large -t 500
   ```

3. Check for duplicates:
   ```bash
   python analyze.py duplicates
   ```

## Configuration

Key configuration in `reconcile.py`:

```python
# Matching tolerances
DATE_TOLERANCE_DAYS = 3      # Allow dates to differ by up to 3 days
AMOUNT_TOLERANCE = 0.01      # Allow 1 cent difference
FUZZY_MATCH_THRESHOLD = 0.8  # 80% similarity for merchant names
```

## File Locations

```
/Users/mdangelo/projects/finance/
├── expenses_to_submit.csv          # Main expense tracking
├── michael_dangelo_expenses.csv    # Ramp export
├── chase/                          # Chase statements
│   ├── 20250117-statements-2030-.pdf
│   └── ...
├── boa/                            # Bank of America statements
│   ├── eStmt_2025-01-14.pdf
│   └── ...
└── reconciliation/                 # This system
    ├── schema.sql
    ├── reconcile.py
    ├── analyze.py
    ├── data/
    │   └── reconciliation.db
    └── README.md
```

## Troubleshooting

### "File already imported"
The system tracks imported files by hash. To re-import:
```bash
python reconcile.py query "DELETE FROM import_batches WHERE file_path LIKE '%filename%'"
```

### Low match counts
Check date ranges - sources may not overlap:
```bash
python analyze.py summary
```

### Reset database
```bash
rm reconciliation/data/reconciliation.db
python reconcile.py init
```

## Future Enhancements

1. **PDF Statement Parsing**
   - Use `pdfplumber` or `tabula-py` for Chase/Amex PDFs
   - Extract transaction tables automatically

2. **Bank Account Reconciliation**
   - Track credit card payments
   - Verify outgoing transfers

3. **Gmail Receipt Integration**
   - Auto-import receipts via Gmail API
   - Match to transactions

4. **Web Dashboard**
   - Visual reconciliation status
   - Interactive discrepancy resolution

5. **Scheduled Reconciliation**
   - Cron job for daily/weekly checks
   - Email alerts for issues
