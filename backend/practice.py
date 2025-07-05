import requests
import certifi
from utils.db import collection
import asyncio
from langchain_core.documents import Document
from pydantic import BaseModel, Field
from dotenv import load_dotenv


class Example:
    calls = []
    def __init__(self):
        self.logs = []

    def append_log(self, thing_to_append):
        self.logs.append(thing_to_append)

    def append_calls(self, thing_to_append):
        self.calls.append(thing_to_append)

    def print_calls(self):
        print(self.calls)

example1 = Example()
example2 = Example()

example1.append_calls(1)
example2.print_calls()
