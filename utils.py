#processing of docx documents using langchain and storing them in Chroma
from uuid import uuid4
from langchain.document_loaders import UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from dotenv import load_dotenv
import os
from main import vector_store, llm
import base64
from langchain_core.messages import HumanMessage
from langchain_core.documents import Document

load_dotenv()

#creating a router function to identify the document type and call the respective processing function
def process_document(file_path):
    if file_path.endswith(".docx"):
        return process_docx(file_path)
    elif file_path.endswith(".pdf"):
        return process_pdf(file_path)
    elif file_path.endswith(".txt"):
        return process_txt(file_path)
    elif file_path.endswith((".png", ".jpg", ".jpeg")):
        return process_image(file_path)
    else:
        return {"error": "Unsupported file type."}

#function to process docx files
def process_docx(file_path):
    # Load the document
    loader = UnstructuredWordDocumentLoader(file_path)
    documents = loader.load()

    # Split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    print(f"No of chunks created: {len(docs)}")
    print(docs[0].page_content)
    #addition of metadata to each chunk
    for i, doc in enumerate(docs):
        doc.metadata["source"] = f"{os.path.basename(file_path)}_chunk_{i}"
    
    uuids = [str(uuid4()) for _ in range(len(docs))]

    vector_store.add_documents(documents=docs, ids=uuids)

    return {"message": f"Docx file {file_path} uploaded successfully."}

#function to process pdf files
def process_pdf(file_path):
    """Extract text and image from PDF along with metadata i.e. page number and then
    pass image to get description of image using openAI's model and then store the chunck of text and image description in chroma"""
    return {"message": f"PDF file {file_path} uploaded successfully (actually nhi upload hui h)."}

def process_txt(file_path):
    """Process text files."""
    loader = TextLoader(file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150) # Increased overlap for better context
    docs = text_splitter.split_documents(documents)
    print(f"Document split into {len(docs)} chunks.")
    for i, doc in enumerate(docs):
        doc.metadata["source"] = f"{os.path.basename(file_path)}_chunk_{i}"
    
    uuids = [str(uuid4()) for _ in range(len(docs))]

    vector_store.add_documents(documents=docs, ids=uuids)
    return {"message": f"Text file {file_path} uploaded successfully."}
    

def process_image(image_file_path):
    """Process image files by converting them to base64 and generating description using OpenAI and then storing the description in Chroma with metadata."""
    # Example using a local image file encoded in base64
    with open(image_file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        message = HumanMessage(
            content=[
                {"type": "text", "text": "Describe the given image."},
                {"type": "image_url", "image_url": f"data:image/png;base64,{encoded_image}"},
            ]
        )
        result = llm.invoke([message])
        print(f"Response for local image: {result.content}")
        # Storing the image description in Chroma
        
        doc = Document(
            page_content = result.content,
            metadata={"source": os.path.basename(image_file_path)}
        )
        vector_store.add_documents(documents=[doc], ids=[str(uuid4())])
    return {"message": f"Image file {image_file_path} processed successfully."}
        