#endpoints going to be hit by our user
import uuid 
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session

from db.database import get_db, SessionLocal
from models.story import Story, StoryNode
from models.job import StoryJob
from schemas.story import CreateStoryRequest, CompleteStoryNodeResponse, CompleteStoryResponse
from schemas.job import StoryJobResponse
from core.story_generator import StoryGenerator

router = APIRouter( #backend URL/api/stories
    prefix="/stories",
    tags=["stories"],
)

def get_session_id(session_id: Optional[str] = Cookie(None)): #get session id from cookie
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id

@router.post("/create", response_model=StoryJobResponse) #post request to create a story
def create_story( #inject values to parameters
    request: CreateStoryRequest,
    background_tasks: BackgroundTasks,
    response: Response,
    session_id: str = Depends(get_session_id), #depends on get_session_id function, call this function whenever endpoint is hit
    db: Session = Depends(get_db) #depends on get_db function
):
    response.set_cookie(key="session_id", value=session_id, httponly=True) #set cookie, to store user session

    #create job
    job_id = str(uuid.uuid4())
    job = StoryJob(
        job_id=job_id, #once we have job id we can use it to track the job staus like is it pending
        theme=request.theme, 
        session_id=session_id,
        status="pending") #create job
    db.add(job) #add job to database, staging in db 
    db.commit() #commit staging

    background_tasks.add_task(
        generate_story_task, 
        job_id=job_id, 
        theme=request.theme, 
        session_id=session_id
        ) #add background task, generate story

    return job

def generate_story_task(job_id: str, theme: str, session_id: str):
    db = SessionLocal() #make sure we have a new session so that one session can be doing another one waiting for the other to finish

    try:
        job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first() #get job

        if not job:
            return 
        
        try:
            job.status = "processing" #update job status
            db.commit()

            story = StoryGenerator.generate_story(db, session_id, theme) # todo generate story

            job.story_id = story.id #update story id
            job.status = "completed" #update job status
            job.completed_at = datetime.now() #update completed at
            db.commit()     

        except Exception as e:
            job.status = "failed" #update job status
            job.completed_at = datetime.now() #update completed at
            job.error = str(e) #update error
            db.commit()   

    finally:
        db.close() #close session

@router.get("/{story_id}/complete", response_model=CompleteStoryResponse) #get request to get a job

def get_complete_story(
    story_id: int,
    db: Session = Depends(get_db) #depends on get_db function
):
    story = db.query(Story).filter(Story.id == story_id).first() #get story
    if not story:
        raise HTTPException(status_code=404, detail="Story not found") #raise exception if story not found
    
    # todo parse story
    complete_story = build_complete_story_tree(db, story)
    return complete_story

def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
    nodes = db.query(StoryNode).filter(StoryNode.story_id == story.id).all() #get nodes

    node_dict = {}
    for node in nodes:
        node_response = CompleteStoryNodeResponse(
            id=node.id,
            content=node.content,
            is_ending=node.is_ending,
            is_winning_ending=node.is_winning_ending,
            options=node.options
        )
        node_dict[node.id] = node_response

    root_node = next((node for node in nodes if node.is_root), None) # looking  at all of the nodes and searching for root node, which will give us a list so we can call Next
    if not root_node:
        raise HTTPException(status_code=500, detail="Story root node not found")
    
    return CompleteStoryResponse( 
        id=story.id,
        title=story.title,
        session_id=story.session_id,
        created_at=story.created_at,
        root_node=node_dict[root_node.id],
        all_nodes=node_dict
    )