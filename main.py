from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from utils.pdf_parser import parse_pdf
from utils.url_scraper import scrape_url
import os
import json

app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Dictionary to hold user sessions and their data
user_sessions = {}

@app.post("/train")
async def train(pdf_file: UploadFile = File(None), website_url: str = Form(None)):
    # Handle PDF upload
    if pdf_file:
        filepath = os.path.join(UPLOAD_DIR, pdf_file.filename)
        with open(filepath, "wb") as f:
            f.write(await pdf_file.read())
        content = parse_pdf(filepath)
        source = "pdf"
    # Handle URL input
    elif website_url:
        content = scrape_url(website_url)
        source = "url"
    else:
        return JSONResponse(status_code=400, content={"error": "No input provided."})

    # Generate a unique session ID for the user
    user_id = str(len(user_sessions) + 1)
    user_sessions[user_id] = content  # Store the content for this user

    # Save the content to a file (optional, can store in DB)
    session_file = os.path.join(UPLOAD_DIR, f"{user_id}.json")
    with open(session_file, "w") as f:
        json.dump({"source": source, "content": content}, f)

    return {
        "user_id": user_id,
        "source": source,
        "characters_received": len(content),
        "sample": content[:500] + "..."
    }

@app.post("/chat")
async def chat(user_id: str, message: str):
    # Retrieve the content associated with the user
    if user_id not in user_sessions:
        return JSONResponse(status_code=404, content={"error": "User not found"})

    # Get the training content for this user
    user_data = user_sessions[user_id]
    
    # Simple logic: just return the content that contains the message
    # You can replace this with an actual AI model logic
    if message.lower() in user_data.lower():
        response = f"Bot: Found a match! Here’s part of the content: {user_data[:500]}..."
    else:
        response = "Bot: Sorry, I couldn’t find any relevant information."
    
    return {"response": response}
