from fastapi import FastAPI
from routes.document import doc_router
from routes.query import query_router
import os
import getpass
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI

load_dotenv()

app = FastAPI() 

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)

vector_store = Chroma(
    collection_name="mutli_modal",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",
)

@app.get("/")
def read_root():
    return {"Welcome": "Multi-modal RAG"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(doc_router, prefix="/document", tags=["documents"])
app.include_router(query_router, prefix="/query", tags=["queries"])