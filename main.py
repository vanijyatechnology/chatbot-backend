from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from utils.pdf_parser import parse_pdf
from utils.url_scraper import scrape_url
import os

app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/train")
async def train(pdf_file: UploadFile = File(None), website_url: str = Form(None)):
    if pdf_file:
        filepath = os.path.join(UPLOAD_DIR, pdf_file.filename)
        with open(filepath, "wb") as f:
            f.write(await pdf_file.read())
        content = parse_pdf(filepath)
        source = "pdf"
    elif website_url:
        content = scrape_url(website_url)
        source = "url"
    else:
        return JSONResponse(status_code=400, content={"error": "No input provided."})

    return {
        "source": source,
        "characters_received": len(content),
        "sample": content[:500] + "..."
    }
