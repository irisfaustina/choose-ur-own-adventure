from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base #inherit from this class to create models

#metadata of the story
class Story(Base):
    __tablename__ = "stories" #table name we store in sql, class = table with orm
    
    id = Column(Integer, primary_key=True, index=True) #unique identifier, index true so we can look up stories with id
    title = Column(String, index=True) #title of story, index true so we can look up stories with title
    session_id = Column(String, index=True) #foreign key to session
    created_at = Column(DateTime(timezone=True), default=func.now()) #when story was created

    nodes = relationship("StoryNode", back_populates="story") #bilateral with story node relationship, not an actual column in the database! It’s a convenience for object-oriented code to get nodes related to the story.

#content, options and paths for each story
class StoryNode(Base): 
    __tablename__ = "story_nodes"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id"), index=True) #foreign key to ensure each node has a reference back to the story it belongs to
    content = Column(String, index=True)
    is_root = Column(Boolean, default=False) #is this the staring node
    is_ending = Column(Boolean, default=False) #is this the ending node
    is_winning_ending = Column(Boolean, default=False) #is this the winning ending
    options = Column (JSON, default=list)

    story = relationship("Story", back_populates="nodes") #bilateral with story


    

