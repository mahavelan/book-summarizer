from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from summarizer import summarize_chapters, summarize_topics, summarize_concept

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
    page_range: str = Form(None)  # ✅ optional field for topic summary
):
    content = await file.read()

    if type == "chapter":
        result = summarize_chapters(content)
    elif type == "topic":
        result = summarize_topics(content, page_range)
    elif type == "bookconcept":
        result = summarize_concept(content)
    else:
        result = "Invalid type selected"
    return {"result": result}
