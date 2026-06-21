from fastapi import APIRouter, UploadFile, File
import os
import shutil
import fitz  # PyMuPDF
import json

from app.models.job import Job
from app.models.screening import ScreeningResult
from app.services.ai_scoring import score_resume
from app.database import SessionLocal
from app.models.resume import Resume

router = APIRouter()

UPLOAD_DIR = "uploads"


def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text

@router.get("/")
def get_resumes():
    db = SessionLocal()

    resumes = db.query(Resume).all()

    db.close()

    return resumes


@router.post("/upload")
def upload_resume(job_id: int, file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # 1. Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Extract text from PDF
    extracted_text = extract_text_from_pdf(file_path)

    # 3. Save Resume to DB
    db = SessionLocal()

    new_resume = Resume(
        filename=file.filename,
        filepath=file_path,
        content=extracted_text,
        job_id=job_id
    )

    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    # Default values in case Gemini fails
    screening = None
    result = None

    try:
        # 4. Get Job
        job = db.query(Job).filter(
            Job.id == job_id
        ).first()

        # 5. Run AI Screening
        if job:
            result = score_resume(
                job.description,
                extracted_text
            )

            screening = ScreeningResult(
                score=result["score"],
                strengths=json.dumps(result["strengths"]),
                gaps=json.dumps(result["gaps"]),
                summary=result["summary"],
                resume_id=new_resume.id,
                job_id=job.id
            )

            db.add(screening)
            db.commit()
            db.refresh(screening)

    except Exception as e:
        print(f"Gemini Error: {e}")

    # Store values before closing DB session
    resume_id = new_resume.id
    screening_id = screening.id if screening else None
    score = result["score"] if result else None

    db.close()

    return {
        "message": "Resume uploaded successfully",
        "resume_id": resume_id,
        "screening_id": screening_id,
        "score": score,
        "text_length": len(extracted_text)
    }