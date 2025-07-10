import io
import os
from PyPDF2 import PdfReader
from docx import Document
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Load Gemini API key from environment
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Use correct Gemini model name
model = genai.GenerativeModel("gemini-pro")

# --- File extractors ---

def extract_text_from_pdf(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    return [page.extract_text() or "" for page in reader.pages]

def extract_text_from_docx(file_bytes):
    doc = Document(io.BytesIO(file_bytes))
    return [para.text for para in doc.paragraphs]

def extract_text_from_txt(file_bytes):
    return io.BytesIO(file_bytes).read().decode("utf-8").splitlines()

def extract_all_text(file_bytes):
    try:
        return extract_text_from_pdf(file_bytes)
    except:
        try:
            return extract_text_from_docx(file_bytes)
        except:
            try:
                return extract_text_from_txt(file_bytes)
            except:
                return ["❌ Unsupported or unreadable file format."]

# --- Gemini Summary Function ---

def summarize_with_gemini(text, prompt="Summarize this text"):
    try:
        response = model.generate_content(f"{prompt}\n\n{text[:30000]}")
        return response.text
    except Exception as e:
        return f"❌ Gemini Error: {str(e)}"
