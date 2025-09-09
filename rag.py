"""Implement RAG pipeline:- takes user query, fetch relevant document, use llm to generate response and return it to user with citiations"""

from main import llm, vector_store, embeddings
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain import hub

def generate_response(user_query:str):
    #getting relevant docs form vector store
    results = vector_store.similarity_search_by_vector(
    embedding=embeddings.embed_query(user_query), k=3
    )
    for doc in results:
        print(f"* {doc.page_content} [{doc.metadata}]")
    # Define prompt for question-answering
    prompt = hub.pull("rlm/rag-prompt")
    docs_content = "\n\n".join(doc.page_content for doc in results)
    messages = prompt.invoke({"question": user_query, "context": docs_content})
    response = llm.invoke(messages)
    print(f"Response: {response.content}")
    return {"answer": response.content + "\n\n" + "SOURCES:\n" + "\n".join(set(doc.metadata["source"] for doc in results))}
    
    