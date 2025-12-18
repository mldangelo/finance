#!/usr/bin/env python3
"""
Expense Reconciliation CLI Tool

A robust system for reconciling credit card statements, bank accounts,
and expense tracking across multiple data sources.

Usage:
    python reconcile.py init                    # Initialize database
    python reconcile.py import chase <file>    # Import Chase statement
    python reconcile.py import expenses        # Import expense CSV
    python reconcile.py import ramp            # Import Ramp reimbursements
    python reconcile.py reconcile              # Run full reconciliation
    python reconcile.py report                 # Generate reconciliation report
    python reconcile.py status                 # Show current status
"""

import argparse
import csv
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

# Configuration
DB_PATH = Path(__file__).parent / "data" / "reconciliation.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"
PROJECT_ROOT = Path(__file__).parent.parent

# Matching configuration
DATE_TOLERANCE_DAYS = 3  # Allow dates to differ by up to 3 days
AMOUNT_TOLERANCE = Decimal("0.01")  # Allow 1 cent difference
FUZZY_MATCH_THRESHOLD = 0.8  # 80% similarity for merchant names


@dataclass
class Transaction:
    """Represents a transaction from any source."""
    id: str
    source_id: str
    external_id: Optional[str]
    transaction_date: str
    post_date: Optional[str]
    amount: Decimal
    merchant_name: str
    merchant_name_normalized: str
    description: Optional[str]
    category: Optional[str]
    subcategory: Optional[str]
    memo: Optional[str]
    is_credit: bool
    raw_data: Optional[str]
    import_batch_id: Optional[str]


class Database:
    """Database connection and operations."""

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row

    def initialize(self):
        """Initialize database with schema."""
        with open(SCHEMA_PATH) as f:
            self.conn.executescript(f.read())
        self.conn.commit()
        print(f"Database initialized at {self.db_path}")

    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        return self.conn.execute(query, params)

    def executemany(self, query: str, params_list: List[tuple]) -> sqlite3.Cursor:
        return self.conn.executemany(query, params_list)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()


def normalize_merchant_name(name: str) -> str:
    """Normalize merchant name for matching."""
    if not name:
        return ""
    # Convert to lowercase
    normalized = name.lower()
    # Remove common prefixes
    prefixes = ['dd ', 'doordash*', 'uber *', 'lyft *', 'tst* ', 'sq *', 'paypal *']
    for prefix in prefixes:
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix):]
    # Remove special characters and extra spaces
    normalized = re.sub(r'[^a-z0-9\s]', '', normalized)
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    # Remove common suffixes
    suffixes = [' ca', ' ny', ' nyc', ' sf', ' inc', ' llc', ' corp']
    for suffix in suffixes:
        if normalized.endswith(suffix):
            normalized = normalized[:-len(suffix)]
    return normalized.strip()


def calculate_file_hash(file_path: Path) -> str:
    """Calculate SHA256 hash of file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def levenshtein_similarity(s1: str, s2: str) -> float:
    """Calculate similarity ratio between two strings."""
    if not s1 or not s2:
        return 0.0
    if s1 == s2:
        return 1.0

    len1, len2 = len(s1), len(s2)
    if len1 < len2:
        s1, s2 = s2, s1
        len1, len2 = len2, len1

    current_row = range(len2 + 1)
    for i in range(1, len1 + 1):
        previous_row, current_row = current_row, [i] + [0] * len2
        for j in range(1, len2 + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if s1[i - 1] != s2[j - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    distance = current_row[len2]
    max_len = max(len1, len2)
    return 1 - (distance / max_len)


# ============================================
# IMPORTERS
# ============================================

class ExpenseCSVImporter:
    """Import expenses from the tracking CSV."""

    def __init__(self, db: Database):
        self.db = db
        self.source_id = "expense_csv"

    def import_file(self, file_path: Path) -> int:
        """Import expense CSV file."""
        batch_id = str(uuid4())
        file_hash = calculate_file_hash(file_path)

        # Check if already imported
        existing = self.db.execute(
            "SELECT id FROM import_batches WHERE file_hash = ?",
            (file_hash,)
        ).fetchone()
        if existing:
            print(f"File already imported (batch {existing['id']}). Skipping.")
            return 0

        transactions = []
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    amount = Decimal(row['amount'])
                    tx = Transaction(
                        id=f"exp_{row['id']}",
                        source_id=self.source_id,
                        external_id=row['id'],
                        transaction_date=row['date'],
                        post_date=None,
                        amount=amount,
                        merchant_name=row['merchant'],
                        merchant_name_normalized=normalize_merchant_name(row['merchant']),
                        description=row.get('description', ''),
                        category=row.get('category', ''),
                        subcategory=row.get('subcategory', ''),
                        memo=row.get('business_purpose', ''),
                        is_credit=False,
                        raw_data=json.dumps(row),
                        import_batch_id=batch_id
                    )
                    transactions.append(tx)
                except (KeyError, ValueError) as e:
                    print(f"Error parsing row: {e}")
                    continue

        # Insert transactions
        self._insert_transactions(transactions)

        # Record import batch
        self.db.execute("""
            INSERT INTO import_batches (id, source_id, file_path, file_hash, import_type, record_count, date_range_start, date_range_end)
            VALUES (?, ?, ?, ?, 'csv_export', ?, ?, ?)
        """, (
            batch_id,
            self.source_id,
            str(file_path),
            file_hash,
            len(transactions),
            min(t.transaction_date for t in transactions) if transactions else None,
            max(t.transaction_date for t in transactions) if transactions else None
        ))
        self.db.commit()

        print(f"Imported {len(transactions)} expenses from {file_path}")
        return len(transactions)

    def _insert_transactions(self, transactions: List[Transaction]):
        """Insert transactions into database."""
        self.db.executemany("""
            INSERT OR REPLACE INTO transactions
            (id, source_id, external_id, transaction_date, post_date, amount,
             merchant_name, merchant_name_normalized, description, category,
             subcategory, memo, is_credit, raw_data, import_batch_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            (t.id, t.source_id, t.external_id, t.transaction_date, t.post_date,
             str(t.amount), t.merchant_name, t.merchant_name_normalized,
             t.description, t.category, t.subcategory, t.memo, t.is_credit,
             t.raw_data, t.import_batch_id)
            for t in transactions
        ])


