from typing_extensions import TypedDict, Literal, Optional
from pydantic import Field, BaseModel

class State(TypedDict):
    caller_id: str
    name: str
    convo: list[dict]
    scheduling_callback: str
    passing_message: str
    
    
class Routes(BaseModel):
    action: Literal["schedule_callback", "pass_message", "nothing"]

class Callback(BaseModel):
    day_of_week: Optional[str]
    date: str = Field(examples=["01/30"])
    
class PassedMessage(BaseModel):
    message: str = Field(description="A summarized version of the message the caller wanted to leave")
    
class CallerName(BaseModel):
    name: str = Field(description="name of the person who called", default="unknown")    
