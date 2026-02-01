# scripts/generate_synthetic_statements.py

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import random
import os
from pathlib import Path

def generate_statement_from_row(row, output_dir="data/synthetic", fraud_label=""):
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"account_{row.name}_{fraud_label}.pdf")

    c = canvas.Canvas(filename, pagesize=letter)
    w, h = letter

    # Header
    y = h - 80
    c.drawString(100, y, "Synthetic Bank Statement")
    y -= 20
    c.drawString(100, y, f"Account Holder: {row.get('email', 'Unknown')[:10]}...")
    y -= 20
    c.drawString(100, y, f"Income Quantile: {row['income']}")
    y -= 20
    c.drawString(100, y, f"Age Bucket: {row['customer_age']}")
    y -= 20
    c.drawString(100, y, f"Employment: {row.get('employment_status', 'N/A')}")
    y -= 20
    c.drawString(100, y, f"Fraud Label: {row['fraud_bool']} ({'FRAUD' if row['fraud_bool'] else 'Legit'})")

    # Transaction table header
    y -= 40
    c.drawString(50, y, "Date".ljust(15) + "Description".ljust(35) + "Amount")
    y -= 20

    # Simulated transactions (this is the loop!)
    for i in range(random.randint(5, 12)):
        date = f"{random.randint(1,28)} Feb 2025"
        desc_options = ["Salary Deposit", "Groceries", "Rent Payment", "Transfer In", "ATM Withdrawal"]
        if row['fraud_bool'] == 1 and random.random() < 0.5:
            desc_options += ["Cash Deposit Round", "Quick Transfer", "Unknown Merchant"]
        desc = random.choice(desc_options)
        amount = round(random.uniform(50, 2000) * (row['income'] + 1), 2)
        if "Withdrawal" in desc or "Payment" in desc:
            amount = -amount

        # Draw with aligned columns
        c.drawString(50, y, date.ljust(15))
        c.drawString(150, y, desc.ljust(35))
        c.drawString(350, y, f"£{amount:,.2f}".rjust(15))
        y -= 15

    c.save()
    print(f"Generated: {filename}")

# ────────────────────────────────────────────────
# Load CSV (your confirmed path)
CSV_PATH = "/Users/atif/Desktop/credai/creditai/app/data/Base.csv"

print(f"Trying to load: {CSV_PATH}")

if not os.path.exists(CSV_PATH):
    print(f"ERROR: File not found at {CSV_PATH}")
    exit(1)

df = pd.read_csv(CSV_PATH)

# Sample 10 legit + 10 fraud
legit = df[df['fraud_bool'] == 0].sample(10, random_state=42)
fraud = df[df['fraud_bool'] == 1].sample(10, random_state=42)

for _, row in legit.iterrows():
    generate_statement_from_row(row, fraud_label="legit")

for _, row in fraud.iterrows():
    generate_statement_from_row(row, fraud_label="fraud")

print("Generation complete! Check data/synthetic/ folder.")