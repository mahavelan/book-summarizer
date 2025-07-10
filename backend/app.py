from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from summarizer import extract_all_text, summarize_with_gpt
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/summarize")
async def summarize(
    file: UploadFile = File(...),
    type: str = Form(...),
    page_range: Optional[str] = Form(None)
):
    content = await file.read()
    pages = extract_all_text(content)

    if type == "chapter":
        full_text = "\n".join(pages)
        return {"result": summarize_with_gpt(full_text, "Summarize the text chapter by chapter.")}

    elif type == "topic":
        if page_range:
            try:
                start, end = map(int, page_range.strip().split("-"))
                selected_pages = pages[start-1:end]
                text = "\n".join(selected_pages)
                return {"result": summarize_with_gpt(text, "Summarize the following topic based on these pages.")}
            except:
                return {"result": "❌ Invalid page range. Use format like 2-5."}
        return {"result": "❌ Page range is required for topic summary."}

    elif type == "bookconcept":
        full_text = "\n".join(pages)
        return {"result": summarize_with_gpt(full_text, "What is the overall concept or key idea of this book?")}

    return {"result": "❌ Invalid type provided."}
