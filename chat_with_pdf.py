"""
RAG-powered Document Chat Application

This application implements a Retrieval Augmented Generation (RAG) system that allows users
to upload documents (.txt and .pdf formats) and interact with their content through a 
conversational interface powered by LangChain, ChromaDB, and OpenAI.

Author: Xiwen Zhang
Date: October 2025
"""

import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
import tempfile
import shutil
from typing import List, Dict, Optional
from pathlib import Path

# LangChain imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.schema import Document

# Load environment variables
load_dotenv()

# Configuration constants
CHUNK_SIZE = 1000  # Number of characters per chunk
CHUNK_OVERLAP = 200  # Overlap between chunks to maintain context
EMBEDDING_MODEL = "openai.text-embedding-ada.002"
LLM_MODEL = "openai.gpt-4o"
TEMPERATURE = 0.7
MAX_TOKENS_LIMIT = 8000
RETRIEVAL_K = 4  # Number of relevant chunks to retrieve

# Cornell API configuration
API_BASE_URL = "https://api.ai.it.cornell.edu"

# Initialize OpenAI client
def get_openai_client():
    """Initialize and return OpenAI client with Cornell API configuration."""
    api_key = os.getenv("API_KEY")
    if not api_key:
        st.error("❌ API Key not found! Please set API_KEY in your .env file.")
        st.stop()
    return OpenAI(api_key=api_key, base_url=API_BASE_URL)


def initialize_session_state():
    """
    Initialize Streamlit session state variables for managing application state
    across user interactions.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
    
    if "conversation_chain" not in st.session_state:
        st.session_state.conversation_chain = None
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []
    
    if "processing" not in st.session_state:
        st.session_state.processing = False
    
    if "temp_dir" not in st.session_state:
        # Create a temporary directory for ChromaDB persistence
        st.session_state.temp_dir = tempfile.mkdtemp()


def load_document(file_path: str, file_type: str) -> List[Document]:
    """
    Load a document using appropriate loader based on file type.
    
    Args:
        file_path: Path to the document file
        file_type: Type of file ('txt' or 'pdf')
    
    Returns:
        List of LangChain Document objects
    
    Raises:
        Exception: If document loading fails
    """
    try:
        if file_type == "txt":
            loader = TextLoader(file_path, encoding='utf-8')
        elif file_type == "pdf":
            loader = PyPDFLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        documents = loader.load()
        return documents
    except Exception as e:
        st.error(f"Error loading {file_type.upper()} file: {str(e)}")
        return []


def chunk_documents(documents: List[Document]) -> List[Document]:
    """
    Split documents into smaller chunks using RecursiveCharacterTextSplitter.
    
    Chunking Strategy:
    - Chunk Size: 1000 characters
      * Large enough to maintain context and semantic meaning
      * Small enough for efficient retrieval and processing
      * Balances between retrieval precision and context preservation
    
    - Chunk Overlap: 200 characters
      * Prevents information loss at chunk boundaries
      * Ensures continuity when concepts span multiple chunks
      * Helps maintain coherence in retrieved context
    
    - Splitting Strategy: Recursive splitting by paragraph, sentence, then character
      * Preserves natural document structure
      * Maintains semantic units where possible
      * Falls back to character splitting when necessary
    
    Args:
        documents: List of Document objects to be chunked
    
    Returns:
        List of chunked Document objects
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]  # Prioritize natural breaks
    )
    
    chunks = text_splitter.split_documents(documents)
    return chunks


def create_vectorstore(chunks: List[Document]) -> Chroma:
    """
    Create a ChromaDB vector store from document chunks.
    
    Uses OpenAI's text-embedding-ada-002 model for generating embeddings.
    This model provides:
    - 1536-dimensional embeddings
    - Strong semantic understanding
    - Good balance between quality and cost
    
    Args:
        chunks: List of document chunks to embed
    
    Returns:
        Chroma vector store instance
    """
    try:
        embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            openai_api_key=os.getenv("API_KEY"),
            openai_api_base=API_BASE_URL
        )
        
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=st.session_state.temp_dir
        )
        
        return vectorstore
    except Exception as e:
        st.error(f"Error creating vector store: {str(e)}")
        return None


def create_conversation_chain(vectorstore: Chroma) -> ConversationalRetrievalChain:
    """
    Create a conversational retrieval chain that combines retrieval and generation.
    
    The chain:
    1. Retrieves relevant document chunks based on the query
    2. Uses conversation history for context-aware responses
    3. Generates grounded responses using retrieved information
    
    Args:
        vectorstore: ChromaDB vector store for retrieval
    
    Returns:
        ConversationalRetrievalChain instance
    """
    try:
        llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=TEMPERATURE,
            openai_api_key=os.getenv("API_KEY"),
            openai_api_base=API_BASE_URL
        )
        
        # Create memory to maintain conversation context
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            output_key="answer",
            return_messages=True
        )
        
        # Create the conversational retrieval chain
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": RETRIEVAL_K}
            ),
            memory=memory,
            return_source_documents=True,
            verbose=False
        )
        
        return conversation_chain
    except Exception as e:
        st.error(f"Error creating conversation chain: {str(e)}")
        return None


