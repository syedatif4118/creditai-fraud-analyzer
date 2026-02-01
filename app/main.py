from datetime import date
from ocr.ocr_engine import run_ocr, detect_document_type
from schemas.financial_doc import FinancialDocument
from storage.db import init_db
from fraud.anomaly_detector import parse_transactions, detect_fraud_anomalies


def ingest_document(file_path: str):
    text = run_ocr(file_path)
    doc_type = detect_document_type(text)

    # Parse transactions
    transactions = parse_transactions(text)

    # Detect fraud flags
    fraud_flags = detect_fraud_anomalies(transactions)

    doc = FinancialDocument(
        document_type=doc_type,
        institution=None,  # can extract later
        customer_name=None,
        account_number=None,
        statement_period=None,
        extracted_text=text,
        entities=fraud_flags,  # ← fraud flags here!
        ingestion_date=date.today(),
        source_file=file_path
    )

    # ... save to DB if ready ...

    print("\n--- FRAUD / ANOMALY FLAGS ---")
    for flag in fraud_flags:
        print(f"{flag.label}: {flag.value} (conf: {flag.confidence})")

    print("\n--- PARSED TRANSACTIONS SAMPLE ---")
    print(transactions[:5])

if __name__ == "__main__":
    init_db()

    import glob

    # Test on synthetic files (legit and fraud)
    pdf_files = glob.glob("data/synthetic/*.pdf")

    # Or pick specific ones for quick testing
    # pdf_files = [
    #     "data/synthetic/account_518794_legit.pdf",
    #     "data/synthetic/account_724262_fraud.pdf",
    #     "data/synthetic/account_143831_fraud.pdf"
    # ]

    for pdf_path in pdf_files[:5]:  # limit to 5 to avoid long run
        print(f"\n{'='*40}")
        print(f"Processing synthetic file: {pdf_path}")
        print(f"{'='*40}")
        ingest_document(pdf_path)
        print("\n")
