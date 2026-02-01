import streamlit as st
import pandas as pd
import os
from datetime import datetime
import ollama

from ocr.ocr_engine import run_ocr, detect_document_type
from fraud.anomaly_detector import parse_transactions, detect_fraud_anomalies
from storage.db import init_db

# =========================
# Streamlit Page Config
# =========================
st.set_page_config(
    page_title="CreditAI – Local Fraud & Credit Analyzer",
    layout="wide"
)

st.title("CreditAI: Local Multimodal Credit & Fraud Analyzer")
st.markdown(
    "Upload a bank statement PDF to extract transactions, detect fraud patterns, "
    "and generate **local AI explanations**. No cloud. Apple Silicon friendly."
)

# =========================
# UI State
# =========================
progress_bar = st.progress(0)
status_text = st.empty()

# =========================
# LLM Helpers
# =========================
def serialize_flags(flags):
    return [
        {
            "label": f.label,
            "value": f.value,
            "confidence": round(f.confidence, 2)
        }
        for f in flags
    ]


def generate_fraud_explanation(fraud_flags, transactions, risk_score):
    flags = serialize_flags(fraud_flags)
    sample_tx = transactions[:10]

    prompt = f"""
You are a senior fraud analyst at a credit bureau.

Risk score: {risk_score}/100

Detected fraud indicators:
{flags if flags else "No high-risk fraud indicators detected."}

Sample transactions:
{sample_tx}

Explain in 3–5 sentences:
- Why this statement is risky OR clean
- What an analyst should monitor
- Whether this would pass bureau screening
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[{"role": "user", "content": prompt}],
    )

    return response["message"]["content"].strip()

# =========================
# Init DB
# =========================
init_db()

# =========================
# Upload
# =========================
uploaded_file = st.file_uploader(
    "Upload Bank Statement (PDF)",
    type=["pdf"]
)

if uploaded_file:
    # -------------------------
    # Save file
    # -------------------------
    status_text.text("Saving uploaded file...")
    progress_bar.progress(10)

    temp_path = f"/tmp/{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    # -------------------------
    # OCR
    # -------------------------
    status_text.text("Running OCR...")
    progress_bar.progress(25)

    ocr_text = run_ocr(temp_path)
    doc_type = detect_document_type(ocr_text)

    st.subheader("📄 Document Type")
    st.write(doc_type)

    # -------------------------
    # Parse Transactions
    # -------------------------
    status_text.text("Parsing transactions...")
    progress_bar.progress(45)

    transactions = parse_transactions(ocr_text)

    st.subheader("💳 Extracted Transactions")
    tx_df = pd.DataFrame(transactions)
    st.dataframe(tx_df, use_container_width=True)

    # -------------------------
    # Fraud Detection
    # -------------------------
    status_text.text("Detecting fraud patterns...")
    progress_bar.progress(65)

    fraud_flags, risk_score = detect_fraud_anomalies(transactions)

    st.subheader("🚨 Fraud Signals")
    st.metric("Overall Risk Score", f"{risk_score}/100")

    if fraud_flags:
        for flag in fraud_flags:
            st.warning(
                f"**{flag.label}** — {flag.value} "
                f"(confidence: {round(flag.confidence, 2)})"
            )
    else:
        st.success("No major fraud indicators detected.")

    # -------------------------
    # LLM Explanation (ALWAYS)
    # -------------------------
    st.subheader("🧠 AI Risk Explanation")

    with st.spinner("Generating explanation using local AI..."):
        try:
            explanation = generate_fraud_explanation(
                fraud_flags=fraud_flags,
                transactions=transactions,
                risk_score=risk_score
            )
            st.markdown(explanation)
        except Exception as e:
            st.error("LLM explanation failed")
            st.code(str(e))

    # -------------------------
    # Finish
    # -------------------------
    progress_bar.progress(100)
    status_text.success("Processing complete!")
