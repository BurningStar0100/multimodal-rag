from fastapi import APIRouter

from rag import generate_response


query_router = APIRouter()

@query_router.post("/{user_query}")
def handle_query(user_query: str):
    """Handle user queries."""
    return generate_response(user_query)