from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import uuid
import pandas as pd
from generator import generate_metadata
from validator import validate_metadata
from typing import List

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def handle_generation(
    request: Request,
    input_file: UploadFile = File(...)
):
    # Save input files
    batch_id = str(uuid.uuid4())[:8]
    batch_dir = os.path.join(UPLOAD_DIR, batch_id)
    os.makedirs(batch_dir, exist_ok=True)
    
    # Save input Excel
    input_path = os.path.join(batch_dir, input_file.filename)
    with open(input_path, "wb") as f:
        f.write(await input_file.read())
  
    
    # Process generation
    results = generate_metadata(input_path)
    print(results)
    return {"status": "complete", "batch_id": batch_id, "stats":results["stats"]}

@app.post("/validate")
async def handle_validation(
    request: Request,
    metadata_file: UploadFile = File(...)
):
    # Save files
    batch_id = str(uuid.uuid4())[:8]
    batch_dir = os.path.join(UPLOAD_DIR, batch_id)
    os.makedirs(batch_dir, exist_ok=True)

    
    # Save metadata file
    metadata_path = os.path.join(batch_dir, metadata_file.filename)
    print("Meta Data Path : ", metadata_path)
    with open(metadata_path, "wb") as f:
        f.write(await metadata_file.read())
    
    # Process validation
    results = validate_metadata(metadata_path)
    print(results)
    return {
        "status": "complete",
        "batch_id": batch_id,
        "scores": results.to_dict(),
        "overall": results['overall_score'].mean()
    }