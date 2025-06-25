# Metadata Generator with Google Cloud Vision OCR

This app extracts text and metadata from uploaded files (PDF, DOCX, TXT) using OCR powered by Google Cloud Vision API.

## Features

- OCR for scanned PDFs and images using Google Cloud Vision
- Language detection
- Named Entity Recognition (NER) using spaCy
- Title guessing and key sentence extraction
- JSON export of metadata

## How to Use

1. Upload your `vision-key.json` securely (never commit it to GitHub).
2. Run locally with `streamlit run app.py` or deploy on [Streamlit Cloud](https://streamlit.io/cloud).
3. Make sure to set your Google credentials properly:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=vision-key.json
```

## Setup

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Deployment Note

Tesseract has been removed to ensure compatibility with Streamlit Cloud.

---

Built with ❤️ using Streamlit and Google Cloud.
