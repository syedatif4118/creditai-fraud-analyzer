# CreditAI – Local Fraud & Credit Risk Analyzer

CreditAI is a **credit bureau–style fraud detection and risk analysis system**
built to process real-world financial documents using OCR, rule-based analytics,
and local large language models.

Designed to be **fully local, explainable, and production-inspired**.

---

## 🚀 Features

- 📄 OCR-based bank statement ingestion (PDF)
- 💳 Transaction extraction & normalization
- 🚨 Rule-based fraud & anomaly detection
- 📊 Credit-bureau-style risk scoring (0–100)
- 🧠 Local LLM explanations (offline, Ollama)
- 🧱 SQLite-backed document persistence
- 🍎 Optimized for Apple Silicon (M-series)

---

## 🧠 Architecture


---

## 🛠 Tech Stack

- Python 3.11
- Streamlit
- PaddleOCR
- Pydantic v2
- SQLite
- FAISS (future embeddings)
- Ollama (local LLM inference)

---

## 🔒 Local vs Cloud

| Feature | Local | Streamlit Cloud |
|------|------|------|
OCR | ✅ | ✅ |
Fraud Rules | ✅ | ✅ |
Risk Score | ✅ | ✅ |
LLM Explanation | ✅ | ❌ |
GPU Required | ❌ | ❌ |

---

## 🧪 Use Cases

- Credit bureau document triage
- Fraud pre-screening
- Analyst decision support
- Synthetic identity detection (planned)
- AML & transaction monitoring (planned)

---

## 📈 Portfolio Impact

This project demonstrates:
- Real-world financial domain modeling
- Explainable AI in regulated systems
- Offline-first architecture
- Production-quality data pipelines
- Clear separation of rules vs AI inference

---

## 🔮 Roadmap

- Synthetic identity detection
- Analyst override workflow
- n8n integration
- Embedding-based anomaly detection
- Multi-document risk aggregation

---

## ⚠️ Disclaimer

This project is for **educational and portfolio purposes only**.
Not intended for real credit decisioning.

---

Built with ❤️ on Apple Silicon
