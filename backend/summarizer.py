import io
from PyPDF2 import PdfReader
from docx import Document
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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

def summarize_with_gpt(text, prompt="Summarize this text"):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text[:6000]}
            ],
            max_tokens=800,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except openai.error.OpenAIError as e:
        return f"❌ GPT Error: {str(e)}"
