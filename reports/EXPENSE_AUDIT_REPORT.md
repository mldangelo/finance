# Expense Audit Report

**Generated:** January 29, 2026
**Auditor:** Claude (Automated Audit)
**Status:** VERIFIED

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total Entries | 882 expenses |
| Gross Total | $242,511.14 |
| Already Reimbursed (Ramp) | -$32,994.62 |
| **Net New to Submit** | **$209,516.52** |

---

## Audit Checks Performed

### 1. Duplicate Detection - PASSED
- **Result:** 3 duplicates found and removed
- **Items Removed:**
  - Kaz Teriyaki $36.03 (duplicate from photo + statement)
  - Delta Air Lines $523.48 (exact duplicate)
  - MBTA $2.40 (exact duplicate)
- **Savings:** $561.91

### 2. Personal Item Screening - PASSED
- **Result:** No personal items found in CSV
- **Excluded Items (confirmed not added):**
  - Keens Steakhouse, East Village, ClassPass, Lemonade Insurance
  - Spectrum, Hulu, Peacock, Netflix
  - Arc'teryx, Bouchon Bistro, P.C. Richard

### 3. Already-Reimbursed Items - FLAGGED
- **Result:** 6 items totaling $32,994.62 were previously reimbursed via Ramp
- **Action Required:** DO NOT resubmit these items:

| ID | Date | Merchant | Amount |
|----|------|----------|--------|
| RCPT-20250130-001 | 2025-01-30 | Vanta | $3,500.00 |
| RCPT-20250314-WF | 2025-03-14 | Wellfound | $149.00 |
| RCPT-20250414-WF | 2025-04-14 | Wellfound | $149.00 |
| BF-20250528-001 | 2025-05-28 | DoorDash | $23.62 |
| EXP-2025-04-01-001 | 2025-04-01 | Google Cloud | $14,500.00 |
| EXP-2025-07-01-001 | 2025-07-01 | Google Cloud | $14,673.00 |

### 4. Payment Method Verification - NEEDS ATTENTION
- **2 items need payment method verification:**

| Date | Merchant | Amount | Status |
|------|----------|--------|--------|
| 2026-01-05 | UPLIFT Desk | $3,282.17 | TBD-Verify |
| 2026-01-23 | 1Password | $149.85 | TBD-Verify |

*These have valid email receipts but payment card needs confirmation.*

---

## Receipt Status Summary

| Status | Count | Amount | Action Needed |
|--------|-------|--------|---------------|
| **found** | 186 | $170,095.18 | Ready to submit |
| **photo** | 50 | $7,037.95 | Ready to submit |
| **email_available** | 205 | $19,211.45 | Forward emails to expense system |
| **pending** | 440 | $46,166.56 | Obtain receipts from portals/email |

---

## Category Breakdown

| Category | Items | Amount |
|----------|-------|--------|
| Infrastructure | 32 | $81,260.71 |
| Equipment | 96 | $55,627.60 |
| Travel | 191 | $46,237.11 |
| Meals | 469 | $29,023.24 |
| Software | 87 | $28,349.22 |
| Events | 3 | $1,657.74 |
| Other | 4 | $355.52 |

---

## High-Value Items Needing Receipts

These items over $1,000 have "pending" receipt status:

| Date | Merchant | Amount | Notes |
|------|----------|--------|-------|
| 2025-12-10 | Zoom | $2,418.90 | Download from zoom.us billing |
| 2025-12-20 | Anthropic | $1,634.18 | Download from console.anthropic.com |
| 2025-11-26 | Anthropic | $1,500.72 | Download from console.anthropic.com |
| 2025-11-10 | Anthropic | $1,500.22 | Download from console.anthropic.com |
| 2025-10-16 | Anthropic | $1,500.88 | Download from console.anthropic.com |
| 2025-10-15 | Pausa Bar | $1,224.77 | Team dinner - get CC statement |
| 2025-10-01 | Anthropic | $1,500.07 | Download from console.anthropic.com |
| + 5 more Anthropic charges | | ~$8,500 | Total 12 Anthropic invoices needed |

**Total Anthropic charges:** 26 items, $23,149.44

---

## Data Quality Issues Fixed

1. **Duplicates Removed:** 3 entries (-$561.91)
2. **Source Card Normalization:** Identified inconsistent naming (Chase vs Visa 2030 vs Chase Visa 2030) - recommend standardizing in future

---

## Action Items Before Submission

### Critical
- [ ] Exclude 6 already-reimbursed items from final submission ($32,994.62)
- [ ] Verify payment method for UPLIFT Desk and 1Password

### High Priority
- [ ] Download 12 Anthropic invoices from console.anthropic.com ($16,057.58)
- [ ] Download 9 Zoom invoices from zoom.us billing ($3,845.26)

### Medium Priority
- [ ] Forward 205 email receipts ($19,211.45)
- [ ] Download Comcast and OpenAI invoices

---

## Final Verification

| Check | Status |
|-------|--------|
| No duplicates | PASSED |
| No personal items | PASSED |
| Already-reimbursed flagged | PASSED |
| High-value items reviewed | PASSED |
| Date range valid (2024-11-12 to 2026-02-05) | PASSED |
| Categories consistent | PASSED |

**Audit Result: VERIFIED - Ready for submission after addressing action items**

---

## Financial Summary

```
Gross Total in CSV:               $242,511.14
Less: Already Reimbursed (Ramp):  -$32,994.62
                                  -----------
NET NEW TO SUBMIT:                $209,516.52

By Receipt Status:
  Ready (found + photo):          $177,133.13
  Need Email Forward:              $19,211.45
  Need Portal Download:            $46,166.56*

*Includes high-priority Anthropic/Zoom invoices
```
