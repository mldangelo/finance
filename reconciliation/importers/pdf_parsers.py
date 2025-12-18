#!/usr/bin/env python3
"""
PDF Statement Parsers for Chase and Bank of America

Extracts transactions from PDF statements using pdfplumber.
"""

import re
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import List, Optional, Tuple

import pdfplumber


@dataclass
class ParsedTransaction:
    """A transaction parsed from a PDF statement."""
    date: str  # YYYY-MM-DD
    description: str
    amount: Decimal
    is_credit: bool  # True for payments/refunds, False for purchases
    category: Optional[str] = None
    raw_text: Optional[str] = None


class ChasePDFParser:
    """Parse Chase credit card PDF statements."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.statement_year = self._extract_year_from_filename()
        self.statement_month = self._extract_month_from_filename()

    def _extract_year_from_filename(self) -> int:
        """Extract year from filename like 20250817-statements-2030-.pdf"""
        match = re.search(r'(\d{4})\d{4}-statements', self.file_path.name)
        if match:
            return int(match.group(1))
        return datetime.now().year

    def _extract_month_from_filename(self) -> int:
        """Extract month from filename."""
        match = re.search(r'\d{4}(\d{2})\d{2}-statements', self.file_path.name)
        if match:
            return int(match.group(1))
        return datetime.now().month

    def parse(self) -> List[ParsedTransaction]:
        """Parse all transactions from the PDF."""
        transactions = []

        with pdfplumber.open(self.file_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"

            # Find the ACCOUNT ACTIVITY section
            transactions = self._parse_transactions(full_text)

        return transactions

    def _parse_transactions(self, text: str) -> List[ParsedTransaction]:
        """Parse transactions from the statement text."""
        transactions = []

        # Pattern for transaction lines: MM/DD Description Amount
        # Amount can be positive or negative (with leading -)
        tx_pattern = re.compile(
            r'(\d{2}/\d{2})\s+'  # Date MM/DD
            r'(.+?)\s+'  # Description
            r'(-?[\d,]+\.\d{2})\s*$',  # Amount
            re.MULTILINE
        )

        # Find all matches
        for match in tx_pattern.finditer(text):
            date_str = match.group(1)
            description = match.group(2).strip()
            amount_str = match.group(3).replace(',', '')

            # Skip header rows and non-transaction lines
            if any(skip in description.lower() for skip in [
                'date of', 'transaction', 'merchant name', 'amount',
                'page', 'account', 'continued', 'total'
            ]):
                continue

            # Parse amount
            amount = Decimal(amount_str)
            is_credit = amount < 0

            # Convert date to full format
            month, day = map(int, date_str.split('/'))

            # Determine year based on statement month
            if month > self.statement_month:
                # Transaction is from previous year
                year = self.statement_year - 1
            else:
                year = self.statement_year

            full_date = f"{year}-{month:02d}-{day:02d}"

            transactions.append(ParsedTransaction(
                date=full_date,
                description=description,
                amount=abs(amount),
                is_credit=is_credit,
                raw_text=match.group(0)
            ))

        return transactions

    def get_statement_period(self) -> Tuple[str, str]:
        """Get the statement period from the PDF."""
        with pdfplumber.open(self.file_path) as pdf:
            first_page = pdf.pages[0].extract_text()

            # Look for statement period
            period_match = re.search(
                r'(\w+\s+\d{4})\s*New Balance',
                first_page
            )
            if period_match:
                return period_match.group(1), period_match.group(1)

        return "", ""


class BankOfAmericaPDFParser:
    """Parse Bank of America PDF statements."""

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def parse(self) -> List[ParsedTransaction]:
        """Parse all transactions from the PDF."""
        transactions = []

        with pdfplumber.open(self.file_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"

            # Parse deposits (income/reimbursements)
            deposits = self._parse_deposits(full_text)
            transactions.extend(deposits)

            # Parse withdrawals (payments)
            withdrawals = self._parse_withdrawals(full_text)
            transactions.extend(withdrawals)

        return transactions

    def _parse_deposits(self, text: str) -> List[ParsedTransaction]:
        """Parse deposit transactions."""
        transactions = []

        # Find deposits section
        deposits_section = re.search(
            r'Deposits and other additions\s*\n(.*?)(?:Total deposits|Withdrawals)',
            text,
            re.DOTALL
        )

        if not deposits_section:
            return transactions

        section_text = deposits_section.group(1)

        # Pattern: MM/DD/YY Description Amount
        tx_pattern = re.compile(
            r'(\d{2}/\d{2}/\d{2})\s+'  # Date MM/DD/YY
            r'(.+?)\s+'  # Description
            r'([\d,]+\.\d{2})\s*$',  # Amount
            re.MULTILINE
        )

        for match in tx_pattern.finditer(section_text):
            date_str = match.group(1)
            description = match.group(2).strip()
            amount_str = match.group(3).replace(',', '')

            # Skip headers
            if 'date' in description.lower() or 'description' in description.lower():
                continue

            # Parse date
            month, day, year = date_str.split('/')
            full_date = f"20{year}-{month}-{day}"

            # Identify transaction type
            category = self._categorize_deposit(description)

            transactions.append(ParsedTransaction(
                date=full_date,
                description=description,
                amount=Decimal(amount_str),
                is_credit=True,  # Deposits are credits
                category=category,
                raw_text=match.group(0)
            ))

        return transactions

    def _parse_withdrawals(self, text: str) -> List[ParsedTransaction]:
        """Parse withdrawal transactions."""
        transactions = []

        # Find withdrawals section
        withdrawals_section = re.search(
            r'Withdrawals and other subtractions\s*\n(.*?)(?:Total withdrawals|Checks|Service fees|Braille)',
            text,
            re.DOTALL
        )

        if not withdrawals_section:
            return transactions

        section_text = withdrawals_section.group(1)

        # Pattern: MM/DD/YY Description -Amount or Amount
        tx_pattern = re.compile(
            r'(\d{2}/\d{2}/\d{2})\s+'  # Date MM/DD/YY
            r'(.+?)\s+'  # Description
            r'-?([\d,]+\.\d{2})\s*$',  # Amount (may have leading -)
            re.MULTILINE
        )

        for match in tx_pattern.finditer(section_text):
            date_str = match.group(1)
            description = match.group(2).strip()
            amount_str = match.group(3).replace(',', '')

            # Skip headers
            if 'date' in description.lower() or 'description' in description.lower():
                continue

            # Parse date
            month, day, year = date_str.split('/')
            full_date = f"20{year}-{month}-{day}"

            # Identify transaction type
            category = self._categorize_withdrawal(description)

            transactions.append(ParsedTransaction(
                date=full_date,
                description=description,
                amount=Decimal(amount_str),
                is_credit=False,  # Withdrawals are debits
                category=category,
                raw_text=match.group(0)
            ))

        return transactions

    def _categorize_deposit(self, description: str) -> str:
        """Categorize a deposit transaction."""
        desc_lower = description.lower()

        if 'promptfoo' in desc_lower:
            if 'payroll' in desc_lower:
                return 'salary'
            return 'reimbursement'
        if 'interest' in desc_lower:
            return 'interest'
        if 'transfer' in desc_lower:
            return 'transfer'

        return 'deposit'

    def _categorize_withdrawal(self, description: str) -> str:
        """Categorize a withdrawal transaction."""
        desc_lower = description.lower()

        if 'chase credit' in desc_lower:
            return 'cc_payment_chase'
        if 'american express' in desc_lower or 'amex' in desc_lower:
            return 'cc_payment_amex'
        if 'venmo' in desc_lower:
            return 'venmo'
        if 'paypal' in desc_lower:
            return 'paypal'
        if 'con ed' in desc_lower:
            return 'utility'
        if 'bill payment' in desc_lower:
            return 'bill_payment'

        return 'withdrawal'

    def get_statement_period(self) -> Tuple[str, str]:
        """Get the statement period from the PDF."""
        with pdfplumber.open(self.file_path) as pdf:
            first_page = pdf.pages[0].extract_text()

            # Look for date range
            period_match = re.search(
                r'(\w+\s+\d+,\s+\d{4})\s+to\s+(\w+\s+\d+,\s+\d{4})',
                first_page
            )
            if period_match:
                return period_match.group(1), period_match.group(2)

        return "", ""


def parse_chase_statement(file_path: Path) -> List[ParsedTransaction]:
    """Convenience function to parse a Chase statement."""
    parser = ChasePDFParser(file_path)
    return parser.parse()


def parse_boa_statement(file_path: Path) -> List[ParsedTransaction]:
    """Convenience function to parse a Bank of America statement."""
    parser = BankOfAmericaPDFParser(file_path)
    return parser.parse()


# Test the parsers
if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python pdf_parsers.py <pdf_file>")
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if 'chase' in file_path.parent.name.lower() or 'chase' in file_path.name.lower():
        print(f"Parsing Chase statement: {file_path}")
        transactions = parse_chase_statement(file_path)
    else:
        print(f"Parsing BoA statement: {file_path}")
        transactions = parse_boa_statement(file_path)

    print(f"\nFound {len(transactions)} transactions:\n")

    for tx in transactions[:20]:
        credit_indicator = "+" if tx.is_credit else "-"
        print(f"  {tx.date} | {credit_indicator}${tx.amount:>10,.2f} | {tx.description[:50]}")

    if len(transactions) > 20:
        print(f"  ... and {len(transactions) - 20} more")

    total = sum(tx.amount if not tx.is_credit else -tx.amount for tx in transactions)
    print(f"\n  Net total: ${total:,.2f}")
