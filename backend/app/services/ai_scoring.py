import os

from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class ScreeningResult(BaseModel):
    score: int
    strengths: list[str]
    gaps: list[str]
    summary: str
    vocalpoints: list[str]


def score_resume(job_description: str, resume_text: str):
    prompt = f"""
    You are an expert technical recruiter.

    Evaluate the resume against the job description.

    Job Description:
    {job_description}

    Resume:
    {resume_text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": ScreeningResult,
        },
    )

    return response.parsed.model_dump()