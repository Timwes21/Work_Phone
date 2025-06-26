import os
import json

from langchain_core.documents import Document
from pydantic import BaseModel, Field
from uuid import uuid4
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, MongodbLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.chains.retrieval_qa.base import RetrievalQA

load_dotenv()
from utils.llm import llm
from utils.db import collection
NUMBER = os.environ["NUMBER"]
api_key = os.environ['GOOGLE_API_KEY']
embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001', api_key=api_key)
url = os.environ["MONGO_URL"]
res = collection.find_one({"number": NUMBER})
files = res["files"]
files_content_list = [j for i in files for j in i.values()]

doc = Document(page_content=json.dumps(files_content_list))
# print(doc.page_content)


# doc = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=0,
    length_function=len
)

docs = text_splitter.split_documents([doc])

library = FAISS.from_documents(docs, embeddings)

query = "Have you worked with react?"

def ask_document(query):    
    retriever = library.as_retriever()
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    results = qa.invoke(query)
    return results['result']



