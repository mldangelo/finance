#!/usr/bin/env python3
"""
Advanced Analysis Tool for Expense Reconciliation

Provides deeper analysis and comparison capabilities beyond basic reconciliation.
"""

import sqlite3
from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Tuple
import argparse

DB_PATH = Path(__file__).parent / "data" / "reconciliation.db"


class Analyzer:
    """Advanced analysis capabilities."""

    def __init__(self):
        self.conn = sqlite3.connect(str(DB_PATH))
        self.conn.row_factory = sqlite3.Row

    def find_potential_duplicates(self) -> List[Dict]:
        """Find potential duplicate entries in the expense CSV."""
        # Find transactions with same amount on same or nearby dates
        results = self.conn.execute("""
            SELECT t1.id, t1.transaction_date, t1.amount, t1.merchant_name,
                   t2.id as dup_id, t2.transaction_date as dup_date, t2.merchant_name as dup_merchant
            FROM transactions t1
            JOIN transactions t2 ON t1.amount = t2.amount
                AND t1.id < t2.id
                AND t1.source_id = t2.source_id
                AND ABS(julianday(t1.transaction_date) - julianday(t2.transaction_date)) <= 2
            WHERE t1.source_id = 'expense_csv'
            ORDER BY t1.amount DESC
        """).fetchall()

        return [dict(r) for r in results]

    def compare_date_ranges(self) -> Dict:
        """Compare date ranges across sources."""
        sources = self.conn.execute("""
            SELECT
                source_id,
                MIN(transaction_date) as earliest,
                MAX(transaction_date) as latest,
                COUNT(*) as count,
                SUM(CASE WHEN is_credit THEN -amount ELSE amount END) as total
            FROM transactions
            GROUP BY source_id
        """).fetchall()

        return {r['source_id']: dict(r) for r in sources}

    def find_large_unmatched(self, threshold: float = 500) -> List[Dict]:
        """Find large expenses that aren't matched to anything."""
        results = self.conn.execute("""
            SELECT t.*, s.name as source_name
            FROM transactions t
            JOIN sources s ON t.source_id = s.id
            WHERE t.amount >= ?
                AND t.source_id = 'expense_csv'
                AND t.id NOT IN (
                    SELECT transaction_id_1 FROM matches
                    UNION
                    SELECT transaction_id_2 FROM matches
                )
            ORDER BY t.amount DESC
        """, (threshold,)).fetchall()

        return [dict(r) for r in results]

    def merchant_summary(self) -> List[Dict]:
        """Summarize spending by merchant."""
        results = self.conn.execute("""
            SELECT
                merchant_name,
                COUNT(*) as transaction_count,
                SUM(amount) as total_amount,
                AVG(amount) as avg_amount,
                MIN(transaction_date) as first_date,
                MAX(transaction_date) as last_date
            FROM transactions
            WHERE source_id = 'expense_csv'
                AND NOT is_credit
            GROUP BY merchant_name_normalized
            HAVING COUNT(*) >= 2
            ORDER BY total_amount DESC
            LIMIT 30
        """).fetchall()

        return [dict(r) for r in results]

    def monthly_comparison(self) -> List[Dict]:
        """Compare monthly totals across sources."""
        results = self.conn.execute("""
            SELECT
                strftime('%Y-%m', transaction_date) as month,
                SUM(CASE WHEN source_id = 'expense_csv' THEN amount ELSE 0 END) as expense_csv,
                SUM(CASE WHEN source_id = 'ramp_reimbursements' THEN amount ELSE 0 END) as ramp,
                SUM(CASE WHEN source_id = 'chase_visa_2030' THEN amount ELSE 0 END) as chase
            FROM transactions
            WHERE NOT is_credit
            GROUP BY strftime('%Y-%m', transaction_date)
            ORDER BY month DESC
        """).fetchall()

        return [dict(r) for r in results]

    def find_overlapping_amounts(self) -> List[Dict]:
        """Find transactions with exact same amounts between expense CSV and Ramp."""
        results = self.conn.execute("""
            SELECT
                e.transaction_date as expense_date,
                e.amount,
                e.merchant_name as expense_merchant,
                r.transaction_date as ramp_date,
                r.merchant_name as ramp_merchant,
                ABS(julianday(e.transaction_date) - julianday(r.transaction_date)) as date_diff
            FROM transactions e
            JOIN transactions r ON e.amount = r.amount
            WHERE e.source_id = 'expense_csv'
                AND r.source_id = 'ramp_reimbursements'
                AND NOT e.is_credit
                AND NOT r.is_credit
            ORDER BY e.amount DESC, date_diff ASC
            LIMIT 50
        """).fetchall()

        return [dict(r) for r in results]

    def category_breakdown(self) -> List[Dict]:
        """Break down expenses by category."""
        results = self.conn.execute("""
            SELECT
                category,
                subcategory,
                COUNT(*) as count,
                SUM(amount) as total,
                AVG(amount) as average
            FROM transactions
            WHERE source_id = 'expense_csv'
                AND NOT is_credit
                AND category IS NOT NULL
                AND category != ''
            GROUP BY category, subcategory
            ORDER BY total DESC
        """).fetchall()

        return [dict(r) for r in results]

    def find_ramp_not_in_expenses(self) -> List[Dict]:
        """Find Ramp reimbursements that might be missing from expense tracking."""
        # Find Ramp transactions in our date range that don't match any expense
        results = self.conn.execute("""
            SELECT r.*
            FROM transactions r
            WHERE r.source_id = 'ramp_reimbursements'
                AND r.transaction_date >= '2025-08-01'
                AND r.id NOT IN (
                    SELECT transaction_id_2 FROM matches WHERE transaction_id_1 LIKE 'exp_%'
                    UNION
                    SELECT transaction_id_1 FROM matches WHERE transaction_id_2 LIKE 'exp_%'
                )
            ORDER BY r.amount DESC
        """).fetchall()

        return [dict(r) for r in results]


