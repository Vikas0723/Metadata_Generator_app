import streamlit as st
import docx2txt
from io import StringIO, BytesIO
import tempfile
import fitz  # PyMuPDF
import json
from collections import Counter
import re
import os
from langdetect import detect
import spacy
import spacy
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


from google.cloud import vision
from PIL import Image

# --- Initialize Google Vision Client ---
if "VISION_JSON" in st.secrets:
    with open("vision-key.json", "w") as f:
        f.write(st.secrets["VISION_JSON"])
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "vision-key.json"

# --- Load SpaCy Model ---
nlp = spacy.load("en_core_web_sm")

# --- OCR with Google Vision using pixmap directly ---
def preprocess_pixmap(pixmap):
    img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
    img = img.convert("L")  # Grayscale
    img = img.point(lambda x: 0 if x < 140 else 255, '1')  # Binarize
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

def google_ocr_from_pixmap(pixmap):
    content = preprocess_pixmap(pixmap)
    image = vision.Image(content=content)
    image_context = vision.ImageContext(language_hints=["en", "hi"])

    response = vision_client.document_text_detection(image=image, image_context=image_context)
    if not response.full_text_annotation.text:
        response = vision_client.text_detection(image=image, image_context=image_context)
    if response.error.message:
        raise Exception(f"Vision API error: {response.error.message}")
    return response.full_text_annotation.text.strip() if response.full_text_annotation.text else ""

# --- Text Extraction Functions ---
def extract_text_from_pdf(file):
    text = ""
    debug_log = []
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for i, page in enumerate(doc):
            extracted = page.get_text()
            if extracted and extracted.strip() and len(extracted.strip()) > 10:
                text += extracted
                debug_log.append(f"Page {i+1}: Text extracted using get_text()")
            else:
                debug_log.append(f"Page {i+1}: No text found, using Google Vision OCR")
                pix = page.get_pixmap(dpi=300)
                try:
                    ocr_text = google_ocr_from_pixmap(pix)
                    text += ocr_text
                    debug_log.append(f"Page {i+1}: OCR succeeded")
                except Exception as e:
                    debug_log.append(f"Page {i+1}: OCR failed - {e}")
    return text, debug_log

def extract_text_from_docx(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        tmp.write(file.read())
        tmp.flush()
        text = docx2txt.process(tmp.name)
    return text, []

def extract_text_from_txt(file):
    stringio = StringIO(file.getvalue().decode("utf-8"))
    return stringio.read(), []

def extract_text(file):
    if file.type == "application/pdf":
        return extract_text_from_pdf(file)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(file)
    elif file.type == "text/plain":
        return extract_text_from_txt(file)
    else:
        return "Unsupported file format.", []

# --- Metadata and NLP ---
def generate_metadata(text):
    from langdetect.lang_detect_exception import LangDetectException
    def safe_detect_language(txt):
        try:
            return detect(txt)
        except LangDetectException:
            return "Unknown"

    return {
        "character_count": len(text),
        "word_count": len(text.split()),
        "line_count": len(text.splitlines()),
        "starts_with": text[:50] + "..." if len(text) > 50 else text,
        "ends_with": text[-50:] + "..." if len(text) > 50 else text,
        "language": safe_detect_language(text) if len(text.strip()) > 20 else "Unknown"
    }

def guess_title(text):
    lines = text.strip().split('\n')
    for line in lines:
        clean_line = line.strip()
        if len(clean_line.split()) <= 10 and (clean_line.isupper() or clean_line.istitle()):
            return clean_line
    return lines[0] if lines else "Unknown Title"

def extract_key_sentences(text, sentence_count=5):
    sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20]
    words = re.findall(r'\w+', text.lower())
    common_words = set(word for word, _ in Counter(words).most_common(50))

    def score(sentence):
        words_in_sentence = re.findall(r'\w+', sentence.lower())
        return sum(word in common_words for word in words_in_sentence)

    ranked = sorted(sentences, key=score, reverse=True)
    return ranked[:sentence_count]

def extract_named_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in ["PERSON", "ORG", "GPE", "DATE", "EVENT"]]

# --- UI Layout ---
st.set_page_config(page_title="Metadata Generator", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
        .main { background: linear-gradient(135deg, #f0f4f8, #ffffff); color: #333; }
        .stApp { font-family: 'Segoe UI', sans-serif; }
        h1.title { font-size: 2.8em; color: #004d80; margin-bottom: 0.5em; text-align: center; }
        .metadata-box {
            background-color: #e8f5e9;
            padding: 15px;
            border-radius: 8px;
            font-size: 16px;
            color: #2e7d32;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title'>🧾 Metadata Generator</h1>", unsafe_allow_html=True)

with st.container():
    uploaded_file = st.file_uploader("Upload a PDF, DOCX, or TXT file", type=["pdf", "docx", "txt"])

    if uploaded_file is not None:
        with st.spinner("🔍 Extracting text..."):
            text, debug_log = extract_text(uploaded_file)

        if not text.strip():
            st.warning("⚠️ No extractable text found. This file may be empty or OCR failed.")
            if debug_log:
                st.expander("Show Debug Log").write("\n".join(debug_log))
        else:
            st.subheader("📄 Extracted Text")
            st.text_area("", text, height=500)

            st.subheader("📊 Structured Metadata")
            metadata = generate_metadata(text)
            title = guess_title(text)
            st.markdown(f"""
            <div class='metadata-box'>
                <strong>Title (Guessed):</strong> {title}<br>
                <strong>Language:</strong> {metadata['language']}<br>
                <strong>Character Count:</strong> {metadata['character_count']}<br>
                <strong>Word Count:</strong> {metadata['word_count']}<br>
                <strong>Line Count:</strong> {metadata['line_count']}<br>
                <strong>Starts With:</strong> {metadata['starts_with']}<br>
                <strong>Ends With:</strong> {metadata['ends_with']}<br>
            </div>
            """, unsafe_allow_html=True)

            st.subheader("🔍 Key Semantic Sentences")
            key_sentences = extract_key_sentences(text)
            for i, sent in enumerate(key_sentences, 1):
                st.markdown(f"**{i}.** {sent}")

            st.subheader("🧠 Named Entities (NER)")
            named_entities = extract_named_entities(text)
            if named_entities:
                for entity, label in named_entities:
                    st.markdown(f"- **{entity}** ({label})")
            else:
                st.write("No named entities found.")

            st.subheader("📝 Readable Summary")
            summary = f"This document, titled **\"{title}\"**, is written in **{metadata['language']}**.\n"
            summary += f"It contains approximately **{metadata['word_count']} words** and spans **{metadata['line_count']} lines**.\n"
            summary += "Some important sentences include:\n\n"
            for s in key_sentences:
                summary += f"- {s}\n"
            if named_entities:
                summary += "\nIt mentions key entities like: " + ", ".join(set([e[0] for e in named_entities]))
            st.markdown(summary)

            st.subheader("📥 Download Metadata as JSON")
            combined_data = {
                "title": title,
                "metadata": metadata,
                "key_sentences": key_sentences,
                "named_entities": named_entities,
                "summary": summary.strip(),
                "debug_log": debug_log
            }
            json_data = json.dumps(combined_data, indent=2)
            st.download_button("Download JSON", json_data, file_name="metadata.json", mime="application/json")
    else:
        st.info("📁 Please upload a file to begin metadata extraction.")
