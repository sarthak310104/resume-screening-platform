from sqlalchemy import Column, Integer, Text, Float, ForeignKey

from app.database import Base


class ScreeningResult(Base):
    __tablename__ = "screening_results"

    id = Column(Integer, primary_key=True, index=True)

    score = Column(Float)

    strengths = Column(Text)

    gaps = Column(Text)

    summary = Column(Text)

    resume_id = Column(Integer, ForeignKey("resumes.id"))

    job_id = Column(Integer, ForeignKey("jobs.id"))