def print_table(data: List[Dict], columns: List[str] = None, max_width: int = 100):
    """Print data as a formatted table."""
    if not data:
        print("No data to display.")
        return

    if columns is None:
        columns = list(data[0].keys())

    # Calculate column widths
    widths = {col: len(col) for col in columns}
    for row in data:
        for col in columns:
            val = str(row.get(col, ''))[:50]
            widths[col] = max(widths[col], len(val))

    # Print header
    header = " | ".join(col.ljust(widths[col])[:widths[col]] for col in columns)
    print(header)
    print("-" * len(header))

    # Print rows
    for row in data:
        line = " | ".join(str(row.get(col, '')).ljust(widths[col])[:widths[col]] for col in columns)
        print(line)


def cmd_duplicates(args):
    """Check for potential duplicates."""
    analyzer = Analyzer()
    dups = analyzer.find_potential_duplicates()

    print(f"\n{'='*60}")
    print("POTENTIAL DUPLICATES IN EXPENSE CSV")
    print(f"{'='*60}\n")

    if not dups:
        print("No potential duplicates found!")
        return

    print(f"Found {len(dups)} potential duplicate pairs:\n")
    for d in dups[:20]:
        print(f"  ${float(d['amount']):>10,.2f} | {d['transaction_date']} vs {d['dup_date']}")
        print(f"           | {d['merchant_name'][:40]}")
        print(f"           | {d['dup_merchant'][:40]}")
        print()


def cmd_overlaps(args):
    """Find overlapping amounts between sources."""
    analyzer = Analyzer()
    overlaps = analyzer.find_overlapping_amounts()

    print(f"\n{'='*60}")
    print("AMOUNT OVERLAPS: EXPENSE CSV vs RAMP")
    print(f"{'='*60}\n")

    if not overlaps:
        print("No overlapping amounts found!")
        return

    print(f"Found {len(overlaps)} potential matches:\n")
    for o in overlaps:
        date_diff = o['date_diff']
        status = "EXACT" if date_diff == 0 else f"{int(date_diff)}d apart"
        print(f"  ${float(o['amount']):>10,.2f} | {status:12} | {o['expense_date']} vs {o['ramp_date']}")
        print(f"           | Expense: {o['expense_merchant'][:40]}")
        print(f"           | Ramp:    {o['ramp_merchant'][:40]}")
        print()


def cmd_monthly(args):
    """Show monthly comparison."""
    analyzer = Analyzer()
    monthly = analyzer.monthly_comparison()

    print(f"\n{'='*60}")
    print("MONTHLY TOTALS BY SOURCE")
    print(f"{'='*60}\n")

    print(f"{'Month':10} | {'Expense CSV':>14} | {'Ramp':>14} | {'Chase':>14}")
    print("-" * 60)

    for m in monthly:
        exp = f"${float(m['expense_csv']):>12,.2f}" if m['expense_csv'] else "           -"
        ramp = f"${float(m['ramp']):>12,.2f}" if m['ramp'] else "           -"
        chase = f"${float(m['chase']):>12,.2f}" if m['chase'] else "           -"
        print(f"{m['month']:10} | {exp} | {ramp} | {chase}")


