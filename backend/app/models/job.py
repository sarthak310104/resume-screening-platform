from sqlalchemy import Column, Integer, String, Text, ForeignKey

from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(Text, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))