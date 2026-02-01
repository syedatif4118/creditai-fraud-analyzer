# app/fraud/anomaly_detector.py
import re
from typing import List, Dict, Optional
from datetime import datetime
import statistics  # built-in

from schemas.financial_doc import FinancialEntity, FinancialDocument

import re
from typing import List, Dict

def parse_transactions(text: str) -> List[Dict]:
    """
    Parser for multi-line synthetic PDFs:
    - Date on line 1
    - Description on line 2
    - Amount on line 3 (with possible leading spaces)
    """
    transactions = []
    lines = text.splitlines()
    i = 0

    while i < len(lines) - 2:  # need at least 3 lines for one transaction
        line = lines[i].strip()

        # Skip non-transaction lines
        if not line or any(skip in line for skip in ["Synthetic Bank Statement", "Account Holder", "Income Quantile", "Age Bucket", "Employment", "Fraud Label", "Date", "Description", "Amount"]):
            i += 1
            continue

        # Check if current line looks like a date
        date_match = re.match(r'^\d{1,2}\s+[A-Za-z]{3}\s+\d{4}$', line)
        if date_match:
            date_str = line

            # Next line: description
            i += 1
            desc = lines[i].strip() if i < len(lines) else ''

            # Next line: amount (may have leading spaces)
            i += 1
            amount_line = lines[i].strip() if i < len(lines) else ''

            # Clean amount
            amount_clean = re.sub(r'[£,\s]', '', amount_line)
            try:
                amount = float(amount_clean)
                trans_type = 'out' if amount < 0 else 'in'
                transactions.append({
                    'date': date_str,
                    'desc': desc or 'No description',
                    'amount': abs(amount),
                    'type': trans_type,
                    'raw': f"{date_str}\n{desc}\n{amount_line}"
                })
            except ValueError:
                # If amount not valid, skip or log
                pass

        else:
            i += 1

    return transactions

def detect_fraud_anomalies(transactions: List[Dict], doc: Optional[FinancialDocument] = None):
    flags = []
    risk_score = 0

    if not transactions:
        return flags, risk_score

    # Rule 1: Suspicious descriptions
    suspicious_desc_count = sum(
        1 for t in transactions
        if any(k in t['desc'] for k in ["Quick Transfer", "Cash Deposit Round", "Unknown Merchant"])
    )

    if suspicious_desc_count >= 2:
        flags.append(FinancialEntity(
            label="High Suspicious Transaction Count",
            value=f"{suspicious_desc_count} suspicious descriptions detected",
            confidence=0.85
        ))
        risk_score += 30

    # Rule 2: Large round amounts
    round_large = [
        t for t in transactions
        if t['amount'] % 100 == 0 and t['amount'] >= 1000
    ]

    if len(round_large) >= 2:
        flags.append(FinancialEntity(
            label="Multiple Round Large Amounts",
            value=f"{len(round_large)} round transactions over £1000",
            confidence=0.80
        ))
        risk_score += 25

    # Rule 3: High outflow velocity
    outflows = [t['amount'] for t in transactions if t['type'] == 'out']

    if len(outflows) >= 3 and sum(outflows) > 5000:
        flags.append(FinancialEntity(
            label="High Outflow Velocity",
            value=f"£{sum(outflows):,.2f} across {len(outflows)} debits",
            confidence=0.75
        ))
        risk_score += 35

    # Cap risk score at 100
    risk_score = min(risk_score, 100)

    return flags, risk_score
