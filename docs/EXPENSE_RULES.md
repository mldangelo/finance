# Expense Inclusion Rules and Policies

## General Principles

1. **Business Purpose Required**: Every expense must have a clear business justification
2. **Receipt Required**: All expenses >$25 require receipts
3. **Timely Submission**: Submit within 60 days of expense
4. **No Duplicates**: Check Ramp history before submitting

---

## Location-Based Rules

### San Mateo / Bay Area (INCLUDE ALL)

**Always include** any expense in these locations:
- San Mateo (office location)
- Burlingame
- Palo Alto
- San Francisco
- Daly City
- Redwood City
- Mountain View

**Rationale**: When in the Bay Area, you are working at or traveling to the Promptfoo office. All meals, coffee, transportation, and supplies are business expenses.

**Examples**:
- Philz Coffee San Mateo - INCLUDE
- Blue Bottle Palo Alto - INCLUDE
- Uber from SFO to San Mateo - INCLUDE
- DoorDash delivery to San Mateo - INCLUDE
- Target run for office supplies - INCLUDE

### New York City (SELECTIVE)

**Include**:
- Meals during work hours (9am-6pm weekdays)
- Late night meals (after 9pm) when working
- Airport transit (LIRR, subway to JFK/LGA)
- Uber/Lyft to airports for business travel
- Work-from-home office supplies

**Exclude**:
- ALL grocery deliveries (considered personal)
- Weekend personal meals
- Personal entertainment
- Regular commute costs

**Decision Framework**:
```
Is it a weekday?
  YES → Is it during work hours OR late night work?
    YES → INCLUDE
    NO → Was there a work reason? → INCLUDE if yes
  NO → Was it for travel or work emergency? → INCLUDE if yes
```

### Boston (SELECTIVE)

**Include**:
- Meals during work hours
- MBTA transit for business meetings
- Work-from-home supplies

**Exclude**:
- Personal meals
- Weekend activities
- Grocery deliveries

### Other Locations (BUSINESS TRAVEL ONLY)

**Include**:
- All meals during business trips
- Hotel stays for work
- Ground transportation
- Conference expenses

---

## Category-Specific Rules

### Infrastructure (Always Include)

| Expense Type | Include? | Notes |
|--------------|----------|-------|
| Google Cloud Platform | YES | Critical infrastructure |
| Anthropic/Claude API | YES | Core product development |
| AWS services | YES | Infrastructure |
| Internet service (home office) | YES | Comcast/Xfinity for remote work |
| Coworking (WeWork) | YES | Alternative workspace |

### Travel (Business Purpose Required)

**Flights**:
- All flights between NYC and SF/Bay Area = INCLUDE
- Flights to conferences = INCLUDE
- Personal vacation = EXCLUDE

**Hotels**:
- Bay Area hotels during work trips = INCLUDE
- NYC hotels for Promptfoo business = INCLUDE
- Personal travel = EXCLUDE

**Ground Transportation**:
- Airport rides = INCLUDE
- Rides between meetings = INCLUDE
- Personal errands = EXCLUDE

### Equipment (Office Use)

**Always Include**:
- Computers and laptops for work
- Monitors and displays
- Keyboards, mice, peripherals
- Office furniture (desk, chair)
- Webcams, microphones
- Cables and adapters

**Include if for Office**:
- Coffee makers (San Mateo office)
- Kitchen supplies (office)
- Cleaning supplies (office)

**Exclude**:
- Personal electronics
- Home furniture (unless dedicated office)
- Entertainment devices

### Software Subscriptions

**Always Include**:
- AI development tools (Cursor, Copilot, Replicate)
- Productivity tools (Zoom, Slack)
- Security tools (Vanta)
- HR/recruiting tools (Recruit Pro)
- Cloud storage for work

**Review Carefully**:
- Personal AI subscriptions (ChatGPT, Claude.ai) - include if used for work
- General productivity apps - only if primarily work use

### Meals and Food

**San Mateo Office**:
| Type | Include? |
|------|----------|
| Coffee shops | YES |
| Restaurants | YES |
| DoorDash/delivery | YES |
| Groceries | YES (for office) |
| Team dinners | YES |

