from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import json

from app.database import SessionLocal
from app.models.job import Job
from app.models.resume import Resume
from app.models.screening import ScreeningResult
from app.services.ai_scoring import score_resume

router = APIRouter()


class ScreeningRequest(BaseModel):
    job_id: int
    resume_id: int


@router.post("/score")
def screen_resume(data: ScreeningRequest):
    db = SessionLocal()

    job = db.query(Job).filter(Job.id == data.job_id).first()

    if not job:
        db.close()
        raise HTTPException(status_code=404, detail="Job not found")

    resume = db.query(Resume).filter(
        Resume.id == data.resume_id
    ).first()

    if not resume:
        db.close()
        raise HTTPException(status_code=404, detail="Resume not found")

    result = score_resume(
        job.description,
        resume.content
    )

    screening = ScreeningResult(
        score=result["score"],
        strengths=json.dumps(result["strengths"]),
        gaps=json.dumps(result["gaps"]),
        summary=result["summary"],
        resume_id=resume.id,
        job_id=job.id
    )

    db.add(screening)
    db.commit()
    db.refresh(screening)

    response = {
        "screening_id": screening.id,
        **result
    }

    db.close()

    return response

@router.get("/")
def get_screenings():
    db = SessionLocal()

    screenings = db.query(ScreeningResult).all()

    db.close()

    return screenings


@router.get("/job/{job_id}")
def get_ranked_candidates(job_id: int):
    db = SessionLocal()

    results = (
        db.query(ScreeningResult)
        .filter(ScreeningResult.job_id == job_id)
        .order_by(ScreeningResult.score.desc())
        .all()
    )

    response = [
        {
            "resume_id": r.resume_id,
            "score": r.score,
            "strengths": json.loads(r.strengths),
            "gaps": json.loads(r.gaps),
            "summary": r.summary
        }
        for r in results
    ]

    db.close()

    return response