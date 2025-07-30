from types import ClassMethodDescriptorType
from sqlalchemy.orm import Session
from core.config import settings

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.prompts import STORY_PROMPT
from models.story import Story, StoryNode
from core.models import StoryLLMResponse, StoryNodeLLM
import os


class StoryGenerator: #not specific to the instance
    
    @classmethod
    def _get_llm(cls): #private method internal use only
        # sample Python code snippet
        openai_api_key = os.getenv("CHOREO_OPENAI_CONNECTION_OPENAI_API_KEY")
        serviceurl = os.getenv("CHOREO_OPENAI_CONNECTION_SERVICEURL")

        if openai_api_key and serviceurl:
            return ChatOpenAI(
                model= "gpt-4o-mini",
                api_key=openai_api_key,
                base_url=serviceurl,
            )
        return ChatOpenAI(
            model= "gpt-4o-mini"
        )
        
    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy") -> Story:
        llm = cls._get_llm()
        story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)
        
        prompt = ChatPromptTemplate.from_messages([
            (
                "system", 
                STORY_PROMPT
            ),
            (
                "human", 
                f"Create the story with this theme: {theme}"
            )
        ]).partial(format_instructions=story_parser.get_format_instructions()) #embed format instructions pass it to prompt template

        raw_response= llm.invoke(prompt.invoke({})) #invoke llm

        response_text = raw_response
        if hasattr(raw_response, "content"): #strip out the content
            response_text = raw_response.content

        story_structure = story_parser.parse(response_text)

        story_db = Story(
            title=story_structure.title,
            session_id=session_id,
            )
        db.add(story_db)
        db.flush() #update db with fileds that have default values

        root_node_data = story_structure.root_node
        if isinstance(root_node_data, dict):
            root_node = StoryNodeLLM.model_validate(root_node_data)
        
        cls._process_story_node(db, story_db.id, root_node_data, is_root=True)

        db.commit()
        return story_db

    @classmethod #json to python process
    def _process_story_node(cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool = False) -> StoryNode:
        node = StoryNode(
            story_id=story_id,
            content=node_data.content if hasattr(node_data, "content") else node_data["content"],
            is_root=is_root,
            is_ending=node_data.is_ending if hasattr(node_data, "is_ending") else node_data["is_ending"],
            is_winning_ending=node_data.is_winning_ending if hasattr(node_data, "is_winning_ending") else node_data["is_winning_ending"],
            options=[]
        )
        db.add(node)
        db.flush()
        #if not ending and has options
        if not node.is_ending and (hasattr(node_data, "options") and node_data.options):
            options_list = []
            for option_data in node_data.options:
                next_node = option_data.next_node

                if isinstance(next_node, dict):
                    next_node = StoryNodeLLM.model_validate(next_node) #validate next node
                
                child_node = cls._process_story_node(db, story_id, next_node, is_root=False)
                
                options_list.append({
                    "text": option_data.text,
                    "node_id": child_node.id
                })

            node.options = options_list
        
        db.flush()
        return node