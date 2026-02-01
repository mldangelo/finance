# Receipt Audit Report - Gmail Cross-Reference

**Generated:** January 3, 2026
**Expense CSV:** 844 expenses, $221,418.65
**Pending Receipts:** 444 items ($104,328)

---

## Executive Summary

| Category | Pending in CSV | Found in Gmail | Match Rate | Action Needed |
|----------|----------------|----------------|------------|---------------|
| DoorDash | 78 | 50+ | ~65% | Forward receipts |
| Lyft | 23 | 30+ | 100%+ | Match & forward |
| Uber | 17 | 30+ | 100%+ | Match & forward |
| Delta Flights | 6 | 50+ | 100% | Forward receipts |
| **Billing Portals** | 37 | 0 | 0% | Download from portals |

---

## SECTION 1: MATCHED RECEIPTS (Ready to Forward)

### Delta Flights - 6 Pending, All Matched

| Expense Date | Amount | Description | Gmail ID | Email Date |
|--------------|--------|-------------|----------|------------|
| 2025-11-24 | $588.18 | JFK→SLC→SAN Dec 1 | `19ab24ea75b7e1e1` | Nov 23 |
| 2025-12-09 | $617.97 | JFK↔SFO Dec 14 RT | `19afcde43aa3498a` | Dec 8 |
| 2025-11-02 | -$619.97 | Flight Credit/Refund | N/A | Credit applied |

**Action:** Forward all Delta receipts: `from:DeltaAirLines@t.delta.com subject:"Flight Receipt" 2025`

### Uber - 17 Pending, 30+ Found

Gmail IDs for December 2025 Uber trips (sample):
- `19b4bda6289734d1` - Dec 22
- `19b499ba78f7d1a6` - Dec 22
- `19b40cb4d0e5545b` - Dec 20
- `19b3e7de97053501` - Dec 20
- `19b23ad2ee154c72` - Dec 15
- `19b2169a13f8a483` - Dec 15
- `19b013bb906620d3` - Dec 9
- `19afeeafc1944ca7` - Dec 8
- ... and 20+ more

**Action:** Forward all: `from:uber.com receipt 2025`

### Lyft - 23 Pending, 30+ Found

Gmail IDs for Lyft receipts (sample):
- `19b4c61e062b98d4` - Dec 22 daily receipt
- `19b497381236e379` - Dec 22 ride
- `19b47f08ef0791fa` - Dec 22 ride
- `19b41983b4e4c8bc` - Dec 20 daily receipt
- `19b37b724316e458` - Dec 18 daily receipt
- ... and 25+ more including Lyft Bike rides

**Action:** Forward all: `from:lyftmail.com receipt 2025`

### DoorDash - 78 Pending, 50+ Found

Gmail IDs for DoorDash orders (sample from Dec 2025):
- `19b765e04dfa00cd` - Levain Bakery Dec 31
- `19b6cb0cca6060a3` - Soothr Thai Dec 30
- `19b479acf5368520` - Ox9 Lanzhou Dec 22
- `19b46ff1b6d5d006` - KOBA Korean BBQ Dec 22
- `19b4483aee526048` - Target Dec 22
- `19b3e38595497f1f` - CVS Dec 21
- `19b3df297bda9b94` - Non La Dec 20
- `19b3788451aa4dc5` - Dim Sum Sam Dec 19
- `19b332f040eaecc7` - Hummus Mediterranean Dec 18
- ... and 40+ more

**Action:** Forward all: `from:no-reply@doordash.com 2025`

---

## SECTION 2: BILLING PORTAL ITEMS (No Email Receipts)

These merchants do NOT send email receipts - must download from billing portals:

### Google Cloud Platform - $58,519 (6 items pending)

| Date | Amount | Portal |
|------|--------|--------|
| 2025-04-01 | $14,500.00 | console.cloud.google.com/billing |
| 2025-07-01 | $14,673.00 | console.cloud.google.com/billing |
| 2025-10-01 | $14,500.00 | console.cloud.google.com/billing |
| 2025-11-01 | $173.00 | console.cloud.google.com/billing |
| 2025-12-31 | $10,000.00 | console.cloud.google.com/billing |
| 2026-01-01 | $4,672.97 | console.cloud.google.com/billing |

### Anthropic API - $22,657 (12 items pending)

| Date | Amount | Portal |
|------|--------|--------|
| 2025-08-12 | $2,500.00 | console.anthropic.com/settings/billing |
| 2025-08-15 | $1,502.14 | console.anthropic.com/settings/billing |
| 2025-09-02 | $1,501.80 | console.anthropic.com/settings/billing |
| 2025-09-17 | $1,500.15 | console.anthropic.com/settings/billing |
| 2025-10-01 | $1,500.07 | console.anthropic.com/settings/billing |
| 2025-10-16 | $1,500.88 | console.anthropic.com/settings/billing |
| 2025-11-10 | $1,500.22 | console.anthropic.com/settings/billing |
| 2025-11-26 | $1,500.72 | console.anthropic.com/settings/billing |
| 2025-11-29 | $545.78 | console.anthropic.com/settings/billing |
| 2025-12-07 | $435.75 | console.anthropic.com/settings/billing |
| 2025-12-10 | $435.89 | console.anthropic.com/settings/billing |
| 2025-12-20 | $1,634.18 | console.anthropic.com/settings/billing |

