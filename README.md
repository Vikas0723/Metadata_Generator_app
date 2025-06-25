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

### ✅ 1. Clone the Repository

If this project is on GitHub:

```bash
git clone https://github.com/your-username/metadata-generator-app.git
cd metadata-generator-app
```

Or if you downloaded the ZIP:

- Extract it
- Open the folder in your terminal

---

### ✅ 2. Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

---

### ✅ 3. Install the Required Libraries

Make sure `pip` is updated, then install:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### ✅ 4. Set Up Google Cloud Vision API (for OCR Support)

This is only needed if you're working with **scanned PDFs**.

#### Step 1: Enable the API
- Go to [https://console.cloud.google.com](https://console.cloud.google.com)
- Create a project or use an existing one
- Enable **Google Cloud Vision API**

#### Step 2: Create a Service Account Key
- Go to IAM & Admin → Service Accounts
- Create a service account and download the JSON key

#### Step 3: Add Your Credentials to the App

Create a `.streamlit/secrets.toml` file in your project folder:

```toml
# .streamlit/secrets.toml

VISION_JSON = """
{ paste your full JSON key content here }
"""
```

Streamlit will automatically load this securely.

---

### ✅ 5. Run the Web App

Now you're ready to launch:

```bash
streamlit run app.py
```

This will open the app in your browser at:

```
http://localhost:8501
```

---

### ✅ 6. Upload a File and View Results

- Click “Browse files” to upload a `.pdf`, `.docx`, or `.txt`
- The app will:
  - Extract text
  - Show metadata and summary
  - Highlight named entities
  - Let you download the JSON output



