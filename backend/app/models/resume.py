from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)

    content = Column(Text, nullable=True)  # extracted text

    job_id = Column(Integer, ForeignKey("jobs.id"))