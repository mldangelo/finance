# Duplicate Candidate Report

Generated: 2026-01-03
Source: expenses_to_submit.csv

Rules:
- Exact duplicate IDs
- Exact duplicate (date, merchant, amount)
- Fuzzy: normalized merchant + exact amount + date window <= 2 days
- Fuzzy (looser): normalized merchant + amount delta <= 0.50 + date window <= 2 days (positive amounts only)

## Summary

- Duplicate IDs: 14
- Duplicate exact (date, merchant, amount): 3
- Fuzzy clusters (exact amount): 5
- Fuzzy clusters (amount delta <= 0.50): 25

## Duplicate IDs

### BF-20250914-001

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 491 | BF-20250914-001 | 2025-09-14 | IKEA | 3032.24 | Amex | email_available |  |
| 492 | BF-20250914-001 | 2025-09-14 | Uber | 45.34 | Chase | email_available |  |

### EXP-2025-08-12-001

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 329 | EXP-2025-08-12-001 | 2025-08-12 | Anthropic | 2500.00 | Amex | pending |  |
| 330 | EXP-2025-08-12-001 | 2025-08-12 | DoorDash | 25.76 | Chase | pending |  |

### EXP-2025-08-15-001

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 342 | EXP-2025-08-15-001 | 2025-08-15 | Anthropic | 1502.14 | Amex | pending |  |
| 343 | EXP-2025-08-15-001 | 2025-08-15 | DoorDash | 21.97 | Chase | pending |  |

### EXP-2025-08-22-001

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 385 | EXP-2025-08-22-001 | 2025-08-22 | Delta Air Lines | 100.01 | Amex | found |  |
| 387 | EXP-2025-08-22-001 | 2025-08-22 | Pancho Villa | 20.01 | Chase | pending |  |

### EXP-2025-08-22-002

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 386 | EXP-2025-08-22-002 | 2025-08-22 | Zoom | 66.88 | Chase | pending |  |
| 388 | EXP-2025-08-22-002 | 2025-08-22 | Peet's Coffee | 4.55 | Chase | pending |  |

### EXP-2025-09-12-002

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 475 | EXP-2025-09-12-002 | 2025-09-12 | Zoom | 54.23 | Chase | pending |  |
| 476 | EXP-2025-09-12-002 | 2025-09-12 | Amazon | 272.57 | Chase | found |  |

### EXP-2025-10-11-001

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 571 | EXP-2025-10-11-001 | 2025-10-11 | Airbnb | 2248.12 | Chase | found |  |
| 572 | EXP-2025-10-11-001 | 2025-10-11 | DoorDash | 33.52 | Chase | pending |  |

### EXP-2025-10-30-001

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 670 | EXP-2025-10-30-001 | 2025-10-30 | Waymo | 24.37 | Chase | pending |  |
| 751 | EXP-2025-10-30-001 | 2025-10-30 | Delta Air Lines | 438.19 | Amex | found |  |

### EXP-2025-10-30-006

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 675 | EXP-2025-10-30-006 | 2025-10-30 | DoorDash | 66.62 | Chase | pending |  |
| 795 | EXP-2025-10-30-006 | 2025-10-30 | Amazon | 82.21 | Amex | pending |  |

### EXP-2025-11-02-003

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 688 | EXP-2025-11-02-003 | 2025-11-02 | HotelTonight | 491.00 | Chase | found |  |
| 788 | EXP-2025-11-02-003 | 2025-11-02 | Delta Air Lines | -619.97 | Amex | pending |  |

### EXP-2025-11-10-001

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 716 | EXP-2025-11-10-001 | 2025-11-10 | Anthropic | 1500.22 | Amex | pending |  |
| 717 | EXP-2025-11-10-001 | 2025-11-10 | DoorDash | 25.24 | Chase | found |  |

### EXP-2025-11-10-002

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 718 | EXP-2025-11-10-002 | 2025-11-10 | DoorDash | 32.98 | Chase | found |  |
| 719 | EXP-2025-11-10-002 | 2025-11-10 | Google One | 21.76 | Chase | pending |  |

### EXP-2025-11-13-001

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 723 | EXP-2025-11-13-001 | 2025-11-13 | Apple.com | 3855.90 | Chase | found |  |
| 725 | EXP-2025-11-13-001 | 2025-11-13 | DoorDash | 22.14 | Chase | found |  |

### EXP-2025-11-17-003

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 736 | EXP-2025-11-17-003 | 2025-11-17 | Lyft | 16.97 | Chase | pending |  |
| 737 | EXP-2025-11-17-003 | 2025-11-17 | Philz Coffee | 13.63 | Chase | found |  |

