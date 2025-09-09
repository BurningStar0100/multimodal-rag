from fastapi import FastAPI
from routes.document import doc_router
from routes.query import query_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"Welcome": "Multi-modal RAG"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(doc_router, prefix="/document", tags=["documents"])
app.include_router(query_router, prefix="/query", tags=["queries"])