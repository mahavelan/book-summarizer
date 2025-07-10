from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from summarizer import extract_all_text,summarize_with_gemini 
import os
from dotenv import load_dotenv

load_dotenv()
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
        try:
            if page_range:
                start, end = map(int, page_range.strip().split("-"))
                if start < 1 or end > len(pages) or start > end:
                    raise ValueError
                selected_pages = pages[start-1:end]
                text = "\n".join(selected_pages)
                return {"result": summarize_with_gpt(text, "Summarize the following topic based on these pages.")}
            else:
                return {"result": "❌ Please provide a page range like 2-5."}
        except:
            return {"result": "❌ Invalid page range. Use format like 2-5."}

    elif type == "bookconcept":
        full_text = "\n".join(pages)
        return {"result": summarize_with_gpt(full_text, "What is the overall concept or key idea of this book?")}

    return {"result": "❌ Invalid type provided."}
