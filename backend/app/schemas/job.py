from pydantic import BaseModel


class JobCreate(BaseModel):
    title: str
    description: str


class JobResponse(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        from_attributes = True