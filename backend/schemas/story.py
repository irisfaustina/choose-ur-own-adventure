# API schemas
# #python classes we expect API to receive, fastapi can do some validation for us

from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel

class StoryOptionsSchema(BaseModel): #describing the options available at each node in the story
    text: str
    node_id: Optional[int] = None

#story node schema
class StoryNodeBase(BaseModel): #base = parent class so it's easier to inherit from not directly used in api; describing individual events, scenes, or branching points within the story
    content: str
    is_ending: bool = False
    is_winning_ending: bool = False


class CompleteStoryNodeResponse(StoryNodeBase): #naming convention for response = response from api returned from the front end; request is from the front end to the backend, includes everything in storynodebase
    id: int
    options: List[StoryOptionsSchema] = []

    class Config:
        from_attributes = True


class StoryBase(BaseModel): #Defines the core fields for an entire story
    title: str
    session_id: Optional[str] = None
    
    class Config:
        from_attributes = True


class CreateStoryRequest(BaseModel): #pass some theme to request create story from api sent to the backend
    theme: str


class CompleteStoryResponse(StoryBase): #response from api returned from the backend
    id: int
    created_at: datetime
    root_node: CompleteStoryNodeResponse
    all_nodes: Dict[int, CompleteStoryNodeResponse] 
    
    class Config:
        from_attributes = True