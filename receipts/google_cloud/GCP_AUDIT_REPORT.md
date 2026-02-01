# Google Cloud Invoice Audit Report

**Generated:** January 3, 2026
**Source:** google-payments-document-center-download_202601032232.zip
**Invoices:** 10 PDF statements (Mar-Dec 2025)

---

## Invoice Data Summary

| Month | New Activity | Payments | Ending Balance | Payment Card |
|-------|-------------|----------|----------------|--------------|
| Mar 2025 | $606.91 | $300.00 | $306.91 | Mastercard 7204 |
| Apr 2025 | $14,673.00 | $14,979.91 | $0.00 | Amex 1003 ($14,500) + MC 7204 ($479.91) |
| May 2025 | $0.00 | $0.00 | $0.00 | - |
| Jun 2025 | $0.00 | $0.00 | $0.00 | - |
| Jul 2025 | $14,673.00 | $14,673.00 | $0.00 | Amex 1003 |
| Aug 2025 | $0.00 | $0.00 | $0.00 | - |
| Sep 2025 | $0.00 | $0.00 | $0.00 | - |
| Oct 2025 | $14,673.00 | $14,500.00 | $173.00 | Amex 1003 |
| Nov 2025 | -$0.01 | $173.00 | -$0.01 | Amex 1003 |
| Dec 2025 | $14,672.98 | $10,000.00 | $4,672.97 | Amex 1003 |
| **TOTALS** | **$59,298.88** | **$54,625.91** | **$4,672.97** | |

---

## Expense CSV Comparison

### Current GCP Entries in expenses_to_submit.csv:

| ID | Date | Amount | Status | Ramp Status |
|----|------|--------|--------|-------------|
| EXP-2025-04-01-001 | 2025-04-01 | $14,500.00 | pending | ALREADY_REIMBURSED |
| EXP-2025-07-01-001 | 2025-07-01 | $14,673.00 | pending | ALREADY_REIMBURSED |
| EXP-2025-10-01-001 | 2025-10-01 | $14,500.00 | pending | NOT_REIMBURSED |
| EXP-2025-11-01-001 | 2025-11-01 | $173.00 | pending | NOT_REIMBURSED |
| EXP-2025-12-31-001 | 2025-12-31 | $10,000.00 | pending | NOT_REIMBURSED |
| EXP-2026-01-01-001 | 2026-01-01 | $4,672.97 | pending | NOT_REIMBURSED |
| **CSV Total** | | **$58,518.97** | | |

---

## DISCREPANCIES RESOLVED

### Mastercard 7204 Payments - NOT USER'S CARD

The March/April 2025 invoices show $779.91 paid from Mastercard ...7204:
- Mar 2025: $300.00
- Apr 2025: $479.91

**CONFIRMED:** Mastercard 7204 is **NOT the user's card**. These payments were made by someone else (company card, previous owner, etc.).

**Result:** The expense CSV correctly includes ONLY Amex 1003 payments, which are the user's reimbursable expenses.

### Payment Timing Notes

- **April 2025:** Invoice activity was $14,673, but user's Amex paid $14,500 (the Mastercard covered the rest)
- **October 2025:** Invoice activity was $14,673, but Amex paid $14,500 (remaining $173 paid in November)
- All amounts in expense CSV correctly reflect actual Amex charges

---

## RECONCILIATION SUMMARY

### Amex Payments (What's in CSV)

| Month | Amex Payment | In CSV | Match |
|-------|-------------|--------|-------|
| Apr 2025 | $14,500.00 | $14,500.00 | ✓ |
| Jul 2025 | $14,673.00 | $14,673.00 | ✓ |
| Oct 2025 | $14,500.00 | $14,500.00 | ✓ |
| Nov 2025 | $173.00 | $173.00 | ✓ |
| Dec 2025 | $10,000.00 | $10,000.00 | ✓ |
| Jan 2026 | $4,672.97* | $4,672.97 | ✓ |
| **Total** | **$58,518.97** | **$58,518.97** | ✓ |

