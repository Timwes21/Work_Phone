from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage
import sys
import os
from utils.models import State, Callback
from Nodes.action_graph_nodes import (
    get_caller_info,
    call_action_action_router,
    scheduler,
    pass_message,
    nothing,
    add_to_db,
)
    

    
builder = (
    StateGraph(State)
    .add_node("get_caller_info", get_caller_info)
    .add_node("call_action_action_router", call_action_action_router)
    .add_node("scheduler", scheduler)
    .add_node("pass_message", pass_message)
    .add_node("add_to_db", add_to_db)
    .add_node("nothing", nothing)
    .add_edge(START, "get_caller_info")
    .add_conditional_edges("get_caller_info", call_action_action_router, {"schedule_callback": "scheduler", "pass_message":"pass_message", "": "nothing"})
    .add_edge("pass_message", "add_to_db")
    .add_edge("scheduler", "add_to_db")
    .add_edge("add_to_db", END)
    .add_edge("nothing", END)
)



action_graph = builder.compile()

