from fastapi import FastAPI

from app.database import Base, engine

# 👇 VERY IMPORTANT: ensures SQLAlchemy registers all tables
from app.models import user, job, resume, screening

from app.routers import user as user_router
from app.routers import job as job_router
from app.routers import resume as resume_router
from app.routers import screening as screening_router

app = FastAPI()

# create tables
Base.metadata.create_all(bind=engine)

# register routes
app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(job_router.router, prefix="/jobs", tags=["Jobs"])
app.include_router(resume_router.router, prefix="/resumes", tags=["Resumes"])
app.include_router(screening_router.router, prefix="/screening", tags=["Screening"])

@app.get("/")
def root():
    return {"message": "API running"}