**Remote (NYC/Boston)**:
| Type | Include? |
|------|----------|
| Work hour meals | YES |
| Late night work meals | YES |
| Weekend meals | NO |
| Groceries | NO |

**Team Meals**:
- All team meals = INCLUDE
- Flag meals >$500 for review
- Document attendees for large meals

---

## DoorDash Specific Rules

### How to Identify California Orders

Credit card statements show DoorDash as:
```
DOORDASH*[RESTAURANT] 855-431-0459 CA
```

The "CA" suffix and California phone number indicate Bay Area orders.

### Decision Matrix

| Location Indicator | Action |
|--------------------|--------|
| `855-431-0459 CA` | INCLUDE (Bay Area) |
| `Wegmans` | EXCLUDE (NYC only - no CA Wegmans) |
| NYC merchant name | Review - only include if work-related |
| Unknown | Check Gmail receipt for delivery address |

### Common CA DoorDash Merchants

All of these should be included:
- Sweetgreen, Chipotle, Dig Inn
- Rise Woodfire, Seoul Soul, Sao Mai
- Safeway, Target, CVS (supplies)
- Any merchant with CA indicator

---

## Receipt Requirements

### Required (>$25)
- All equipment purchases
- All travel expenses
- Software subscriptions
- Team meals
- Any expense >$25

### Not Required (<$25)
- Coffee <$25
- Small transit fares
- Parking <$25
- Small supplies

### Receipt Sources
1. Gmail receipts (preferred)
2. Credit card statements
3. Physical receipts (photograph)
4. Bank transaction records

---

## Duplicate Prevention

### Before Adding Any Expense

1. **Check Ramp History**: Search `michael_dangelo_expenses.csv`
2. **Check Current CSV**: Search `expenses_to_submit.csv`
3. **Match by Amount**: Credit card dates may differ by 1-2 days

### Common Duplicate Scenarios

| Scenario | Resolution |
|----------|------------|
| Same amount, different date | Match by amount, use earlier date |
| Same merchant, same day, different amounts | Likely two transactions - include both |
| Appears in Ramp CSV | Already reimbursed - do not add |

---

## Edge Cases

### Home Office Equipment

**Include if**:
- Dedicated to work use
- Reasonable for job function
- Not duplicating office equipment

**Examples**:
- Second monitor for home = INCLUDE
- Standing desk for home office = INCLUDE
- Personal gaming chair = EXCLUDE

### Travel Upgrades

| Upgrade Type | Include? |
|--------------|----------|
| Economy flights | YES |
| Economy Plus/Comfort+ | YES (if long flight) |
| Business class | REVIEW (needs approval) |
| Hotel room upgrades | NO (personal preference) |

### Mixed-Use Purchases

If a purchase is partially personal:
1. Calculate business percentage
2. Only claim business portion
3. Document the split in notes

### Subscription Proration

When starting mid-month:
- Include prorated amount
- Note "partial month" in notes

---

## Approval Thresholds

| Amount | Approval Needed |
|--------|-----------------|
| <$500 | Self-approval |
| $500-$2,000 | Manager notification |
| >$2,000 | Pre-approval required |
| >$5,000 | CFO approval |

### Pre-Approval Required

- Computer purchases >$2,000
- Furniture >$1,000
- Conference tickets >$500
- Any single expense >$5,000

---

## Seasonal Considerations

### End of Year (November-December)
- Process all pending expenses before year-end
- Higher priority on large infrastructure costs
- Ensure all 2025 expenses submitted by Jan 15, 2026

### Travel Seasons
- SF trips: Higher meal expenses expected
- Conference season (Sept-Nov): Higher travel costs
- Holiday period: Lower travel, normal subscriptions

---

## Red Flags (Do Not Submit)

- Personal entertainment subscriptions
- Alcohol as sole purchase
- Personal groceries (NYC)
- Vacation travel
- Gifts for family/friends
- Personal clothing
- Gym memberships
- Personal phone bills (unless reimbursement policy exists)
