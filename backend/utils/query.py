import os
from langchain_core.documents import Document
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
# from langchain_community.document_loaders import TextLoader, MongodbLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.chains.retrieval_qa.base import RetrievalQA

load_dotenv()
from utils.llm import llm
api_key = os.environ['GOOGLE_API_KEY']
embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001', api_key=api_key)
url = os.environ["MONGO_URL"]

mount_path = os.environ["MNT_PATH"]
def get_file_path(number):
    return f"{mount_path}/{number}"


class OrganizedDoc(BaseModel):
    metadata: str
    content: str

class Docs(BaseModel):
    docs: list[OrganizedDoc]





async def ask_document(number, files):
    filepath = get_file_path(number)
    if len(files) > 0:
        print("vector store exists")
        library = FAISS.load_local(filepath, embeddings=embeddings, allow_dangerous_deserialization=True)
        retriever = library.as_retriever()
        return retriever
        
    return None


async def save_docs_with_faiss(files_content, number, portfolio=False):
    filepath = get_file_path(number)
    if len(files_content) == 0:
        return
    docs = organize_docs(files_content)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
        length_function=len
    )

    docs = text_splitter.split_documents(docs)

    library = FAISS.from_documents(docs, embeddings)

    
    
    if not portfolio and len(files_content) > 1:
        existing = FAISS.load_local(filepath, embeddings, allow_dangerous_deserialization=True)
        existing.merge_from(library)
        existing.save_local(filepath)
        return

    library.save_local(filepath)


def organize_docs(files_content):
    parser = PydanticOutputParser(pydantic_object=Docs)
    instructions = parser.get_format_instructions()
    prompt_template = ChatPromptTemplate.from_template("Condense this document into organized sections that make it easy to find things in a vector store, make sure each metadata is unique: {files_content} {format}")
    prompt = prompt_template.partial(format=instructions)
    chain = prompt | llm | parser
    res: Docs = chain.invoke({"files_content": files_content})
    print(res)
    docs = []
    for item in res.docs:
        print(item)
        docs.append(Document(page_content=item.content, metadata={"category": item.metadata}))
    return docs


    


    