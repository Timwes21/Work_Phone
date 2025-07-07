import os
import json

from langchain_core.documents import Document
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
# from langchain_community.document_loaders import TextLoader, MongodbLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.chains.retrieval_qa.base import RetrievalQA

load_dotenv()
from utils.llm import llm
from utils.db import collection
api_key = os.environ['GOOGLE_API_KEY']
embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001', api_key=api_key)
url = os.environ["MONGO_URL"]

def get_file_path(number):
    return f"stores/{number}"


async def ask_document(number):
    filepath = get_file_path(number)
    if os.path.exists(filepath):
        library = FAISS.load_local(filepath, embeddings=embeddings, allow_dangerous_deserialization=True)
        retriever = library.as_retriever()
        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
        return qa
        
    return None


def save_docs(files_content_list, number):
    filepath = get_file_path(number)
    doc = Document(page_content=json.dumps(files_content_list))
    if len(doc.page_content) == 0:
        return

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=0,
        length_function=len
    )

    docs = text_splitter.split_documents([doc])

    library = FAISS.from_documents(docs, embeddings)

    # add, 
    # add first
    # delete last
    # delete 
    
    
    if os.path.exists(filepath):
        existing = FAISS.load_local(filepath, embeddings, allow_dangerous_deserialization=True)
        existing.merge_from(library)
        existing.save_local(filepath)
        return

    library.save_local(filepath)



    