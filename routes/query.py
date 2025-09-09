from fastapi import APIRouter


query_router = APIRouter()

@query_router.post("/{user_query}")
def handle_query(user_query: str):
    """Handle user queries."""
    return {"query": user_query, "response": "This is a placeholder response."}