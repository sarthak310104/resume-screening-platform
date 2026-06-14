from fastapi import FastAPI

app = FastAPI(
    title="Resume Screening Platform",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Resume Screening Platform API is running"
    }