*Outstanding balance, expected to be charged

### Mastercard Payments (NOT User's Card - No Action Needed)

| Month | MC Payment | In CSV | Status |
|-------|-----------|--------|--------|
| Mar 2025 | $300.00 | N/A | Not user's card |
| Apr 2025 | $479.91 | N/A | Not user's card |
| **Total** | **$779.91** | **N/A** | **Paid by other party** |

---

## ACTION ITEMS

### 1. Mastercard 7204 - RESOLVED
- [x] Verified: Mastercard 7204 is NOT user's card
- [x] No additional expenses to add - CSV is correct

### 2. Update Receipt File Paths - DONE
All GCP expenses should have receipt_file updated to point to invoices:

| Expense ID | Receipt File |
|------------|--------------|
| EXP-2025-04-01-001 | receipts/google_cloud/8342400783419062_20250430.pdf |
| EXP-2025-07-01-001 | receipts/google_cloud/8342400783419062_20250731.pdf |
| EXP-2025-10-01-001 | receipts/google_cloud/8342400783419062_20251031.pdf |
| EXP-2025-11-01-001 | receipts/google_cloud/8342400783419062_20251130.pdf |
| EXP-2025-12-31-001 | receipts/google_cloud/8342400783419062_20251231.pdf |
| EXP-2026-01-01-001 | receipts/google_cloud/8342400783419062_20251231.pdf |

### 3. Already Reimbursed (Do Not Resubmit)
- EXP-2025-04-01-001: $14,500.00 - Already in Ramp
- EXP-2025-07-01-001: $14,673.00 - Already in Ramp

---

## FINANCIAL SUMMARY

| Category | Amount |
|----------|--------|
| Total GCP Activity (Mar-Dec 2025) | $59,298.88 |
| Less: Paid by other party (MC 7204) | -$779.91 |
| **User's GCP Charges (Amex 1003)** | **$58,518.97** |
| Already Reimbursed via Ramp | -$29,173.00 |
| **Net New to Submit** | **$29,345.97** |

### Breakdown of User's Amex Charges:

| Period | Amount | Status |
|--------|--------|--------|
| Apr 2025 | $14,500.00 | ALREADY_REIMBURSED |
| Jul 2025 | $14,673.00 | ALREADY_REIMBURSED |
| Oct 2025 | $14,500.00 | NOT_REIMBURSED |
| Nov 2025 | $173.00 | NOT_REIMBURSED |
| Dec 2025 | $10,000.00 | NOT_REIMBURSED |
| Jan 2026 | $4,672.97 | NOT_REIMBURSED (outstanding) |

**Already Reimbursed:** $29,173.00 (Apr + Jul)
**Net New to Submit:** $29,345.97 (Oct + Nov + Dec + Jan)

---

## PDF Invoice Files

| File | Period | Status |
|------|--------|--------|
| 8342400783419062_20250331.pdf | Mar 2025 | ✓ Extracted |
| 8342400783419062_20250430.pdf | Apr 2025 | ✓ Extracted |
| 8342400783419062_20250531.pdf | May 2025 | ✓ Extracted |
| 8342400783419062_20250630.pdf | Jun 2025 | ✓ Extracted |
| 8342400783419062_20250731.pdf | Jul 2025 | ✓ Extracted |
| 8342400783419062_20250831.pdf | Aug 2025 | ✓ Extracted |
| 8342400783419062_20250930.pdf | Sep 2025 | ✓ Extracted |
| 8342400783419062_20251031.pdf | Oct 2025 | ✓ Extracted |
| 8342400783419062_20251130.pdf | Nov 2025 | ✓ Extracted |
| 8342400783419062_20251231.pdf | Dec 2025 | ✓ Extracted |

All invoices extracted to: `/Users/mdangelo/projects/finance/receipts/google_cloud/`
