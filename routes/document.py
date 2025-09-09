import re
from fastapi import APIRouter


doc_router = APIRouter()

@doc_router.get("/")
def get_docs():
    """List of processed documents."""
    return {"documents": "List of processed documents will be here."}

@doc_router.post("/upload/{doc_name}")
def upload_doc(doc_name: str):
    """Endpoint to upload a new document."""
    return {"message": f"Document {doc_name} uploaded successfully."}