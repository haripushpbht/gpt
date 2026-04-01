# Student Math + Physics Solver (Class 1–12)

A beginner-friendly app that accepts typed or image-based questions and returns student-friendly, step-by-step solutions with rules/formulas used in each step.

## Architecture

- **Streamlit UI (`main.py`)**
  - Collects typed question, optional image, class level, and language mode.
  - Sends request to FastAPI backend.
  - Displays OCR text (if image used), structured solution, and copy/download button.

- **FastAPI backend (`api.py`)**
  - Exposes `/solve` endpoint.
  - Merges typed + OCR question input.
  - Calls OCR module when image is uploaded.
  - Calls solver module to get AI explanation.

- **OCR module (`ocr.py`)**
  - Uses `pytesseract` + PIL preprocessing for text extraction.
  - Cleans noisy OCR output.
  - Returns readable question text.

- **AI solver module (`solver.py`)**
  - Uses OpenAI API with fixed system prompt:
    - "You are a mathematics and physics teacher. Solve step by step, explain simply, and mention rules used in each step."
  - Applies class-based difficulty:
    - 1–5: simple
    - 6–10: medium
    - 11–12: detailed
  - Supports `english`, `hindi`, and `bilingual` explanation modes.

## Folder Structure

```bash
.
├── api.py
├── main.py
├── ocr.py
├── solver.py
├── requirements.txt
└── README.md
```

## Installation

1. Install system dependency (Tesseract):
   - Ubuntu/Debian:
     ```bash
     sudo apt-get update
     sudo apt-get install -y tesseract-ocr
     ```

2. Create virtual env and install Python dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Set environment variables:

```bash
export OPENAI_API_KEY="your_api_key_here"
# Optional
export OPENAI_MODEL="gpt-4o-mini"
export BACKEND_URL="http://localhost:8000"
```

## Run Instructions

### Terminal 1 (Backend)

```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### Terminal 2 (Frontend)

```bash
streamlit run main.py
```

Open `http://localhost:8501`.

## Deployment Notes (Render / Vercel)

- **Render:**
  - Deploy FastAPI as a web service (`uvicorn api:app --host 0.0.0.0 --port $PORT`)
  - Deploy Streamlit as separate web service (`streamlit run main.py --server.port $PORT --server.address 0.0.0.0`)

- **Vercel:**
  - Best suited for backend API route deployment with Python runtime.
  - Host Streamlit separately (Render/Streamlit Cloud) and point `BACKEND_URL` to deployed API.

## Error Handling Included

- OCR failure returns clear user-friendly error.
- Empty question/image validation in UI and backend.
- API/network error handling in Streamlit with clear feedback.

## Future Mobile App Readiness

- Clear separation of UI and backend logic.
- Backend can be reused directly by Android/iOS or Flutter frontends.
