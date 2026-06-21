from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException

import json

from app.database import SessionLocal
from app.models.job import Job
from app.models.resume import Resume
from app.models.screening import ScreeningResult
from app.schemas.job import JobCreate

router = APIRouter()

@router.get("/")
def get_jobs():
    db = SessionLocal()

    jobs = db.query(Job).all()

    db.close()

    return jobs

@router.post("/")
def create_job(job: JobCreate):
    db: Session = SessionLocal()

    new_job = Job(
        title=job.title,
        description=job.description,
        user_id=1
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    db.close()

    return {
        "id": new_job.id,
        "title": new_job.title,
        "description": new_job.description
    }

@router.get("/{job_id}/candidates")
def get_job_candidates(job_id: int):
    db = SessionLocal()

    # Check if job exists
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # Get all screening results for this job
    screenings = (
        db.query(ScreeningResult)
        .filter(ScreeningResult.job_id == job_id)
        .order_by(ScreeningResult.score.desc())
        .all()
    )

    candidates = []

    for screening in screenings:
        resume = (
            db.query(Resume)
            .filter(Resume.id == screening.resume_id)
            .first()
        )

        if resume:
            candidates.append({
                "resume_id": resume.id,
                "filename": resume.filename,
                "score": screening.score,
                "summary": screening.summary,
                "strengths": json.loads(screening.strengths),
                "gaps": json.loads(screening.gaps)
            })

    db.close()

    return {
        "job_id": job.id,
        "job_title": job.title,
        "candidate_count": len(candidates),
        "candidates": candidates
    }