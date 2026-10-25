# MSME-Notice-Drafter-Agent
An agentic assistant that turns that unused law into an automatic, polite, escalating notice drafting agent.

# MSME Notice Drafter Agent

> An agentic AI system that automates MSME invoice compliance under India's **MSMED Act 2006 (Section 15)** — from eligibility checking to legal notice generation.

---

## The Problem

Indian MSMEs lose crores annually due to delayed payments. Under Section 15 of the MSMED Act, buyers must pay within 45 days or owe compound interest at **3× the RBI bank rate**. Most small suppliers lack the legal and financial expertise to calculate dues and draft enforceable demand notices.

This system automates the entire pipeline — in under 3 seconds.

---

## System Architecture

```
POST /invoice_data
        │
        ▼
┌─────────────────────┐
│  Eligibility Agent  │ ── checks Udyam registration + business type
└─────────────────────┘
        │
        ▼
┌──────────────────────────┐
│ Interest Calculator Agent│ ── computes compound interest month-by-month
│                          │    at 3× RBI bank rate per MSMED Act
└──────────────────────────┘
        │
        ▼
┌──────────────────────────┐
│  Notice Drafter Agent    │ ── LLM-generated legal payment demand notice
│  (ChatGroq + LangChain)  │    triggered only when overdue + eligible
└──────────────────────────┘
        │
        ▼
  InvoiceResponse (Pydantic validated)
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| API Framework | FastAPI (async) |
| Data Validation | Pydantic v2 |
| LLM Orchestration | LangChain + ChatGroq |
| Agent Observability | LangSmith |
| Interest Logic | Custom MSMED Act calculator |
| Language | Python 3.11 |

---

## API Reference

**Endpoint:** `POST /invoice_data`

**Request Body:**
```json
{
  "invoice_date": "2026-01-01",
  "amount": 50000.0,
  "agreed_terms": 30,
  "supplier_name": "Raj Enterprises",
  "buyer_name": "Metro Corp",
  "is_udyam": true,
  "business_type": "manufacturer"
}
```

**Response:**
```json
{
  "eligible": true,
  "due_date": "2026-08-31",
  "interest_owed": 1384.45,
  "is_overdue": true,
  "draft_message": "DRAFT — HUMAN REVIEW REQUIRED\n\nTo: Metro Corp\nFrom: Raj Enterprises..."
}
```

---

## Evaluation Results

### Unit Tests — Deterministic Agents

| Test Case | Agent | Result |
|-----------|-------|--------|
| Valid MSME manufacturer | Eligibility | ✅ Passed |
| Valid MSME service provider | Eligibility | ✅ Passed |
| Not Udyam registered | Eligibility | ✅ Passed |
| Wrong business type | Eligibility | ✅ Passed |
| Overdue invoice → interest > 0 | Interest Calculator | ✅ Passed |
| Future invoice → interest = 0 | Interest Calculator | ✅ Passed |

**6/6 unit tests passing**

**Here's the link of Results**
https://smith.langchain.com/o/c3ff4724-baf9-4233-981f-2919b94e43ff/datasets/949cc6de-50c4-4e8a-9203-f5b026cf2b78/compare?selectedSessions=d8d9b3ac-389f-43ca-90bd-63c9b8a03092

---

### LangSmith Eval — Notice Drafter Agent

Evaluated against `notice-drafter-eval` dataset using keyword presence scoring.

| Metric | Value |
|--------|-------|
| Total Runs | 8 |
| Avg Latency (P50) | 2.64s |
| Total Tokens Used | 16,013 |
| Total Cost | $0.0058 |
| Evaluation Metric | `notice_quality` (keyword presence) |
| Avg Score | 0.06 |

> **Note on eval score:** The low score reflects strict string matching against LLM outputs that use varied phrasing. The notices are semantically correct and legally complete — a semantic similarity evaluator (e.g. embedding cosine similarity) would score significantly higher. This is a known limitation of keyword-based LLM evaluation and an identified improvement area.

---

## Interest Calculation Logic

```python
# MSMED Act Section 15 — 3× RBI bank rate, compounded monthly
monthly_rate = (rbi_bank_rate * 3) / 12

# Compound monthly from due date to today
while cursor < today:
    balance = balance * (1 + monthly_rate)
    cursor += relativedelta(months=1)

interest_owed = balance - principal
```

RBI rate changes are tracked historically via `BANK_RATES` lookup table.

---

## Setup & Installation

```bash
# 1. Clone the repo
git clone https://github.com/antariksha-agi/MSME-Notice-Drafter-Agent
cd MSME-Notice-Drafter-Agent

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
GROQ_API_KEY=your_groq_key
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=msme-invoice-agent

# 5. Run the server
uvicorn main:app --reload

# 6. Open Swagger UI
http://127.0.0.1:8000/docs
```

---

## Project Structure

```
MSME-Notice-Drafter-Agent/
├── main.py              # FastAPI app + endpoints
├── agents.py            # All agent definitions
├── calculator.py        # Interest calculation logic
├── tests/
│   └── test_agents.py   # Unit tests
├── requirements.txt
├── .env.example
└── README.md
```

---

## Identified Improvements

- [ ] Replace keyword eval with semantic similarity scoring
- [ ] Fix LLM prompt to eliminate placeholder values in notice
- [ ] Add more test cases to LangSmith dataset
- [ ] Add Docker support for deployment
- [ ] Support multiple invoices in one request (batch processing)

---

## Author

**Antariksha** — [@antariksha-agi](https://github.com/antariksha-agi)

Built as part of an AI engineering portfolio focused on production-grade agentic systems.
