# Master Expense Reconciliation Summary

**Generated:** January 3, 2026
**Files Created:**
- `MASTER_EXPENSE_RECONCILIATION.csv` - Full 844-item list with ramp_status
- `EXPENSE_REVIEW.csv` - Simplified view for review (sorted by status)

---

## CRITICAL FINDING: Potential Duplicates

**6 items ($32,994.62) appear to already be reimbursed through Ramp:**

| ID | Date | Merchant | Amount | Ramp Status |
|----|------|----------|--------|-------------|
| RCPT-20250130-001 | 2025-01-30 | Vanta Q1 | $3,500.00 | ALREADY_REIMBURSED |
| RCPT-20250314-WF | 2025-03-14 | Wellfound | $149.00 | ALREADY_REIMBURSED |
| RCPT-20250414-WF | 2025-04-14 | Wellfound | $149.00 | ALREADY_REIMBURSED |
| BF-20250528-001 | 2025-05-28 | DoorDash | $23.62 | ALREADY_REIMBURSED |
| EXP-2025-04-01-001 | 2025-04-01 | Google Cloud | $14,500.00 | ALREADY_REIMBURSED |
| EXP-2025-07-01-001 | 2025-07-01 | Google Cloud | $14,673.00 | ALREADY_REIMBURSED |

**ACTION:** Remove these 6 items from submission to avoid double reimbursement.

---

## Financial Summary

| Category | Amount |
|----------|--------|
| **Original Expenses to Submit** | $221,627.69 |
| **Less: Already Reimbursed** | -$32,994.62 |
| **NET NEW TO SUBMIT** | **$188,633.07** |
| | |
| Previously Reimbursed (Ramp Jun'24-Jul'25) | $83,468.87 |
| **GRAND TOTAL ALL EXPENSES** | **$272,101.94** |

---

## New Expenses by Category ($188,633.07)

| Category | Count | Amount | % of Total |
|----------|-------|--------|------------|
| Infrastructure | 30 | $52,087.71 | 27.6% |
| Equipment | 91 | $49,491.14 | 26.2% |
| Travel | 177 | $37,194.57 | 19.7% |
| Meals | 469 | $29,035.65 | 15.4% |
| Software | 68 | $19,499.14 | 10.3% |
| Events | 2 | $1,225.86 | 0.6% |
| Professional Development | 1 | $99.00 | 0.1% |

---

## New Expenses by Receipt Status

| Status | Count | Amount | Action Needed |
|--------|-------|--------|---------------|
| **found** | 141 | $87,043.12 | Ready to submit |
| **pending** | 443 | $75,364.17 | Need receipts |
| **email_available** | 204 | $19,187.83 | Forward emails |
| **photo** | 50 | $7,037.95 | Photos ready |

---

## High Priority: Billing Portal Downloads ($50,083.51)

Items with `pending` receipt status and amount >= $500:

| Merchant | Count | Total | Portal | Status |
|----------|-------|-------|--------|--------|
| Google Cloud | 6 | $58,518.97 | console.cloud.google.com/billing | ✅ DONE - 10 PDFs |
| Anthropic | 10 | $16,185.94 | console.anthropic.com/settings/billing | Pending |
| Zoom | 2 | $3,293.68 | zoom.us/account/billing | Pending |
| Pausa Bar | 1 | $1,224.77 | (CC statement backup) | Pending |

---

## By Source Card

| Card | Count | Amount |
|------|-------|--------|
| Amex | 129 | $95,113.15 |
| Chase | 659 | $85,982.30 |
| Credit (receipt photos) | 32 | $5,202.36 |
| Visa 2030 | 13 | $1,491.10 |
| Chase Visa 2030 | 2 | $650.00 |
| Other | 3 | $194.16 |

---

## By Month (New Expenses Only)

| Month | Count | Amount |
|-------|-------|--------|
| 2024-11 | 1 | $54.75 |
| 2025-01 | 38 | $2,878.74 |
| 2025-02 | 35 | $1,949.45 |
| 2025-03 | 48 | $6,144.44 |
| 2025-04 | 46 | $4,142.10 |
| 2025-05 | 48 | $10,012.84 |
| 2025-06 | 41 | $3,393.24 |
| 2025-07 | 56 | $6,902.04 |
| 2025-08 | 129 | $29,686.05 |
| 2025-09 | 130 | $24,896.78 |
| 2025-10 | 147 | $45,229.81 |
| 2025-11 | 79 | $28,347.84 |
| 2025-12 | 39 | $20,322.02 |
| 2026-01 | 1 | $4,672.97 |

---

## Top 20 Merchants (New Expenses)

| Merchant | Count | Amount | Receipt Status |
|----------|-------|--------|----------------|
| Google Cloud | 4 | $29,345.97 | pending |
| Anthropic | 18 | $21,407.44 | mixed |
| Delta Air Lines | 42 | $16,066.09 | mixed |
| Amazon | 66 | $14,223.73 | mixed |
| Apple | 17 | $11,934.73 | found/email |
| Vanta | 3 | $10,500.00 | found |
| DoorDash | 199 | $8,492.25 | mixed |
| Uplift Desk | 2 | $7,261.56 | found |
| Apple.com | 2 | $6,763.90 | found |
| Airbnb | 4 | $4,981.38 | found/email |
| Hotels.com | 9 | $4,174.03 | mixed |
| Zoom | 9 | $3,845.26 | pending |
| Apple Store | 1 | $3,558.31 | found |
| IKEA | 1 | $3,032.24 | email_available |
| HotelTonight | 6 | $2,272.00 | found |
| Framework | 1 | $2,257.00 | found |
| Park MGM | 1 | $2,118.91 | found |
| Restaurant (photos) | 3 | $2,028.62 | photo |
| Chase Travel | 2 | $1,910.19 | mixed |
| Lyft | 40 | $1,733.67 | pending/email |

---

## Verification Checklist

### Credit Card Reconciliation
- [ ] Amex total in expenses ($95,113) vs Amex statements
- [ ] Chase total in expenses ($85,982) vs Chase statements
- [ ] Verify no missing charges from Dec 2025 statements

### Receipt Collection
- [ ] Download 37 invoices from billing portals ($86,919)
- [ ] Forward 170+ email receipts (~$8,000)
- [ ] 50 photo receipts already processed ($7,038)
- [ ] CC statement backup for remaining (~$10,000)

### Ramp Submission
- [ ] REMOVE 6 already-reimbursed items ($32,994.62)
- [ ] Submit net new expenses ($188,633.07)
- [ ] Verify deposit matches expected amount

---

## Files Reference

| File | Description |
|------|-------------|
| `MASTER_EXPENSE_RECONCILIATION.csv` | All 844 expenses with ramp_status column |
| `EXPENSE_REVIEW.csv` | Simplified view sorted by status (duplicates first) |
| `expenses_to_submit.csv` | Original expense list |
| `michael_dangelo_expenses.csv` | Ramp reimbursement history (310 items, $83,469) |
| `RECEIPT_AUDIT_REPORT.md` | Gmail receipt matching analysis |
| `EXPENSE_TODO.md` | Task tracking and notes |

---

## Math Verification

```
Ramp Already Reimbursed (Jun'24-Jul'25):    $  83,468.87
+ New Expenses to Submit:                    $ 188,633.07
= GRAND TOTAL ALL EXPENSES:                  $ 272,101.94

Expense CSV Original Total:                  $ 221,627.69
- Duplicates (already reimbursed):           $  32,994.62
= Net New to Submit:                         $ 188,633.07  ✓
```
