from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class StoryOptionLLM(BaseModel):
    text: str = Field(description="The text of the option whon to the user")
    next_node: Dict[str, Any] = Field(description="The next node content in its options")


class StoryNodeLLM(BaseModel):
    content: str = Field(description="The main content of the node")
    is_ending: bool = Field(description="Whether the node is an ending node")
    is_winning_ending: bool = Field(description="Whether the node is a winning ending")
    options: List[StoryOptionLLM] = Field(default=None, description="The options for the node")


class StoryLLMResponse(BaseModel):
    title: str = Field(description="The title of the story")
    root_node: StoryNodeLLM = Field(description="The root node of the story")
