# 🧾 Metadata Generator Web App

This is a simple, smart web application built using **Streamlit** that allows users to upload `.pdf`, `.docx`, or `.txt` files and automatically extracts useful metadata such as:

- Estimated **document title**
- **Language**, **word count**, **line count**
- Key **semantic sentences**
- Extracted **named entities** (names, dates, organizations)
- A readable **summary**
- Option to **download metadata in JSON** format

This project uses OCR (Optical Character Recognition) via **Google Cloud Vision API** for scanned or image-based PDFs.

---

## 📚 Features

- ✅ Supports **PDF**, **Word (.docx)**, and **Text (.txt)** files
- ✅ Handles scanned documents using **Google OCR**
- ✅ Detects **language** of the text
- ✅ Extracts **key sentences** from the content
- ✅ Performs **basic NER (Named Entity Recognition)** without heavy NLP models
- ✅ Generates a **summary** of the file
- ✅ Allows **JSON download** of the metadata
- ✅ Easy-to-use **Streamlit UI**

---

## 🛠️ Tech Stack

| Tool/Library            | Purpose                                 |
|-------------------------|-----------------------------------------|
| `Streamlit`             | Web App UI                              |
| `PyMuPDF (fitz)`        | PDF text & image extraction             |
| `docx2txt`              | Extract text from Word files            |
| `langdetect`            | Detect document language                |
| `Google Cloud Vision`   | OCR for scanned PDFs                    |
| `re` + regex            | Lightweight named entity extraction     |
| `Pillow`                | Image processing                        |
| `json`                  | Exporting metadata                     |

---

## 🚀 How to Run This App Locally
Follow these steps to set up and run the Metadata Generator web app on your local machine.

## 🚀 How to Run This App Locally

Follow these steps to set up and run the Metadata Generator web app on your local machine.

### ✅ 1. Clone the Repository

If this project is on GitHub:

```bash
git clone https://github.com/your-username/metadata-generator-app.git
cd metadata-generator-app


