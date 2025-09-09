import re
from fastapi import APIRouter

from utils import process_document

processed_files = ["hello.txt"]

doc_router = APIRouter()

@doc_router.get("/")
def get_docs():
    """List of processed documents."""
    return {"documents": processed_files}

@doc_router.post("/upload/{file_path}")
def upload_doc(file_path: str):
    """Endpoint to enter file_path for file processing."""
    response = process_document(file_path)
    processed_files.append(file_path)
    return response