def cmd_merchants(args):
    """Show top merchants."""
    analyzer = Analyzer()
    merchants = analyzer.merchant_summary()

    print(f"\n{'='*60}")
    print("TOP MERCHANTS BY TOTAL SPEND")
    print(f"{'='*60}\n")

    print(f"{'Merchant':35} | {'Count':>6} | {'Total':>12} | {'Avg':>10}")
    print("-" * 75)

    for m in merchants:
        print(f"{m['merchant_name'][:35]:35} | {m['transaction_count']:>6} | ${float(m['total_amount']):>10,.2f} | ${float(m['avg_amount']):>8,.2f}")


def cmd_large(args):
    """Show large unmatched expenses."""
    analyzer = Analyzer()
    threshold = float(args.threshold) if args.threshold else 500
    large = analyzer.find_large_unmatched(threshold)

    print(f"\n{'='*60}")
    print(f"LARGE UNMATCHED EXPENSES (>${threshold:,.0f})")
    print(f"{'='*60}\n")

    if not large:
        print("No large unmatched expenses found!")
        return

    print(f"Found {len(large)} expenses:\n")

    total = 0
    for e in large:
        total += float(e['amount'])
        print(f"  ${float(e['amount']):>10,.2f} | {e['transaction_date']} | {e['merchant_name'][:40]}")

    print(f"\n  {'Total':>10}: ${total:>10,.2f}")


def cmd_categories(args):
    """Show category breakdown."""
    analyzer = Analyzer()
    cats = analyzer.category_breakdown()

    print(f"\n{'='*60}")
    print("EXPENSE BREAKDOWN BY CATEGORY")
    print(f"{'='*60}\n")

    print(f"{'Category':20} | {'Subcategory':25} | {'Count':>6} | {'Total':>12}")
    print("-" * 80)

    for c in cats:
        subcat = c['subcategory'] or '-'
        print(f"{(c['category'] or '-')[:20]:20} | {subcat[:25]:25} | {c['count']:>6} | ${float(c['total']):>10,.2f}")


def cmd_summary(args):
    """Show full summary."""
    analyzer = Analyzer()

    print(f"\n{'='*60}")
    print("RECONCILIATION ANALYSIS SUMMARY")
    print(f"{'='*60}")

    # Date ranges
    print("\n## Date Ranges by Source")
    ranges = analyzer.compare_date_ranges()
    for source, data in ranges.items():
        if data['count'] > 0:
            print(f"  {source:25}: {data['earliest']} to {data['latest']} ({data['count']} txns, ${float(data['total'] or 0):,.2f})")

    # Duplicates
    print("\n## Potential Duplicates")
    dups = analyzer.find_potential_duplicates()
    print(f"  Found {len(dups)} potential duplicate pairs")

    # Overlaps
    print("\n## Amount Overlaps (Expense vs Ramp)")
    overlaps = analyzer.find_overlapping_amounts()
    print(f"  Found {len(overlaps)} transactions with matching amounts")
    if overlaps:
        exact_matches = [o for o in overlaps if o['date_diff'] == 0]
        print(f"  Of which {len(exact_matches)} have exact date matches (likely already reimbursed)")

    # Large unmatched
    print("\n## Large Unmatched Expenses (>$1000)")
    large = analyzer.find_large_unmatched(1000)
    print(f"  Found {len(large)} large expenses pending")
    if large:
        total = sum(float(e['amount']) for e in large)
        print(f"  Total value: ${total:,.2f}")


def main():
    parser = argparse.ArgumentParser(description="Expense Analysis Tool")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    subparsers.add_parser('summary', help='Show full summary')
    subparsers.add_parser('duplicates', help='Find potential duplicates')
    subparsers.add_parser('overlaps', help='Find overlapping amounts between sources')
    subparsers.add_parser('monthly', help='Show monthly comparison')
    subparsers.add_parser('merchants', help='Show top merchants')
    subparsers.add_parser('categories', help='Show category breakdown')

    large_parser = subparsers.add_parser('large', help='Show large unmatched expenses')
    large_parser.add_argument('--threshold', '-t', default='500', help='Amount threshold')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    commands = {
        'summary': cmd_summary,
        'duplicates': cmd_duplicates,
        'overlaps': cmd_overlaps,
        'monthly': cmd_monthly,
        'merchants': cmd_merchants,
        'large': cmd_large,
        'categories': cmd_categories,
    }

    commands[args.command](args)


if __name__ == '__main__':
    main()
