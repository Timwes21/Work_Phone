from langgraph.graph import StateGraph, START, END
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from typing_extensions import TypedDict, Literal, Optional
from pydantic import Field, BaseModel
from utils.llm import llm
from utils.query import ask_document



class State(TypedDict):
    user_input: str
    action: str
    results: str
    
    
class Routes(BaseModel):
    action: Literal["get_query_result", "nothing"]
    
def anazlyze_input(state: State):
    user_input = state["user_input"]
    parser = PydanticOutputParser(pydantic_object=Routes)
    prompt = ChatPromptTemplate.from_template("Based on this convo, decide whether a the caller wanted to get information (get_query_result), or do nothing: {convo} {format}").partial(format=parser.get_format_instructions())
    chain = prompt | llm | parser
    result = chain.invoke({"convo": user_input})
    print(result)
    return {"action": result.action}

def get_action(state: State):
    return state["action"]

def get_query_result(state: State):
    results = ask_document(state['user_input'])
    return {"results": results}

builder = (
    StateGraph(State)
    .add_node("analyze_input", anazlyze_input)
    .add_node("get_query_result", get_query_result)
    .add_edge(START, "analyze_input")
    .add_conditional_edges("analyze_input", get_action, {"get_query_result": "get_query_result", "nothing": END})
    .add_edge("get_query_result", END)
    
)
query_graph = builder.compile()