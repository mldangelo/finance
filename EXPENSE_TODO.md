# Expense Reimbursement Todo List

**Generated:** December 23, 2025
**Status:** 750 expenses, $187,958.39

---

## IMMEDIATE FIXES NEEDED

### Data Corrections
- [x] ~~Remove IKEA duplicate (08-23 Chase $3,032.24)~~ - DONE
- [x] ~~Add missing GCP April charge ($14,500)~~ - DONE Dec 23
- [x] ~~Add missing GCP July charge ($14,673)~~ - DONE Dec 23
- [x] ~~Add 4 missing Anthropic charges (Nov 26 $1,500.72, Nov 29 $545.78, Dec 7 $435.75, Dec 10 $435.89)~~ - DONE Dec 23
- [ ] Verify Claude.ai $1,088.75 is business expense (5 monthly charges)

**Current total: $187,958.39 (750 expenses)**

---

## PHASE 1: Billing Portal Downloads ($28,889)
*No email receipts exist - must download from portals manually*

| Priority | Merchant | Items | Amount | Portal URL | Status |
|----------|----------|-------|--------|------------|--------|
| 1 | Google Cloud | 16+ | $43,846 | console.cloud.google.com/billing | [ ] |
| 2 | Anthropic API | 16 | $19,523 | console.anthropic.com/settings/billing | [ ] |
| 3 | Comcast/Xfinity | 4 | $1,027 | business.comcast.com/myaccount | [ ] |
| 4 | OpenAI | 4 | $871 | platform.openai.com/account/billing | [ ] |
| 5 | Zoom | 7 | $552 | zoom.us/account/billing | [ ] |

**Action:** Download PDF invoices for each month and forward to receipts@ramp.com

---

## PHASE 2: Forward Critical Email Receipts ($17,740)
*Forward these 6 emails to receipts@ramp.com FIRST*

| Email ID | Date | Merchant | Amount | Status |
|----------|------|----------|--------|--------|
| `19b304f1cb8d562d` | Dec 18 | Delta | $607.97 | [ ] |
| `19a11085fd1c3440` | Oct 23 | Vanta Q4 | $3,500 | [ ] |
| `1983c5ca0a64501d` | Jul 24 | Vanta Q3 | $3,500 | [ ] |
| `19689cdd543bccbd` | May 01 | Vanta Q2 | $3,500 | [ ] |
| `194b87d9fdc26529` | Jan 30 | Vanta Q1 | $3,500 | [ ] |
| `198d8e2dce71047b` | Aug 23 | IKEA | $3,032 | [ ] |

---

## PHASE 3: Forward High Priority Receipts (~$15,000)

### Delta Flights (68 receipts)
- [ ] Forward all from DeltaAirLines@t.delta.com
- Gmail: `from:DeltaAirLines@t.delta.com subject:"Flight Receipt" 2025`

### Apple Equipment/Subscriptions (50 receipts)
- [ ] Forward from no_reply@email.apple.com
- Gmail: `from:no_reply@email.apple.com subject:receipt 2025`

### Wellfound Recruit Pro (10 receipts)
- [ ] Forward monthly invoices ($149/mo)
- Gmail: `from:wellfound invoice 2025`

### Sentry (13 receipts)
- [ ] Forward Promptfoo subscription receipts
- Gmail: `from:getsentry.com 2025`

---

## PHASE 4: Match Rideshare Receipts ($5,000)

### DoorDash (78 items, $3,766)
- [ ] Search: `from:doordash.com receipt 2025`
- [ ] Match dates/amounts to expenses
- [ ] Forward matched receipts

### Lyft (23 items, $813)
- [ ] Search: `from:lyftmail.com 2025`
- [ ] Match and forward

### Uber (18 items, $380)
- [ ] Search: `from:uber.com ride receipt 2025`
- [ ] Match and forward

---

## PHASE 5: CC Statement Backup ($4,200)
*No email receipts - use CC statement as backup*

| Merchant | Items | Amount | Status |
|----------|-------|--------|--------|
| Pausa Bar | 1 | $1,225 | [ ] |
| Chase Travel | 1 | $484 | [ ] |
| Mitr Thai | 1 | $459 | [ ] |
| Garaje | 7 | $437 | [ ] |
| Gyu-Kaku | 1 | $357 | [ ] |
| Other restaurants | 20 | $1,238 | [ ] |

**Action:** Export Chase statement, highlight transactions, forward to Ramp

---

## SUMMARY

| Phase | Action | Amount | Priority | Status |
|-------|--------|--------|----------|--------|
| Fixes | Add missing GCP/Anthropic | +$32,091 | CRITICAL | ✅ DONE |
| 1 | Billing portal downloads | $65,800 | HIGH | Pending |
| 2 | Critical email receipts | $17,740 | HIGH | Pending |
| 3 | High priority emails | ~$15,000 | MEDIUM | Pending |
| 4 | Rideshare matching | $5,000 | MEDIUM | Pending |
| 5 | CC statement backup | $4,200 | LOW | Pending |

---

## FILES REFERENCE

| File | Purpose |
|------|---------|
| `expenses_to_submit.csv` | Master expense list (750 items, $187,958) |
| `receipts_to_forward.csv` | 301 receipt emails with IDs |
| `TRAVEL_LOG_2025.md` | Complete travel log with flights, hotels, days by city |
| `chase/*.pdf` | 11 Chase statements (Jan-Nov) |
| `boa/*.pdf` | 12 BoA statements (Jan-Dec) |
| `amex/activity.xlsx` | Amex transactions (226 items) |

---

## NOTES

1. **GCP has no email receipts** - Must download from console.cloud.google.com
2. **Anthropic API vs Claude.ai** - API charges ($19.5K) are different from Claude.ai subscription ($1K)
3. **IKEA duplicate removed** - Was double-counted on both Chase and Amex
4. **Statement cutoff** - Chase data ends Nov 17, some Dec expenses unverifiable
