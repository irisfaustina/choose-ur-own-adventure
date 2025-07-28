from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class StoryJobBase(BaseModel): #Defines the core fields for a job
    theme: str

class StoryJobResponse(BaseModel): #Defines the core fields for a job
    job_id: str
    status: str
    created_at: datetime
    story_id: Optional[int] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None

    class Config:
        from_attributes = True

class StoryJobCreate(StoryJobBase): #Defines the core fields for a job, used for a request for ingesting data
    pass