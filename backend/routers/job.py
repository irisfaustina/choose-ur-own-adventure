import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session

from db.database import get_db, SessionLocal
from models.job import StoryJob
from schemas.job import StoryJobResponse

router = APIRouter( #backend URL/api/jobs
    prefix="/jobs",
    tags=["jobs"],
)

@router.get("/{job_id}", response_model=StoryJobResponse) #get request to get a job
def get_job_status(
    job_id: str,
    db: Session = Depends(get_db) #depends on get_db function
):
    job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first() #get job
    if not job:
        raise HTTPException(status_code=404, detail="Job not found") #raise exception if job not found
    return job