def process_uploaded_files(uploaded_files) -> bool:
    """
    Process uploaded files: load, chunk, and create vector store.
    
    Args:
        uploaded_files: List of uploaded file objects from Streamlit
    
    Returns:
        Boolean indicating success or failure
    """
    if not uploaded_files:
        return False
    
    st.session_state.processing = True
    all_chunks = []
    
    with st.spinner("📄 Processing documents..."):
        for uploaded_file in uploaded_files:
            # Determine file type
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            # Save uploaded file temporarily
            temp_file_path = os.path.join(st.session_state.temp_dir, uploaded_file.name)
            with open(temp_file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            # Load document
            st.write(f"📖 Loading: {uploaded_file.name}")
            documents = load_document(temp_file_path, file_extension)
            
            if documents:
                # Add source metadata
                for doc in documents:
                    doc.metadata['source'] = uploaded_file.name
                
                # Chunk documents
                chunks = chunk_documents(documents)
                all_chunks.extend(chunks)
                st.write(f"✅ Processed {len(chunks)} chunks from {uploaded_file.name}")
    
    if all_chunks:
        with st.spinner("🧠 Creating vector database..."):
            vectorstore = create_vectorstore(all_chunks)
            
            if vectorstore:
                st.session_state.vectorstore = vectorstore
                st.session_state.conversation_chain = create_conversation_chain(vectorstore)
                st.session_state.uploaded_files = [f.name for f in uploaded_files]
                st.success(f"✅ Successfully processed {len(uploaded_files)} document(s) with {len(all_chunks)} total chunks!")
                st.session_state.processing = False
                return True
    
    st.session_state.processing = False
    return False


def display_chat_interface():
    """
    Display the chat interface with message history and input field.
    """
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Display source documents if available
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📚 View Sources"):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(f"**Source {i}:** {source['source']}")
                        st.markdown(f"```\n{source['content'][:300]}...\n```")


def handle_user_input(user_question: str):
    """
    Handle user input and generate response using the RAG pipeline.
    
    Args:
        user_question: User's question/query
    """
    if not st.session_state.conversation_chain:
        st.error("❌ Please upload documents first!")
        return
    
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_question})
    
    with st.chat_message("user"):
        st.markdown(user_question)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                # Query the conversational chain
                response = st.session_state.conversation_chain({
                    "question": user_question
                })
                
                answer = response['answer']
                source_documents = response.get('source_documents', [])
                
                # Display answer
                st.markdown(answer)
                
                # Prepare source information
                sources = []
                if source_documents:
                    for doc in source_documents:
                        sources.append({
                            'source': doc.metadata.get('source', 'Unknown'),
                            'content': doc.page_content
                        })
                    
                    # Display sources
                    with st.expander("📚 View Sources"):
                        for i, source in enumerate(sources, 1):
                            st.markdown(f"**Source {i}:** {source['source']}")
                            st.markdown(f"```\n{source['content'][:300]}...\n```")
                
                # Add assistant message to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })
                
            except Exception as e:
                st.error(f"❌ Error generating response: {str(e)}")


def main():
    """
    Main application function that orchestrates the Streamlit UI and RAG functionality.
    """
    # Page configuration
    st.set_page_config(
        page_title="RAG Document Chat",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Application header
    st.title("📚 RAG-Powered Document Chat")
    st.markdown("""
    Upload your documents (PDF or TXT) and chat with them using AI! 
    This application uses **Retrieval Augmented Generation (RAG)** to provide accurate, 
    context-aware answers based on your documents.
    """)
    
    # Sidebar for file upload and settings
    with st.sidebar:
        st.header("📁 Document Upload")
        
        uploaded_files = st.file_uploader(
            "Upload Documents",
            type=["txt", "pdf"],
            accept_multiple_files=True,
            help="Upload one or more .txt or .pdf files"
        )
        
        if uploaded_files:
            if st.button("🚀 Process Documents", type="primary", disabled=st.session_state.processing):
                process_uploaded_files(uploaded_files)
        
        # Display uploaded files
        if st.session_state.uploaded_files:
            st.success("📄 **Loaded Documents:**")
            for filename in st.session_state.uploaded_files:
                st.write(f"- {filename}")
        
        # Settings
        st.divider()
        st.header("⚙️ Settings")
        
        st.markdown(f"""
        **Configuration:**
        - **Chunk Size:** {CHUNK_SIZE} characters
        - **Chunk Overlap:** {CHUNK_OVERLAP} characters
        - **Retrieval K:** {RETRIEVAL_K} chunks
        - **LLM Model:** {LLM_MODEL}
        - **Temperature:** {TEMPERATURE}
        """)
        
        if st.button("🔄 Clear All & Reset"):
            # Clear session state
            st.session_state.messages = []
            st.session_state.vectorstore = None
            st.session_state.conversation_chain = None
            st.session_state.chat_history = []
            st.session_state.uploaded_files = []
            
            # Clean up temporary directory
            if os.path.exists(st.session_state.temp_dir):
                shutil.rmtree(st.session_state.temp_dir)
                st.session_state.temp_dir = tempfile.mkdtemp()
            
            st.rerun()
    
    # Main chat interface
    st.divider()
    
    if not st.session_state.uploaded_files:
        st.info("👈 Please upload documents using the sidebar to get started!")
    else:
        # Display chat interface
        display_chat_interface()
        
        # Chat input
        if user_input := st.chat_input("Ask a question about your documents..."):
            handle_user_input(user_input)


if __name__ == "__main__":
    main()
