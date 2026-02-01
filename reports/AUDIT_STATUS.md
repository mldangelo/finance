# Comprehensive Expense Audit Status

**Generated:** January 3, 2026 (Updated)
**Current CSV:** 848 items, $221,814.48

---

## RECEIPT STATUS SUMMARY

| Status | Count | Amount | Action |
|--------|-------|--------|--------|
| **found** | 150 | $149,360.09 | Ready to submit |
| **pending** | 442 | $46,205.02 | Need receipts |
| **email_available** | 205 | $19,211.45 | Forward emails |
| **photo** | 50 | $7,037.95 | Photos ready |
| **TOTAL** | **848** | **$221,814.48** | |

---

## COMPLETED AUDITS

### 1. Google Cloud Invoices - DONE
- 10 PDF invoices extracted (Mar-Dec 2025)
- $58,518.97 in user's Amex charges
- All 6 CSV entries updated with receipt file paths
- Mastercard 7204 payments ($779.91) confirmed NOT user's card

### 2. Receipt Photos - DONE
- 50 receipts from Photos-1-001.zip
- $7,037.95 added to CSV
- Personal items excluded (Arc'teryx, Bouchon Bistro, P.C. Richard)

### 3. Amex 90-Day Reconciliation - DONE
- 19 expenses added (+$19,836)
- GCP Dec/Jan, Anthropic, Claude.ai, Delta, Hotels, ElevenLabs, Recruit Pro

### 4. Ramp Duplicate Detection - DONE
- 6 items ($32,994.62) already reimbursed via Ramp
- Marked as ALREADY_REIMBURSED in MASTER_EXPENSE_RECONCILIATION.csv

### 5. Chase Dec Statement Reconciliation - DONE
- Reviewed all transactions from 11/18/25 - 12/17/25
- 4 business items added: TaskRabbit x3 ($256.14), VIO.COM ($139.69)
- 4 personal items excluded: Keens ($458), East Village x2 ($945), Away ($167)

---

## CHASE DEC STATEMENT DETAILS

### From Chase Dec Statement (11/18 - 12/17/25)

| Date | Merchant | Amount | Status | Resolution |
|------|----------|--------|--------|------------|
| 11/27 | Keens Steakhouse NYC | $458.15 | PERSONAL | Not added |
| 11/21 | PY *EAST VILLAGE | $665.00 | PERSONAL | Not added |
| 11/28 | PY *EAST VILLAGE | $280.00 | PERSONAL | Not added |
| 11/27 | TaskRabbit | $45.21 | ✅ ADDED | CA = business |
| 11/29 | TaskRabbit | $144.07 | ✅ ADDED | CA = business |
| 12/10 | TaskRabbit | $66.86 | ✅ ADDED | CA = business |
| 12/07 | VIO.COM | $139.69 | ✅ ADDED | NeurIPS hotel |
| 11/30 | SP AWAY Travel | $166.59 | PERSONAL | Not added |

**Business expenses added: $395.83 (4 items)**
**Personal expenses excluded: $1,569.74 (4 items)**

### Items Confirmed in CSV (from Dec statement)
- Zoom $2,418.90 + $874.78 ✓
- Pausa Bar $1,224.77 ✓ (but listed as $246.29 - different transaction?)
- Alaska Air $341.60 ✓
- Southwest $363.30 ✓
- NeurIPS $1,200.00 ✓
- HotelTonight Timbri $555.00 ✓
- Gyu-Kaku $479.62 ✓ (photo receipt)

---

## BILLING PORTAL DOWNLOADS NEEDED

| Merchant | Pending Items | Amount | Portal | Priority |
|----------|---------------|--------|--------|----------|
| Google Cloud | 0 | $0 | ✅ DONE | - |
| Anthropic | 12 | $16,057.58 | console.anthropic.com | HIGH |
| Zoom | 9 | $3,845.26 | zoom.us/account/billing | HIGH |
| Comcast | 5 | $1,246.30 | business.comcast.com | MEDIUM |
| OpenAI | 5 | $1,088.75 | platform.openai.com | MEDIUM |
| **TOTAL** | **31** | **$22,237.89** | | |

---

## EMAIL RECEIPTS TO FORWARD

| Merchant | Pending | Amount | Gmail Query |
|----------|---------|--------|-------------|
| DoorDash | 78 | $3,766.25 | `from:doordash.com 2025` |
| Delta | 6 | $1,614.14 | `from:delta subject:"Flight Receipt" 2025` |
| Hotels.com | 3 | $982.77 | `from:hotels.com receipt 2025` |
| Lyft | 23 | $813.26 | `from:lyftmail.com 2025` |
| Uber | 17 | $356.20 | `from:uber.com receipt 2025` |
| Claude.ai | 3 | $653.25 | `from:anthropic subject:receipt` |
| **TOTAL** | **130** | **$8,185.87** | |

---

## ITEMS LIKELY PERSONAL (Do NOT add)

From Chase Dec statement - these appear personal:
- J CREW purchases (~$430 total) - clothing
- ClassPass $93.01 - fitness
- Lemonade Insurance $88.25 - personal insurance
- Capsule Pharmacy $25.41 - medical
- Mount Sinai $30.00 - medical
- Spectrum $29.99 - home TV/internet
- Hulu $18.99 - streaming
- Peacock $10.99 - streaming
- Netflix $19.56 - streaming

---

## DATA SOURCES STATUS

| Source | Statements | Period | Status |
|--------|------------|--------|--------|
| Chase Visa 2030 | 13 | Jan-Dec 2025 | ✅ Reconciled |
| Amex | 1 (90-day) | Oct-Jan | ✅ Reconciled |
| BoA | 12 | Jan-Dec 2025 | ✅ N/A (checking only) |
| Receipt Photos | 1 zip | Various | ✅ Processed |
| Google Cloud | 10 PDFs | Mar-Dec 2025 | ✅ Processed |
| Ramp History | 1 CSV | Jun'24-Jul'25 | ✅ Cross-referenced |

---

## PRIORITY ACTION ITEMS

### ✅ CRITICAL - Verify Missing Items - DONE
1. [x] **Keens Steakhouse** ($458.15) - PERSONAL
2. [x] **PY *East Village** ($665 + $280 = $945) - PERSONAL
3. [x] **TaskRabbit** ($256.14) - BUSINESS (CA) - Added to CSV
4. [x] **VIO.COM** ($139.69) - BUSINESS (NeurIPS hotel) - Added to CSV
5. [x] **SP AWAY Travel** ($166.59) - PERSONAL

### HIGH - Download Billing Portal Invoices ($22,238)
1. [ ] Anthropic - 12 invoices ($16,058)
2. [ ] Zoom - 9 invoices ($3,845)
3. [ ] Comcast - 5 invoices ($1,246)
4. [ ] OpenAI - 5 invoices ($1,089)

### MEDIUM - Forward Email Receipts ($8,186)
1. [ ] DoorDash - 78 receipts ($3,766)
2. [ ] Delta - 6 receipts ($1,614)
3. [ ] Hotels.com - 3 receipts ($983)
4. [ ] Lyft - 23 receipts ($813)
5. [ ] Uber - 17 receipts ($356)
6. [ ] Claude.ai - 3 receipts ($653)

### LOW - CC Statement Backup
For items with no email/portal receipts, use credit card statement as documentation.

---

## FINANCIAL RECONCILIATION

```
Expense CSV Total:                    $221,814.48
- Already Reimbursed (Ramp):          -$32,994.62
= Net New to Submit:                  $188,819.86

Chase Dec Statement:
  + Business items added:             +$395.83 (TaskRabbit x3, VIO.COM)
  - Personal items excluded:          -$1,569.74 (not added)
```

---

## NEXT STEPS

1. ✅ **DONE:** Chase Dec statement items classified (business vs personal)

2. **Download invoices** from Anthropic, Zoom, Comcast, OpenAI portals

3. **Forward email receipts** for DoorDash, Delta, Hotels.com, Lyft, Uber

4. **Final reconciliation** once all receipts collected