## Duplicate (date, merchant, amount)

### 2025-09-22 | Kaz Teriyaki | 36.03

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 515 | EXP-2025-09-22-003 | 2025-09-22 | Kaz Teriyaki | 36.03 | Chase | pending |  |
| 833 | RCP-2025-09-22-001 | 2025-09-22 | Kaz Teriyaki | 36.03 | Visa 2030 | photo | IMG_4428.jpg |

### 2025-10-15 | Delta Air Lines | 523.48

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 594 | EXP-2025-10-15-001 | 2025-10-15 | Delta Air Lines | 523.48 | Amex | found |  |
| 595 | EXP-2025-10-15-002 | 2025-10-15 | Delta Air Lines | 523.48 | Amex | found |  |

### 2025-11-01 | MBTA | 2.40

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 683 | EXP-2025-11-01-004 | 2025-11-01 | MBTA | 2.40 | Chase | pending |  |
| 684 | EXP-2025-11-01-005 | 2025-11-01 | MBTA | 2.40 | Chase | pending |  |

## Fuzzy (normalized merchant + exact amount, date window <= 2 days)

### momo noodle | 43.08

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 832 | RCP-2025-08-21-001 | 2025-08-21 | MOMO noodle | 43.08 | Visa 2030 | photo | IMG_4177.jpg |
| 391 | EXP-2025-08-23-002 | 2025-08-23 | Momo Noodle | 43.08 | Chase | pending |  |

### kaz teriyaki | 36.03

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 515 | EXP-2025-09-22-003 | 2025-09-22 | Kaz Teriyaki | 36.03 | Chase | pending |  |
| 833 | RCP-2025-09-22-001 | 2025-09-22 | Kaz Teriyaki | 36.03 | Visa 2030 | photo | IMG_4428.jpg |

### delta air lines | 523.48

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 594 | EXP-2025-10-15-001 | 2025-10-15 | Delta Air Lines | 523.48 | Amex | found |  |
| 595 | EXP-2025-10-15-002 | 2025-10-15 | Delta Air Lines | 523.48 | Amex | found |  |

### mbta | 2.4

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 683 | EXP-2025-11-01-004 | 2025-11-01 | MBTA | 2.40 | Chase | pending |  |
| 684 | EXP-2025-11-01-005 | 2025-11-01 | MBTA | 2.40 | Chase | pending |  |

### delta air lines | 287.99

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 730 | RCPT-20251114-DL1 | 2025-11-14 | Delta Air Lines | 287.99 | Amex | found |  |
| 731 | EXP-2025-11-15-001 | 2025-11-15 | Delta Air Lines | 287.99 | Amex | found |  |

## Fuzzy (normalized merchant + amount delta <= 0.50, date window <= 2 days)

### 

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 72 | BF-20250227-002 | 2025-02-27 | DoorDash | 61.31 | Chase | email_available |  |
| 74 | BF-20250228-001 | 2025-02-28 | DoorDash | 61.61 | Chase | email_available |  |

### 

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 221 | BF-20250612-002 | 2025-06-12 | DoorDash | 27.44 | Chase | email_available |  |
| 227 | BF-20250614-002 | 2025-06-14 | DoorDash | 27.72 | Chase | email_available |  |

### 

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 292 | BF-20250724-001 | 2025-07-24 | DoorDash | 23.58 | Chase | email_available |  |
| 294 | BF-20250726-002 | 2025-07-26 | DoorDash | 24.01 | Chase | email_available |  |

### 

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 327 | EXP-2025-08-11-003 | 2025-08-11 | DoorDash | 25.14 | Chase | pending |  |
| 335 | EXP-2025-08-13-004 | 2025-08-13 | DoorDash | 24.77 | Chase | pending |  |

### 

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 331 | BF-20250812-001 | 2025-08-12 | Uber | 24.08 | Chase | email_available |  |
| 341 | BF-20250814-001 | 2025-08-14 | Uber | 23.99 | Chase | email_available |  |

### 

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 353 | EXP-2025-08-17-007 | 2025-08-17 | DoorDash | 25.76 | Chase | pending |  |
| 364 | BF-20250819-001 | 2025-08-19 | Uber | 25.55 | Chase | email_available |  |

### 

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 389 | EXP-2025-08-22-003 | 2025-08-22 | DoorDash | 13.41 | Chase | pending |  |
| 392 | EXP-2025-08-23-003 | 2025-08-23 | DoorDash | 13.49 | Chase | pending |  |

### 

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 415 | EXP-2025-08-29-001 | 2025-08-29 | DoorDash | 22.55 | Chase | pending |  |
| 418 | EXP-2025-08-30-002 | 2025-08-30 | DoorDash | 22.76 | Chase | pending |  |

