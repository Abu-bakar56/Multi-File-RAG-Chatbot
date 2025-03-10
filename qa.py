# from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
# import os
# import warnings
# import gradio as gr
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import Chroma
# from langchain.chains import RetrievalQA
# from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader

# # Suppress warnings
# warnings.filterwarnings('ignore')

# # Load API key from environment variable
# API_KEY = os.getenv("GOOGLE_API_KEY")
# if not API_KEY:
#     raise ValueError("GOOGLE_API_KEY environment variable is not set. Please set it and try again.")

# # LLM Configuration
# generation_config = {
#     "temperature": 0.5,
#     "max_output_tokens": 256,
# }
# # Initialize the LLM
# model = GoogleGenerativeAI(model="gemini-1.5-flash", generation_config=generation_config, google_api_key=API_KEY)

# # Embedding Model
# def google_gemini_embedding():
#     return GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# # Document Loader
# def document_loader(file):
#     file_extension = file.name.split(".")[-1].lower()
#     if file_extension == "pdf":
#         loader = PyPDFLoader(file.name)
#     elif file_extension in ["doc", "docx"]:
#         loader = Docx2txtLoader(file.name)
#     elif file_extension == "txt":
#         loader = TextLoader(file.name)
#     else:
#         raise ValueError("Unsupported file format. Please upload PDF, DOCX, or TXT files.")
#     return loader.load()

# # Text Splitter
# def text_splitter(data):
#     splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
#     return splitter.split_documents(data)

# # # Vector Database
# # def vector_database(chunks):
# #     embedding_model = google_gemini_embedding()
# #     return Chroma.from_documents(chunks, embedding_model)

# import chromadb
# from chromadb.config import Settings

# def vector_database(chunks):
#     embedding_model = google_gemini_embedding()
    
#     # Use a PostgreSQL database for ChromaDB on Render
#     CHROMA_DB_URL = "postgresql://postgresql_in2c_user:dcMBPqbS0y7WRMrLos25SfeZ9yNv9Yqw@dpg-cv6t4iaj1k6c73e7o3o0-a/postgresql_in2c"
    

#     client = chromadb.PersistentClient(
#         path=CHROMA_DB_URL, 
#         settings=Settings(anonymized_telemetry=False)  # Disable telemetry for privacy
#     )

#     return client.get_or_create_collection("my_collection")


# # Retriever
# def retriever(file):
#     try:
#         splits = document_loader(file)
#         chunks = text_splitter(splits)
#         vectordb = vector_database(chunks)
#         return vectordb.as_retriever()
#     except Exception as e:
#         return str(e)

# # Retrieval QA Function
# def retriever_qa(file, query):
#     retriever_obj = retriever(file)
#     if isinstance(retriever_obj, str):
#         return retriever_obj  # Return error message if any
#     qa = RetrievalQA.from_chain_type(llm=model, chain_type="stuff", retriever=retriever_obj, return_source_documents=False)
#     response = qa.invoke(query)
#     return response.get('result', "No result found.")

# # Gradio Interface
# rag_application = gr.Interface(
#     fn=retriever_qa,
#     allow_flagging="never",
#     inputs=[
#         gr.File(label="Upload Document", file_count="single", file_types=[".pdf", ".docx", ".txt"], type="filepath"),
#         gr.Textbox(label="Input Query", lines=2, placeholder="Type your question here...")
#     ],
#     outputs=gr.Textbox(label="Output"),
#     title="RAG Chatbot",
#     description="Upload a document (PDF, DOCX, TXT) and ask any question. The chatbot will answer using the document's content.",
#     article="© 2025 by AbuBakar Shahzad | All Rights Reserved"
# )


# port = int(os.getenv("PORT", "7862"))

# # Launch the Gradio app
# rag_application.launch(server_name="0.0.0.0", server_port=port, share=False)
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
import os
import warnings
import gradio as gr
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
import chromadb
from chromadb.config import Settings

# Suppress warnings
warnings.filterwarnings('ignore')

# Load API key from environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set. Please set it and try again.")

# LLM Configuration
generation_config = {
    "temperature": 0.5,
    "max_output_tokens": 256,
}

# Initialize the LLM
model = GoogleGenerativeAI(model="gemini-1.5-flash", generation_config=generation_config, google_api_key=API_KEY)

# Embedding Model
def google_gemini_embedding():
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Document Loader
def document_loader(file_path):
    file_extension = file_path.split(".")[-1].lower()
    
    if file_extension == "pdf":
        loader = PyPDFLoader(file_path)
    elif file_extension in ["doc", "docx"]:
        loader = Docx2txtLoader(file_path)
    elif file_extension == "txt":
        loader = TextLoader(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload PDF, DOCX, or TXT files.")
    
    return loader.load()

# Text Splitter
def text_splitter(data):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    return splitter.split_documents(data)

# Vector Database with ChromaDB
def vector_database(chunks):
    embedding_model = google_gemini_embedding()
    
    # Initialize ChromaDB with embeddings
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="./chroma_db"  # Local storage for ChromaDB
    )
    
    return vectordb

# Retriever
def retriever(file_path):
    try:
        splits = document_loader(file_path)
        chunks = text_splitter(splits)
        vectordb = vector_database(chunks)
        return vectordb.as_retriever()
    except Exception as e:
        return str(e)

# Retrieval QA Function
def retriever_qa(file, query):
    try:
        retriever_obj = retriever(file.name)
        if isinstance(retriever_obj, str):  # Error handling
            return retriever_obj  
        
        qa = RetrievalQA.from_chain_type(llm=model, chain_type="stuff", retriever=retriever_obj, return_source_documents=False)
        response = qa.invoke(query)
        
        return response.get("result", "No result found.")
    
    except Exception as e:
        return str(e)

# Gradio Interface
rag_application = gr.Interface(
    fn=retriever_qa,
    allow_flagging="never",
    inputs=[
        gr.File(label="Upload Document", file_count="single", file_types=[".pdf", ".docx", ".txt"], type="filepath"),
        gr.Textbox(label="Input Query", lines=2, placeholder="Type your question here...")
    ],
    outputs=gr.Textbox(label="Output"),
    title="RAG Chatbot",
    description="Upload a document (PDF, DOCX, TXT) and ask any question. The chatbot will answer using the document's content.",
    article="CopyRight © 2025 by AbuBakar Shahzad | All Rights Reserved"
)

port = int(os.getenv("PORT", "7862"))

# Launch the Gradio app
rag_application.launch(server_name="0.0.0.0", server_port=port, share=False)