### Zoom - $3,845 (9 items pending)

| Date | Amount | Portal |
|------|--------|--------|
| 2025-04-24 | $100.75 | zoom.us/account/billing |
| 2025-04-24 | $100.76 | zoom.us/account/billing |
| 2025-06-25 | $165.70 | zoom.us/account/billing |
| 2025-08-22 | $66.88 | zoom.us/account/billing |
| 2025-09-12 | $54.23 | zoom.us/account/billing |
| 2025-10-16 | $33.14 | zoom.us/account/billing |
| 2025-10-22 | $30.12 | zoom.us/account/billing |
| 2025-12-10 | $2,418.90 | zoom.us/account/billing |
| 2025-12-12 | $874.78 | zoom.us/account/billing |

### OpenAI - $871 (5 items pending)

| Date | Amount | Portal |
|------|--------|--------|
| 2025-08-03 | $217.75 | platform.openai.com/account/billing |
| 2025-09-03 | $217.75 | platform.openai.com/account/billing |
| 2025-10-03 | $217.75 | platform.openai.com/account/billing |
| 2025-11-03 | $217.75 | platform.openai.com/account/billing |

### Comcast/Xfinity - $1,027 (5 items pending)

| Date | Amount | Portal |
|------|--------|--------|
| 2025-08-02 | $369.22 | business.comcast.com/myaccount |
| 2025-09-03 | $219.27 | business.comcast.com/myaccount |
| 2025-10-03 | $219.27 | business.comcast.com/myaccount |
| 2025-11-03 | $219.27 | business.comcast.com/myaccount |

---

## SECTION 3: ITEMS NOT FOUND IN GMAIL

### Vanta - $14,000 (4 quarterly invoices)
- Q1: $3,500 (Jan 30) - No email receipt found
- Q2: $3,500 (May 1) - No email receipt found
- Q3: $3,500 (Jul 24) - No email receipt found
- Q4: $3,500 (Oct 23) - No email receipt found

**Action:** Check Vanta billing portal or request invoices from support

### Wellfound Recruit Pro - Found 10 Monthly Invoices
Gmail search found Wellfound invoices Mar-Dec 2025 at $149/mo
**Action:** Forward: `from:wellfound invoice 2025`

### Sentry - No Invoices Found
Only error notification emails, no billing receipts
**Action:** Check Sentry billing portal

---

## SECTION 4: PRIORITY ACTION ITEMS

### HIGH PRIORITY (Billing Portals - $86,919)

1. **Google Cloud** - Download 6 invoices from console.cloud.google.com
2. **Anthropic** - Download 12 invoices from console.anthropic.com
3. **Zoom** - Download 9 invoices from zoom.us
4. **OpenAI** - Download 4 invoices from platform.openai.com
5. **Comcast** - Download 5 invoices from business.comcast.com

### MEDIUM PRIORITY (Email Forwards - ~$5,000)

1. **Delta Flights** - Forward all 50+ flight receipts
   ```
   from:DeltaAirLines@t.delta.com subject:"Flight Receipt" 2025
   ```

2. **Uber** - Forward all 30+ ride receipts
   ```
   from:uber.com receipt 2025
   ```

3. **Lyft** - Forward all 30+ ride receipts
   ```
   from:lyftmail.com receipt 2025
   ```

4. **DoorDash** - Forward all 50+ order receipts
   ```
   from:no-reply@doordash.com 2025
   ```

5. **Wellfound** - Forward 10 monthly invoices
   ```
   from:wellfound invoice 2025
   ```

### LOW PRIORITY (CC Statement Backup)

For items with no email receipt AND no portal access, use credit card statement as backup documentation.

---

## SECTION 5: GMAIL FORWARDING INSTRUCTIONS

Forward receipts to: **receipts@ramp.com**

### Bulk Forward Script (Gmail)

1. Search using query above
2. Select all conversations
3. Forward to receipts@ramp.com
4. Include original email headers

### Manual Forward Priority

| Priority | Merchant | Query | Est. Count |
|----------|----------|-------|------------|
| 1 | Delta | `from:DeltaAirLines@t.delta.com subject:"Flight Receipt" 2025` | 50+ |
| 2 | DoorDash | `from:no-reply@doordash.com 2025` | 50+ |
| 3 | Uber | `from:uber.com receipt 2025` | 30+ |
| 4 | Lyft | `from:lyftmail.com receipt 2025` | 30+ |
| 5 | Wellfound | `from:wellfound invoice 2025` | 10 |

---

## Summary

| Category | Items | Amount | Status |
|----------|-------|--------|--------|
| Billing Portal Required | 37 | $86,919 | Manual download needed |
| Email Receipts Available | 170+ | ~$8,000 | Ready to forward |
| CC Statement Backup | ~200 | ~$9,000 | Use statement as receipt |
| Photo Receipts Added | 50 | $7,038 | Already processed |
| **Total Pending** | **444** | **$104,328** | |

---

## Next Steps

1. [ ] Download invoices from 5 billing portals
2. [ ] Forward Delta flight receipts (50+)
3. [ ] Forward DoorDash receipts (50+)
4. [ ] Forward Uber/Lyft receipts (60+)
5. [ ] Forward Wellfound invoices (10)
6. [ ] Request Vanta invoices from support
7. [ ] Check Sentry billing portal
8. [ ] Update expense CSV with receipt_email_id values