### 

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 560 | EXP-2025-10-04-002 | 2025-10-04 | DoorDash | 21.94 | Chase | pending |  |
| 564 | BF-20251006-001 | 2025-10-06 | Lyft | 22.04 | Chase | email_available |  |

### 

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 586 | EXP-2025-10-14-003 | 2025-10-14 | Uber | 10.96 | Chase | pending |  |
| 602 | EXP-2025-10-16-003 | 2025-10-16 | Uber | 11.44 | Chase | pending |  |

### 

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 602 | EXP-2025-10-16-003 | 2025-10-16 | Uber | 11.44 | Chase | pending |  |
| 612 | EXP-2025-10-17-003 | 2025-10-17 | Uber | 11.65 | Chase | pending |  |

### 

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 618 | EXP-2025-10-18-004 | 2025-10-18 | DoorDash | 26.67 | Chase | pending |  |
| 623 | EXP-2025-10-19-003 | 2025-10-19 | DoorDash | 26.64 | Chase | pending |  |

### 

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 639 | EXP-2025-10-22-002 | 2025-10-22 | DoorDash | 25.34 | Chase | pending |  |
| 645 | EXP-2025-10-24-002 | 2025-10-24 | Uber | 25.22 | Chase | pending |  |

### 

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 645 | EXP-2025-10-24-002 | 2025-10-24 | Uber | 25.22 | Chase | pending |  |
| 648 | EXP-2025-10-25-002 | 2025-10-25 | Uber | 24.82 | Chase | pending |  |

### 

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 703 | EXP-2025-11-07-003 | 2025-11-07 | Lyft | 46.73 | Chase | pending |  |
| 715 | EXP-2025-11-09-004 | 2025-11-09 | DoorDash | 46.84 | Chase | found |  |

### aplpay

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 21 | BF-20250119-002 | 2025-01-19 | Aplpay | 19.58 | Amex | pending |  |
| 22 | BF-20250120-001 | 2025-01-20 | Aplpay | 20.00 | Amex | pending |  |

### delta air lines

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 594 | EXP-2025-10-15-001 | 2025-10-15 | Delta Air Lines | 523.48 | Amex | found |  |
| 595 | EXP-2025-10-15-002 | 2025-10-15 | Delta Air Lines | 523.48 | Amex | found |  |

### delta air lines

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 730 | RCPT-20251114-DL1 | 2025-11-14 | Delta Air Lines | 287.99 | Amex | found |  |
| 731 | EXP-2025-11-15-001 | 2025-11-15 | Delta Air Lines | 287.99 | Amex | found |  |

### zoom

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 151 | BF-20250424-003 | 2025-04-24 | Zoom | 100.75 | Chase | pending |  |
| 150 | BF-20250424-002 | 2025-04-24 | Zoom | 100.76 | Chase | pending |  |

### kaz teriyaki

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 515 | EXP-2025-09-22-003 | 2025-09-22 | Kaz Teriyaki | 36.03 | Chase | pending |  |
| 833 | RCP-2025-09-22-001 | 2025-09-22 | Kaz Teriyaki | 36.03 | Visa 2030 | photo | IMG_4428.jpg |

### momo noodle

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 832 | RCP-2025-08-21-001 | 2025-08-21 | MOMO noodle | 43.08 | Visa 2030 | photo | IMG_4177.jpg |
| 391 | EXP-2025-08-23-002 | 2025-08-23 | Momo Noodle | 43.08 | Chase | pending |  |

### los

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 404 | BF-20250826-002 | 2025-08-26 | Los | 24.64 | Chase | pending |  |
| 414 | BF-20250828-003 | 2025-08-28 | Los | 24.95 | Chase | pending |  |

### verve coffee

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 455 | EXP-2025-09-08-002 | 2025-09-08 | Verve Coffee | 12.86 | Chase | pending |  |
| 459 | EXP-2025-09-09-002 | 2025-09-09 | Verve Coffee | 13.20 | Chase | pending |  |

### verve coffee

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 482 | EXP-2025-09-13-006 | 2025-09-13 | Verve Coffee | 13.20 | Chase | pending |  |
| 488 | EXP-2025-09-14-002 | 2025-09-14 | Verve Coffee | 12.86 | Chase | pending |  |

### mbta

| line | id | date | merchant | amount | source_card | receipt_status | receipt_file |
|---|---|---|---|---|---|---|---|
| 683 | EXP-2025-11-01-004 | 2025-11-01 | MBTA | 2.40 | Chase | pending |  |
| 684 | EXP-2025-11-01-005 | 2025-11-01 | MBTA | 2.40 | Chase | pending |  |
