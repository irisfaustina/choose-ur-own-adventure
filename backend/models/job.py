from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from db.database import Base 

#job = intent to create a story
class StoryJob(Base): #frontend -> job, backend ->job, front end asks if job is done, backend -> report status, if job is completed, failed, pending
    __tablename__ = "story_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, index=True, unique=True) #longer value that's a string
    session_id = Column (String, index=True)
    theme = Column(String) 
    status = Column(String)
    story_id = Column(Integer, nullable=True) #can have no value, generted by this job
    error = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True) #how long it takes to generate story
    