class RampImporter:
    """Import Ramp reimbursement data."""

    def __init__(self, db: Database):
        self.db = db
        self.source_id = "ramp_reimbursements"

    def import_file(self, file_path: Path) -> int:
        """Import Ramp CSV export."""
        batch_id = str(uuid4())
        file_hash = calculate_file_hash(file_path)

        existing = self.db.execute(
            "SELECT id FROM import_batches WHERE file_hash = ?",
            (file_hash,)
        ).fetchone()
        if existing:
            print(f"File already imported. Skipping.")
            return 0

        transactions = []
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Parse date from ISO format
                    date_str = row['spend_time'].split('T')[0]
                    amount = Decimal(row['amount'])

                    # Extract merchant from memo
                    memo = row.get('memo', '')
                    merchant = self._extract_merchant_from_memo(memo)

                    tx = Transaction(
                        id=f"ramp_{row['id']}",
                        source_id=self.source_id,
                        external_id=row['id'],
                        transaction_date=date_str,
                        post_date=None,
                        amount=amount,
                        merchant_name=merchant,
                        merchant_name_normalized=normalize_merchant_name(merchant),
                        description=memo,
                        category=row.get('category', ''),
                        subcategory=None,
                        memo=memo,
                        is_credit=False,
                        raw_data=json.dumps(row),
                        import_batch_id=batch_id
                    )
                    transactions.append(tx)
                except (KeyError, ValueError) as e:
                    print(f"Error parsing Ramp row: {e}")
                    continue

        self._insert_transactions(transactions)

        self.db.execute("""
            INSERT INTO import_batches (id, source_id, file_path, file_hash, import_type, record_count, date_range_start, date_range_end)
            VALUES (?, ?, ?, ?, 'csv_export', ?, ?, ?)
        """, (
            batch_id,
            self.source_id,
            str(file_path),
            file_hash,
            len(transactions),
            min(t.transaction_date for t in transactions) if transactions else None,
            max(t.transaction_date for t in transactions) if transactions else None
        ))
        self.db.commit()

        print(f"Imported {len(transactions)} Ramp reimbursements from {file_path}")
        return len(transactions)

    def _extract_merchant_from_memo(self, memo: str) -> str:
        """Extract merchant name from Ramp memo field."""
        # Common patterns: "Fwd: Order Confirmation for Michael from Kajiken"
        patterns = [
            r'from ([A-Za-z0-9\s\-\']+?)(?:\s*$|(?=\s+[A-Z]))',
            r'receipt from ([A-Za-z0-9\s\-\']+)',
            r'at ([A-Za-z0-9\s\-\']+?)(?:\s*$)',
        ]
        for pattern in patterns:
            match = re.search(pattern, memo, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return memo[:50] if memo else "Unknown"

    def _insert_transactions(self, transactions: List[Transaction]):
        """Insert transactions into database."""
        self.db.executemany("""
            INSERT OR REPLACE INTO transactions
            (id, source_id, external_id, transaction_date, post_date, amount,
             merchant_name, merchant_name_normalized, description, category,
             subcategory, memo, is_credit, raw_data, import_batch_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            (t.id, t.source_id, t.external_id, t.transaction_date, t.post_date,
             str(t.amount), t.merchant_name, t.merchant_name_normalized,
             t.description, t.category, t.subcategory, t.memo, t.is_credit,
             t.raw_data, t.import_batch_id)
            for t in transactions
        ])


class ChaseStatementImporter:
    """Import Chase credit card statement (PDF or CSV)."""

    def __init__(self, db: Database):
        self.db = db
        self.source_id = "chase_visa_2030"

    def import_csv(self, file_path: Path) -> int:
        """Import Chase CSV export (if available)."""
        batch_id = str(uuid4())
        file_hash = calculate_file_hash(file_path)

        existing = self.db.execute(
            "SELECT id FROM import_batches WHERE file_hash = ?",
            (file_hash,)
        ).fetchone()
        if existing:
            print(f"File already imported. Skipping.")
            return 0

        transactions = []
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Chase CSV format: Transaction Date, Post Date, Description, Category, Type, Amount
                    tx_date = self._parse_chase_date(row.get('Transaction Date', ''))
                    post_date = self._parse_chase_date(row.get('Post Date', ''))
                    amount = Decimal(row['Amount'].replace('$', '').replace(',', ''))
                    is_credit = amount > 0  # Positive amounts are credits/payments

                    tx = Transaction(
                        id=f"chase_{batch_id}_{len(transactions)}",
                        source_id=self.source_id,
                        external_id=None,
                        transaction_date=tx_date,
                        post_date=post_date,
                        amount=abs(amount),
                        merchant_name=row.get('Description', ''),
                        merchant_name_normalized=normalize_merchant_name(row.get('Description', '')),
                        description=row.get('Description', ''),
                        category=row.get('Category', ''),
                        subcategory=None,
                        memo=None,
                        is_credit=is_credit,
                        raw_data=json.dumps(row),
                        import_batch_id=batch_id
                    )
                    transactions.append(tx)
                except (KeyError, ValueError) as e:
                    print(f"Error parsing Chase row: {e}")
                    continue

        self._insert_transactions(transactions)

        self.db.execute("""
            INSERT INTO import_batches (id, source_id, file_path, file_hash, import_type, record_count, date_range_start, date_range_end)
            VALUES (?, ?, ?, ?, 'csv_export', ?, ?, ?)
        """, (
            batch_id,
            self.source_id,
            str(file_path),
            file_hash,
            len(transactions),
            min(t.transaction_date for t in transactions) if transactions else None,
            max(t.transaction_date for t in transactions) if transactions else None
        ))
        self.db.commit()

        print(f"Imported {len(transactions)} Chase transactions from {file_path}")
        return len(transactions)

    def _parse_chase_date(self, date_str: str) -> str:
        """Parse Chase date format (MM/DD/YYYY) to ISO format."""
        if not date_str:
            return ""
        try:
            dt = datetime.strptime(date_str, "%m/%d/%Y")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            return date_str

    def _insert_transactions(self, transactions: List[Transaction]):
        """Insert transactions into database."""
        self.db.executemany("""
            INSERT OR REPLACE INTO transactions
            (id, source_id, external_id, transaction_date, post_date, amount,
             merchant_name, merchant_name_normalized, description, category,
             subcategory, memo, is_credit, raw_data, import_batch_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            (t.id, t.source_id, t.external_id, t.transaction_date, t.post_date,
             str(t.amount), t.merchant_name, t.merchant_name_normalized,
             t.description, t.category, t.subcategory, t.memo, t.is_credit,
             t.raw_data, t.import_batch_id)
            for t in transactions
        ])

    def import_pdf(self, file_path: Path) -> int:
        """Import Chase PDF statement."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from importers.pdf_parsers import ChasePDFParser

        batch_id = str(uuid4())
        file_hash = calculate_file_hash(file_path)

        existing = self.db.execute(
            "SELECT id FROM import_batches WHERE file_hash = ?",
            (file_hash,)
        ).fetchone()
        if existing:
            print(f"File already imported. Skipping: {file_path.name}")
            return 0

        parser = ChasePDFParser(file_path)
        parsed_txs = parser.parse()

        transactions = []
        for i, ptx in enumerate(parsed_txs):
            tx = Transaction(
                id=f"chase_{batch_id}_{i}",
                source_id=self.source_id,
                external_id=None,
                transaction_date=ptx.date,
                post_date=None,
                amount=ptx.amount,
                merchant_name=ptx.description,
                merchant_name_normalized=normalize_merchant_name(ptx.description),
                description=ptx.description,
                category=ptx.category,
                subcategory=None,
                memo=None,
                is_credit=ptx.is_credit,
                raw_data=ptx.raw_text,
                import_batch_id=batch_id
            )
            transactions.append(tx)

        if not transactions:
            print(f"No transactions found in {file_path.name}")
            return 0

        self._insert_transactions(transactions)

        self.db.execute("""
            INSERT INTO import_batches (id, source_id, file_path, file_hash, import_type, record_count, date_range_start, date_range_end)
            VALUES (?, ?, ?, ?, 'pdf_statement', ?, ?, ?)
        """, (
            batch_id,
            self.source_id,
            str(file_path),
            file_hash,
            len(transactions),
            min(t.transaction_date for t in transactions),
            max(t.transaction_date for t in transactions)
        ))
        self.db.commit()

        print(f"Imported {len(transactions)} transactions from {file_path.name}")
        return len(transactions)

    def import_all_pdfs(self, directory: Path) -> int:
        """Import all PDF statements from a directory."""
        total = 0
        pdf_files = sorted(directory.glob("*.pdf"))
        print(f"Found {len(pdf_files)} PDF files in {directory}")

        for pdf_file in pdf_files:
            count = self.import_pdf(pdf_file)
            total += count

        return total


class BankOfAmericaImporter:
    """Import Bank of America PDF statements."""

    def __init__(self, db: Database):
        self.db = db
        self.source_id = "boa_checking"

    def import_pdf(self, file_path: Path) -> int:
        """Import Bank of America PDF statement."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from importers.pdf_parsers import BankOfAmericaPDFParser

        batch_id = str(uuid4())
        file_hash = calculate_file_hash(file_path)

        existing = self.db.execute(
            "SELECT id FROM import_batches WHERE file_hash = ?",
            (file_hash,)
        ).fetchone()
        if existing:
            print(f"File already imported. Skipping: {file_path.name}")
            return 0

        parser = BankOfAmericaPDFParser(file_path)
        parsed_txs = parser.parse()

        transactions = []
        for i, ptx in enumerate(parsed_txs):
            tx = Transaction(
                id=f"boa_{batch_id}_{i}",
                source_id=self.source_id,
                external_id=None,
                transaction_date=ptx.date,
                post_date=None,
                amount=ptx.amount,
                merchant_name=ptx.description[:100],  # Truncate long descriptions
                merchant_name_normalized=normalize_merchant_name(ptx.description),
                description=ptx.description,
                category=ptx.category,
                subcategory=None,
                memo=None,
                is_credit=ptx.is_credit,
                raw_data=ptx.raw_text,
                import_batch_id=batch_id
            )
            transactions.append(tx)

        if not transactions:
            print(f"No transactions found in {file_path.name}")
            return 0

        self._insert_transactions(transactions)

        self.db.execute("""
            INSERT INTO import_batches (id, source_id, file_path, file_hash, import_type, record_count, date_range_start, date_range_end)
            VALUES (?, ?, ?, ?, 'pdf_statement', ?, ?, ?)
        """, (
            batch_id,
            self.source_id,
            str(file_path),
            file_hash,
            len(transactions),
            min(t.transaction_date for t in transactions),
            max(t.transaction_date for t in transactions)
        ))
        self.db.commit()

        print(f"Imported {len(transactions)} transactions from {file_path.name}")
        return len(transactions)

    def import_all_pdfs(self, directory: Path) -> int:
        """Import all PDF statements from a directory."""
        total = 0
        pdf_files = sorted(directory.glob("*.pdf"))
        print(f"Found {len(pdf_files)} PDF files in {directory}")

        for pdf_file in pdf_files:
            count = self.import_pdf(pdf_file)
            total += count

        return total

    def _insert_transactions(self, transactions: List[Transaction]):
        """Insert transactions into database."""
        self.db.executemany("""
            INSERT OR REPLACE INTO transactions
            (id, source_id, external_id, transaction_date, post_date, amount,
             merchant_name, merchant_name_normalized, description, category,
             subcategory, memo, is_credit, raw_data, import_batch_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            (t.id, t.source_id, t.external_id, t.transaction_date, t.post_date,
             str(t.amount), t.merchant_name, t.merchant_name_normalized,
             t.description, t.category, t.subcategory, t.memo, t.is_credit,
             t.raw_data, t.import_batch_id)
            for t in transactions
        ])


# ============================================
# RECONCILIATION ENGINE
# ============================================

class ReconciliationEngine:
    """Core reconciliation logic."""

    def __init__(self, db: Database):
        self.db = db

    def reconcile_expenses_vs_ramp(self) -> Dict[str, Any]:
        """Check which expenses have already been reimbursed via Ramp."""
        run_id = self._create_run('expenses_vs_ramp', 'expense_csv', 'ramp_reimbursements')

        # Get all expense transactions
        expenses = self.db.execute("""
            SELECT * FROM transactions WHERE source_id = 'expense_csv'
        """).fetchall()

        # Get all Ramp reimbursements
        ramp_txs = self.db.execute("""
            SELECT * FROM transactions WHERE source_id = 'ramp_reimbursements'
        """).fetchall()

        matched = []
        unmatched_expenses = []
        already_reimbursed = []

        for exp in expenses:
            match = self._find_best_match(exp, ramp_txs)
            if match:
                matched.append((exp['id'], match['id'], match['confidence']))
                already_reimbursed.append(exp)
            else:
                unmatched_expenses.append(exp)

        # Record matches
        for exp_id, ramp_id, confidence in matched:
            self.db.execute("""
                INSERT OR REPLACE INTO matches (transaction_id_1, transaction_id_2, match_type, confidence_score, matched_by)
                VALUES (?, ?, ?, ?, 'system')
            """, (exp_id, ramp_id, 'exact' if confidence > 95 else 'date_fuzzy', confidence))

        # Record discrepancies for already reimbursed items
        for exp in already_reimbursed:
            self.db.execute("""
                INSERT INTO discrepancies (reconciliation_run_id, transaction_id, discrepancy_type, severity, notes)
                VALUES (?, ?, 'already_reimbursed', 'high', 'This expense appears to have been reimbursed already')
            """, (run_id, exp['id']))

        # Update run stats
        self.db.execute("""
            UPDATE reconciliation_runs SET
                total_source_1 = ?,
                total_source_2 = ?,
                matched_count = ?,
                unmatched_source_1 = ?
            WHERE id = ?
        """, (len(expenses), len(ramp_txs), len(matched), len(unmatched_expenses), run_id))

        self.db.commit()

        return {
            'run_id': run_id,
            'total_expenses': len(expenses),
            'total_ramp': len(ramp_txs),
            'matched': len(matched),
            'already_reimbursed': len(already_reimbursed),
            'pending_reimbursement': len(unmatched_expenses)
        }

    def reconcile_expenses_vs_chase(self) -> Dict[str, Any]:
        """Check which expenses are matched in Chase statements."""
        run_id = self._create_run('expenses_vs_chase', 'expense_csv', 'chase_visa_2030')

        # Get expense transactions for Chase card
        expenses = self.db.execute("""
            SELECT * FROM transactions
            WHERE source_id = 'expense_csv'
            AND (LOWER(raw_data) LIKE '%chase%' OR LOWER(category) NOT IN ('Infrastructure'))
        """).fetchall()

        # Get Chase transactions (purchases only, not credits/payments)
        chase_txs = self.db.execute("""
            SELECT * FROM transactions
            WHERE source_id = 'chase_visa_2030'
            AND NOT is_credit
            AND transaction_date >= '2025-08-01'
        """).fetchall()

        matched = []
        unmatched_expenses = []
        unmatched_chase = list(chase_txs)

        for exp in expenses:
            match = self._find_best_match(exp, unmatched_chase)
            if match:
                matched.append((exp['id'], match['id'], match['confidence']))
                # Remove from unmatched
                unmatched_chase = [c for c in unmatched_chase if c['id'] != match['id']]
            else:
                unmatched_expenses.append(exp)

        # Record matches
        for exp_id, chase_id, confidence in matched:
            self.db.execute("""
                INSERT OR REPLACE INTO matches (transaction_id_1, transaction_id_2, match_type, confidence_score, matched_by)
                VALUES (?, ?, ?, ?, 'system')
            """, (exp_id, chase_id, 'exact' if confidence > 95 else 'date_fuzzy', confidence))

        self.db.commit()

        return {
            'run_id': run_id,
            'total_expenses': len(expenses),
            'total_chase': len(chase_txs),
            'matched': len(matched),
            'unmatched_expenses': len(unmatched_expenses),
            'unmatched_chase': len(unmatched_chase)
        }

    def reconcile_cc_payments_vs_boa(self) -> Dict[str, Any]:
        """Check that credit card payments match bank withdrawals."""
        run_id = self._create_run('cc_payments_vs_boa', 'chase_visa_2030', 'boa_checking')

        # Get Chase payments (credits on CC = payments made)
        chase_payments = self.db.execute("""
            SELECT * FROM transactions
            WHERE source_id = 'chase_visa_2030'
            AND is_credit
            AND (LOWER(description) LIKE '%payment%' OR LOWER(description) LIKE '%thank you%')
        """).fetchall()

        # Get BoA Chase payment withdrawals
        boa_chase_payments = self.db.execute("""
            SELECT * FROM transactions
            WHERE source_id = 'boa_checking'
            AND NOT is_credit
            AND LOWER(description) LIKE '%chase%'
        """).fetchall()

        matched = []
        for payment in chase_payments:
            match = self._find_best_match(payment, boa_chase_payments)
            if match:
                matched.append((payment['id'], match['id'], match['confidence']))

        # Record matches
        for cc_id, boa_id, confidence in matched:
            self.db.execute("""
                INSERT OR REPLACE INTO matches (transaction_id_1, transaction_id_2, match_type, confidence_score, matched_by)
                VALUES (?, ?, ?, ?, 'system')
            """, (cc_id, boa_id, 'exact' if confidence > 95 else 'amount_fuzzy', confidence))

        self.db.commit()

        total_chase_payments = sum(Decimal(str(p['amount'])) for p in chase_payments)
        total_boa_payments = sum(Decimal(str(p['amount'])) for p in boa_chase_payments)

        return {
            'run_id': run_id,
            'chase_payments_count': len(chase_payments),
            'boa_payments_count': len(boa_chase_payments),
            'matched': len(matched),
            'total_chase_payments': float(total_chase_payments),
            'total_boa_payments': float(total_boa_payments)
        }

    def find_missing_in_expenses(self) -> List[Dict]:
        """Find Chase transactions not tracked in expense CSV."""
        # Get significant Chase purchases not matched
        results = self.db.execute("""
            SELECT c.*
            FROM transactions c
            WHERE c.source_id = 'chase_visa_2030'
            AND NOT c.is_credit
            AND c.amount >= 20
            AND c.transaction_date >= '2025-08-01'
            AND c.id NOT IN (
                SELECT transaction_id_2 FROM matches WHERE transaction_id_1 LIKE 'exp_%'
            )
            ORDER BY c.amount DESC
            LIMIT 100
        """).fetchall()

        return [dict(r) for r in results]

    def reconcile_all(self) -> Dict[str, Any]:
        """Run all reconciliation checks."""
        results = {}

        print("  Checking expenses vs Ramp reimbursements...")
        results['expenses_vs_ramp'] = self.reconcile_expenses_vs_ramp()

        print("  Checking expenses vs Chase statements...")
        results['expenses_vs_chase'] = self.reconcile_expenses_vs_chase()

        print("  Checking CC payments vs Bank account...")
        results['cc_payments_vs_boa'] = self.reconcile_cc_payments_vs_boa()

        return results

    def _find_best_match(self, transaction: sqlite3.Row, candidates: List[sqlite3.Row]) -> Optional[Dict]:
        """Find best matching transaction from candidates."""
        best_match = None
        best_confidence = 0

        tx_date = datetime.strptime(transaction['transaction_date'], "%Y-%m-%d")
        tx_amount = Decimal(str(transaction['amount']))
        tx_merchant = transaction['merchant_name_normalized']

        for candidate in candidates:
            try:
                cand_date = datetime.strptime(candidate['transaction_date'], "%Y-%m-%d")
                cand_amount = Decimal(str(candidate['amount']))
                cand_merchant = candidate['merchant_name_normalized']

                # Calculate confidence score
                confidence = 0

                # Amount match (40 points)
                amount_diff = abs(tx_amount - cand_amount)
                if amount_diff <= AMOUNT_TOLERANCE:
                    confidence += 40
                elif amount_diff <= Decimal("1.00"):
                    confidence += 30

                # Date match (30 points)
                date_diff = abs((tx_date - cand_date).days)
                if date_diff == 0:
                    confidence += 30
                elif date_diff <= DATE_TOLERANCE_DAYS:
                    confidence += 20
                elif date_diff <= 7:
                    confidence += 10

                # Merchant match (30 points)
                merchant_sim = levenshtein_similarity(tx_merchant, cand_merchant)
                confidence += int(merchant_sim * 30)

                if confidence > best_confidence and confidence >= 60:
                    best_confidence = confidence
                    best_match = {'id': candidate['id'], 'confidence': confidence}

            except (ValueError, TypeError):
                continue

        return best_match

    def _create_run(self, run_type: str, source1: str, source2: str) -> int:
        """Create a new reconciliation run record."""
        cursor = self.db.execute("""
            INSERT INTO reconciliation_runs (run_type, source_id_1, source_id_2)
            VALUES (?, ?, ?)
        """, (run_type, source1, source2))
        self.db.commit()
        return cursor.lastrowid


# ============================================
# REPORTING
# ============================================

class ReportGenerator:
    """Generate reconciliation reports."""

    def __init__(self, db: Database):
        self.db = db

    def status_report(self) -> str:
        """Generate current status report."""
        lines = []
        lines.append("=" * 60)
        lines.append("EXPENSE RECONCILIATION STATUS")
        lines.append("=" * 60)
        lines.append("")

        # Source summary
        sources = self.db.execute("SELECT * FROM v_source_summary").fetchall()
        lines.append("DATA SOURCES:")
        lines.append("-" * 40)
        for s in sources:
            lines.append(f"  {s['name']:30} {s['transaction_count']:5} txns  ${float(s['net_amount'] or 0):>12,.2f}")
        lines.append("")

        # Recent imports
        imports = self.db.execute("""
            SELECT ib.*, s.name as source_name
            FROM import_batches ib
            JOIN sources s ON ib.source_id = s.id
            ORDER BY ib.created_at DESC LIMIT 5
        """).fetchall()

        lines.append("RECENT IMPORTS:")
        lines.append("-" * 40)
        for imp in imports:
            lines.append(f"  {imp['created_at'][:19]}  {imp['source_name']:20}  {imp['record_count']} records")
        lines.append("")

        # Open discrepancies
        discrepancies = self.db.execute("""
            SELECT discrepancy_type, severity, COUNT(*) as count
            FROM discrepancies
            WHERE status = 'open'
            GROUP BY discrepancy_type, severity
            ORDER BY
                CASE severity WHEN 'critical' THEN 1 WHEN 'high' THEN 2 WHEN 'medium' THEN 3 ELSE 4 END
        """).fetchall()

        lines.append("OPEN DISCREPANCIES:")
        lines.append("-" * 40)
        if discrepancies:
            for d in discrepancies:
                lines.append(f"  [{d['severity']:8}] {d['discrepancy_type']:25} {d['count']:3} items")
        else:
            lines.append("  No open discrepancies")
        lines.append("")

        # Match summary
        matches = self.db.execute("""
            SELECT match_type, COUNT(*) as count
            FROM matches
            GROUP BY match_type
        """).fetchall()

        lines.append("MATCHED TRANSACTIONS:")
        lines.append("-" * 40)
        if matches:
            for m in matches:
                lines.append(f"  {m['match_type']:20} {m['count']:5} matches")
        else:
            lines.append("  No matches recorded yet")
        lines.append("")

        return "\n".join(lines)

    def discrepancy_report(self) -> str:
        """Generate detailed discrepancy report."""
        lines = []
        lines.append("=" * 60)
        lines.append("DISCREPANCY REPORT")
        lines.append("=" * 60)
        lines.append("")

        discrepancies = self.db.execute("""
            SELECT d.*, t.merchant_name, t.amount, t.transaction_date, s.name as source_name
            FROM discrepancies d
            JOIN transactions t ON d.transaction_id = t.id
            JOIN sources s ON t.source_id = s.id
            WHERE d.status = 'open'
            ORDER BY
                CASE d.severity WHEN 'critical' THEN 1 WHEN 'high' THEN 2 WHEN 'medium' THEN 3 ELSE 4 END,
                t.amount DESC
        """).fetchall()

        if not discrepancies:
            lines.append("No open discrepancies found.")
            return "\n".join(lines)

        current_type = None
        for d in discrepancies:
            if d['discrepancy_type'] != current_type:
                current_type = d['discrepancy_type']
                lines.append(f"\n### {current_type.upper().replace('_', ' ')}")
                lines.append("-" * 40)

            lines.append(f"  [{d['severity']:8}] {d['transaction_date']} | ${float(d['amount']):>10,.2f} | {d['merchant_name'][:30]}")
            if d['notes']:
                lines.append(f"           Note: {d['notes']}")

        return "\n".join(lines)

    def full_report(self) -> str:
        """Generate comprehensive reconciliation report."""
        parts = [
            self.status_report(),
            "",
            self.discrepancy_report()
        ]
        return "\n".join(parts)


# ============================================
# CLI
# ============================================

def cmd_init(args):
    """Initialize the database."""
    db = Database()
    db.initialize()
    db.close()


def cmd_import(args):
    """Import data from various sources."""
    db = Database()

    if args.source == 'expenses':
        importer = ExpenseCSVImporter(db)
        file_path = PROJECT_ROOT / "expenses_to_submit.csv"
        importer.import_file(file_path)

    elif args.source == 'ramp':
        importer = RampImporter(db)
        file_path = PROJECT_ROOT / "michael_dangelo_expenses.csv"
        importer.import_file(file_path)

    elif args.source == 'chase':
        importer = ChaseStatementImporter(db)
        if args.file:
            file_path = Path(args.file)
            if file_path.suffix.lower() == '.csv':
                importer.import_csv(file_path)
            elif file_path.suffix.lower() == '.pdf':
                importer.import_pdf(file_path)
            elif file_path.is_dir():
                importer.import_all_pdfs(file_path)
            else:
                print(f"Unknown file type: {file_path}")
        else:
            # Default to importing all PDFs from chase directory
            chase_dir = PROJECT_ROOT / "chase"
            if chase_dir.exists():
                print(f"Importing all Chase PDFs from {chase_dir}...")
                importer.import_all_pdfs(chase_dir)
            else:
                print("Please specify a file path for Chase import.")

    elif args.source == 'boa':
        importer = BankOfAmericaImporter(db)
        if args.file:
            file_path = Path(args.file)
            if file_path.suffix.lower() == '.pdf':
                importer.import_pdf(file_path)
            elif file_path.is_dir():
                importer.import_all_pdfs(file_path)
            else:
                print(f"Unknown file type: {file_path}")
        else:
            # Default to importing all PDFs from boa directory
            boa_dir = PROJECT_ROOT / "boa"
            if boa_dir.exists():
                print(f"Importing all BoA PDFs from {boa_dir}...")
                importer.import_all_pdfs(boa_dir)
            else:
                print("Please specify a file path for BoA import.")

    elif args.source == 'all':
        # Import all available sources
        print("=" * 60)
        print("IMPORTING ALL DATA SOURCES")
        print("=" * 60)

        print("\n1. Importing expense CSV...")
        exp_importer = ExpenseCSVImporter(db)
        exp_importer.import_file(PROJECT_ROOT / "expenses_to_submit.csv")

        print("\n2. Importing Ramp reimbursements...")
        ramp_importer = RampImporter(db)
        ramp_importer.import_file(PROJECT_ROOT / "michael_dangelo_expenses.csv")

        print("\n3. Importing Chase credit card statements...")
        chase_dir = PROJECT_ROOT / "chase"
        if chase_dir.exists():
            chase_importer = ChaseStatementImporter(db)
            chase_importer.import_all_pdfs(chase_dir)
        else:
            print("   Chase directory not found, skipping.")

        print("\n4. Importing Bank of America statements...")
        boa_dir = PROJECT_ROOT / "boa"
        if boa_dir.exists():
            boa_importer = BankOfAmericaImporter(db)
            boa_importer.import_all_pdfs(boa_dir)
        else:
            print("   BoA directory not found, skipping.")

        print("\n" + "=" * 60)
        print("IMPORT COMPLETE")
        print("=" * 60)

    db.close()


def cmd_reconcile(args):
    """Run reconciliation."""
    db = Database()
    engine = ReconciliationEngine(db)

    print("Running reconciliation...")
    results = engine.reconcile_all()

    print("\nReconciliation Results:")
    print("-" * 40)
    for check_name, result in results.items():
        print(f"\n{check_name}:")
        for key, value in result.items():
            print(f"  {key}: {value}")

    db.close()


def cmd_report(args):
    """Generate reports."""
    db = Database()
    reporter = ReportGenerator(db)

    if args.type == 'status':
        print(reporter.status_report())
    elif args.type == 'discrepancies':
        print(reporter.discrepancy_report())
    elif args.type == 'full':
        print(reporter.full_report())
    else:
        print(reporter.status_report())

    db.close()


def cmd_status(args):
    """Show current status."""
    db = Database()
    reporter = ReportGenerator(db)
    print(reporter.status_report())
    db.close()


def cmd_query(args):
    """Run custom SQL query."""
    db = Database()
    try:
        results = db.execute(args.sql).fetchall()
        if results:
            # Print header
            print(" | ".join(results[0].keys()))
            print("-" * 60)
            for row in results:
                print(" | ".join(str(v) for v in row))
        else:
            print("No results.")
    except sqlite3.Error as e:
        print(f"SQL Error: {e}")
    db.close()


def main():
    parser = argparse.ArgumentParser(description="Expense Reconciliation Tool")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # init
    subparsers.add_parser('init', help='Initialize database')

    # import
    import_parser = subparsers.add_parser('import', help='Import data')
    import_parser.add_argument('source', choices=['expenses', 'ramp', 'chase', 'boa', 'all'],
                               help='Data source to import')
    import_parser.add_argument('file', nargs='?', help='File path (for chase)')

    # reconcile
    subparsers.add_parser('reconcile', help='Run reconciliation')

    # report
    report_parser = subparsers.add_parser('report', help='Generate reports')
    report_parser.add_argument('type', nargs='?', default='status',
                               choices=['status', 'discrepancies', 'full'],
                               help='Report type')

    # status
    subparsers.add_parser('status', help='Show current status')

    # query
    query_parser = subparsers.add_parser('query', help='Run SQL query')
    query_parser.add_argument('sql', help='SQL query to execute')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    commands = {
        'init': cmd_init,
        'import': cmd_import,
        'reconcile': cmd_reconcile,
        'report': cmd_report,
        'status': cmd_status,
        'query': cmd_query,
    }

    commands[args.command](args)


if __name__ == '__main__':
    main()
