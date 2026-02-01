# Expense Gap Analysis - What We Know and Don't Know
**Generated:** December 17, 2025
**Analysis Period:** August 1 - December 17, 2025

---

## Summary: Data Completeness

| Source | Status | Gap |
|--------|--------|-----|
| Chase Credit Card | 76.5% verified | 23.5% on Amex (expected) |
| Bank of America | 100% imported | N/A |
| Ramp Historical | 100% imported | No overlap with current period |
| American Express | **NOT IMPORTED** | Need Amex PDFs |

---

## WHAT WE KNOW (High Confidence)

### 1. Tracked Expenses Summary
| Metric | Value |
|--------|-------|
| Total Expenses | 375 transactions, $94,974.49 |
| Verified against Chase | 287 transactions (76.5%) |
| On Amex (confirmed) | 35 transactions, $38,655.25 |
| On Amex (likely) | 19 transactions, $6,299.66 |
| December (stmt pending) | 15 transactions, $1,311.75 |

### 2. Credit Card Payment Verification
| Check | Status |
|-------|--------|
| Chase payments match bank | **VERIFIED** - $153,014.70 exact |
| Amex payments from bank | $64,454.06 (Aug-Dec) |

### 3. No Duplicate Reimbursements
- Cross-checked against 310 Ramp reimbursements
- Only valid recurring charges found (GCP, Delta monthly)
- **0 duplicates** - all 375 expenses are new

---

## WHAT WE FOUND: Missing Expenses

### Definitely Missing from Expense CSV ($7,942.99)

| Date | Amount | Merchant | Category | Source |
|------|--------|----------|----------|--------|
| 2025-11-13 | $3,855.90 | Apple.com (equipment) | Equipment | Chase |
| 2025-10-11 | $2,248.12 | Airbnb (team lodging) | Travel | Chase |
| 2025-09-21 | $869.91 | Apple Store NYC | Equipment | Chase |
| 2025-10-02 | $305.75 | Minami Restaurant Toronto | Meals | Chase |
| 2025-09-21 | $271.10 | Apple Store NYC | Equipment | Chase |
| 2025-10-12 | $271.10 | Apple Store NYC | Equipment | Chase |
| 2025-08-22 | $66.88 | Zoom.com subscription | Software | Chase |
| 2025-09-12 | $54.23 | Zoom.com subscription | Software | Chase |

### Likely Missing (Smaller Items ~$718)

16 Lyft/Uber rides ranging from $24-$135 each that appear in Chase but not in expense CSV.

### Total Missing from Chase: **$8,661.74**

---

## WHAT WE DON'T KNOW (Gaps & Uncertainties)

### 1. American Express Transactions (HIGH PRIORITY)
- **Gap:** We have no Amex statement data
- **Impact:** Cannot verify $50,543.49 in claimed Amex expenses
- **Bank shows:** $64,454.06 in Amex payments (Aug-Dec)
- **Difference:** $13,910.57 unaccounted (could be personal or missing business)
- **Action:** Import Amex PDF statements

### 2. Chase Data Cutoff (MEDIUM)
- **Gap:** Chase statement ends November 17, 2025
- **Impact:** Cannot verify 15 December expenses ($1,311.75)
- **Action:** Import December Chase statement when available

### 3. Potential Chase Issues (8 items, $272.48)
These have matching amounts in Chase but failed matching due to date/merchant discrepancies:

| Expense | Chase Entry | Issue |
|---------|-------------|-------|
| Tang Bar $60.89 | Same date, same merchant | Should have matched |
| Amazon $49.33 | Different date (June) | Different transaction |
| City of San Mateo $43.58 | No matching date | Unknown |
| PayByPhone $33.54 | No matching date | Unknown |
| Chaotic Good Cafe $33.50 | Feb date in Chase | Different transaction |
| ElevenLabs $23.95 | Different merchant | May be on different card |
| Donut Delite $14.20 | Oct date in Chase | Different transaction |
| DoorDash $13.49 | Same date, diff merchant | Naming mismatch |

### 4. Unknown Items (11 items, $4,004.35)
Cannot determine payment method for these:

| Date | Amount | Merchant | Notes |
|------|--------|----------|-------|
| 2025-10-23 | $3,500.00 | Vanta | Quarterly billing - valid |
| 2025-11-18+ | ~$500 | DoorDash (6 items) | After Chase stmt cutoff |
| 2025-10-28 | $159.88 | Amazon (2 small) | May be on Amex |
| 2025-11-21+ | ~$55 | Coffee shops (3) | After Chase stmt cutoff |

### 5. Receipt Status
- **324 expenses (83.7%)** have "pending" receipt status
- **55 expenses (14.2%)** have receipts found
- **8 expenses (2.1%)** have receipts attached

---

## Amex Expense Breakdown (Claimed but Unverified)

| Category | Items | Amount | Confidence |
|----------|-------|--------|------------|
| Infrastructure (GCP/Anthropic) | 13 | $27,822.26 | High - matches billing patterns |
| Travel (Delta) | 24 | $11,236.19 | High - no Delta on Chase |
| Travel (Hotels.com) | 5 | $2,404.96 | Medium - could be either card |
| Software (Claude.ai) | 4 | $871.00 | High - subscription pattern |
| Software (Recruit Pro) | 5 | $745.00 | High - subscription pattern |
| Equipment (Amazon large) | 8 | $2,511.91 | Medium - could be either card |

**To verify:** Import Amex statements

---

## Action Items

### Immediate (Before Reimbursement)

1. **Add missing Chase expenses to CSV ($8,661.74)**
   - Apple.com $3,855.90 (Nov 13)
   - Airbnb $2,248.12 (Oct 11)
   - Apple Store $1,412.11 (Sep 21, Oct 12)
   - Toronto restaurant $305.75 (Oct 2)
   - Zoom subscriptions $121.11 (Aug 22, Sep 12)
   - Various Lyft/Uber ~$718

2. **Collect missing receipts**
   - 324 expenses need receipt collection
   - Priority: Large items > $500

3. **Verify Vanta $3,500**
   - Confirm this is a new quarterly charge (not duplicate)
   - Previous charges: Jan, Apr, Jul 2025

### Short-term

4. **Import Amex statements**
   - Verify $50,543.49 in claimed Amex expenses
   - Identify any missing Amex business charges

5. **Import December Chase statement**
   - Verify 15 December expenses ($1,311.75)

### Data Quality

6. **Fix matching issues**
   - Tang Bar - should have matched
   - DoorDash $13.49 - merchant name normalization

---

## Corrected Totals

| Category | Current | After Fixes |
|----------|---------|-------------|
| Total Expenses | $94,974.49 | $103,636.23 |
| Missing to add | - | +$8,661.74 |
| Verified | 76.5% | TBD after Amex import |

---

## Confidence Assessment

| What | Confidence | Notes |
|------|------------|-------|
| Chase transactions tracked | 95% | 287/375 verified, 8 minor issues |
| Amex expenses claimed | 70% | Patterns match but unverified |
| No duplicate reimbursements | 99% | Strict date matching confirms |
| Missing expenses identified | 85% | May be more in Amex |
| Receipt completeness | 16% | 324 pending |
