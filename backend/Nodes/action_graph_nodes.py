from langchain.output_parsers import PydanticOutputParser
from utils.models import Callback, State, Routes, PassedMessage, CallerName
from langchain.prompts import ChatPromptTemplate
from utils.llm import llm
from telegram import send_message
from utils.db import add_call_log
import datetime
import json

def get_caller_info(state: State):
    parser = PydanticOutputParser(pydantic_object=CallerName)
    prompt = ChatPromptTemplate.from_template("Ananlyze this conversation and tell get me the callers name: {convo} {format}").partial(format=parser.get_format_instructions())
    chain = prompt | llm | parser
    result = chain.invoke({"convo": state['convo']})
    return {"name": result.name}


def call_action_action_router(state: State):
    parser = PydanticOutputParser(pydantic_object=Routes)
    prompt = ChatPromptTemplate.from_template("Based on this convo, decide whether a the caller wanted to schedule a callback, pass a message, or do nothing: {convo} {format}").partial(format=parser.get_format_instructions())
    chain = prompt | llm | parser
    result = chain.invoke({"convo": state['convo']})
    print(result)
    return result.action

def scheduler(state: State):
    parser = PydanticOutputParser(pydantic_object=Callback)
    prompt = ChatPromptTemplate.from_template("get the date, day of the week, name of the person, for reference the current date is {date}. {convo} {format}").partial(date=datetime.date.today(), format=parser.get_format_instructions())
    chain = prompt | llm | parser
    result = chain.invoke({"convo": state['convo']})
    body = f"You have a callback with {state['name']} on {result.day_of_week}, {result.date}. You can call them back at {state['caller_id']}"
    send_message(body)
    return {"scheduling_callback": result.model_dump()}
    
    
def pass_message(state: State):
    parser = PydanticOutputParser(pydantic_object=PassedMessage)
    prompt = ChatPromptTemplate.from_template("The caller wants to leave a message, be sure to summarize the message they are leaving while still outlining important points {convo} {format}").partial(format=parser.get_format_instructions())
    chain = prompt | llm | parser
    result = chain.invoke({"convo": state["convo"]})
    body = f"{state["name"]} wanted to leave a message and i summarized it for you: {result.message}"
    send_message(body)
    return {"passing_message": result.model_dump()}

def add_to_db(state: State):
    passing_message = state.get("passing_message", None)
    scheduling_callback = state.get("scheduling_callback", None)
    log = {
        "name": state["name"],
        "caller_id": state["caller_id"],
        "message": passing_message,
        "callback": scheduling_callback
    }
    add_call_log(log)
    
    
    
def nothing(state: State):
    print("there was not an action chosen")
