# Reference Log

This document tracks all external sources, libraries, documentation, tutorials, and tools used in the development of this RAG-powered Document Chat Application.

## Official Documentation

### LangChain
- **Source**: [LangChain Python Documentation](https://python.langchain.com/docs/get_started/introduction)
- **Usage**: Primary framework for building the RAG pipeline
- **Specific Modules Used**:
  - `langchain.text_splitter.RecursiveCharacterTextSplitter` - Document chunking
  - `langchain_openai.OpenAIEmbeddings` - Text embedding generation
  - `langchain_openai.ChatOpenAI` - LLM interface
  - `langchain.chains.ConversationalRetrievalChain` - RAG chain orchestration
  - `langchain.memory.ConversationBufferMemory` - Conversation history management
- **Documentation References**:
  - [Text Splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/)
  - [Conversational Retrieval Chain](https://python.langchain.com/docs/use_cases/question_answering/chat_history)
  - [Vector Stores](https://python.langchain.com/docs/modules/data_connection/vectorstores/)

### LangChain Community
- **Source**: [LangChain Community Documentation](https://python.langchain.com/docs/integrations/platforms/)
- **Usage**: Document loaders and vector store integrations
- **Specific Modules Used**:
  - `langchain_community.document_loaders.TextLoader` - Loading .txt files
  - `langchain_community.document_loaders.PyPDFLoader` - Loading .pdf files
  - `langchain_community.vectorstores.Chroma` - ChromaDB integration

### ChromaDB
- **Source**: [ChromaDB Documentation](https://docs.trychroma.com/)
- **Usage**: Vector database for storing and retrieving document embeddings
- **Key Features Used**:
  - Document embedding storage
  - Similarity search
  - Persistent storage
- **Documentation References**:
  - [Getting Started](https://docs.trychroma.com/getting-started)
  - [Usage Guide](https://docs.trychroma.com/usage-guide)

### Streamlit
- **Source**: [Streamlit Documentation](https://docs.streamlit.io/)
- **Usage**: Web application framework for building the user interface
- **Components Used**:
  - `st.file_uploader()` - File upload widget
  - `st.chat_message()` - Chat interface components
  - `st.chat_input()` - User input field
  - `st.session_state` - State management across reruns
  - `st.sidebar` - Sidebar layout
  - `st.spinner()` - Loading indicators
- **Documentation References**:
  - [Chat Elements](https://docs.streamlit.io/library/api-reference/chat)
  - [File Uploader](https://docs.streamlit.io/library/api-reference/widgets/st.file_uploader)
  - [Session State](https://docs.streamlit.io/library/api-reference/session-state)

### OpenAI
- **Source**: [OpenAI API Documentation](https://platform.openai.com/docs/introduction)
- **Usage**: LLM and embedding models via Cornell API endpoint
- **Models Used**:
  - `gpt-4o` - Chat completion model for response generation
  - `text-embedding-ada-002` - Text embedding model (1536 dimensions)
- **Documentation References**:
  - [Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
  - [Chat Completions](https://platform.openai.com/docs/guides/chat)

### PyPDF
- **Source**: [PyPDF Documentation](https://pypdf.readthedocs.io/)
- **Usage**: PDF text extraction for document processing
- **Features Used**:
  - Text extraction from PDF pages
  - Page-by-page processing

### Python-dotenv
- **Source**: [Python-dotenv Documentation](https://github.com/theskumar/python-dotenv)
- **Usage**: Loading environment variables from .env file
- **Purpose**: Secure API key management without hardcoding

## 📖 Learning Resources & Tutorials

### RAG Fundamentals
- **Paper**: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
  - **Authors**: Patrick Lewis et al. (2020)
  - **Link**: [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)
  - **Usage**: Understanding RAG architecture and principles
  - **Key Concepts Applied**:
    - Combining retrieval and generation
    - Context-grounded response generation
    - Document chunking strategies

### LangChain Tutorials
- **Source**: [LangChain YouTube Channel](https://www.youtube.com/@LangChain)
- **Usage**: Understanding LangChain architecture and best practices
- **Topics Covered**:
  - Building RAG applications
  - Document loaders and text splitters
  - Vector stores and embeddings
  - Conversational chains

### Chunking Strategies
- **Article**: "Chunking Strategies for LLM Applications"
- **Source**: Pinecone Learning Center
- **Link**: [https://www.pinecone.io/learn/chunking-strategies/](https://www.pinecone.io/learn/chunking-strategies/)
- **Usage**: Determining optimal chunk size and overlap
- **Key Insights Applied**:
  - Chunk size of 1000 characters for balanced context
  - 20% overlap (200 characters) to prevent information loss
  - Recursive splitting to preserve document structure

## 🔧 Development Tools & Libraries

### Core Python Libraries
- **Python 3.9**: Base programming language
- **typing**: Type hints for better code quality
- **tempfile**: Temporary file and directory management
- **pathlib**: Object-oriented filesystem paths
- **os**: Operating system interface
- **shutil**: High-level file operations

### Additional Dependencies
- **pydantic**: Data validation and settings management (used by LangChain)
- **requests**: HTTP library (used by various integrations)
- **tiktoken**: OpenAI's tokenizer for token counting
- **sentence-transformers**: Additional embedding model support

## GenAI Usage

### Copilot AI Assistant
- **Usage**: Code assistance and problem-solving throughout development
- **Specific Uses**:
  1. **Documentation Writing**: Assisted in writing comprehensive docstrings
     - Rationale: Ensure clear documentation of complex functions
  2. **Best Practices**: Advised on LangChain best practices
     - Rationale: Ensure proper usage of framework features
  3. **README Creation**: Helped structure comprehensive documentation
     - Rationale: Create professional, complete documentation

### ChatGPT
- **Usage**: Conceptual understanding and problem-solving
- **Specific Uses**:
  1. **RAG Architecture**: Explained RAG pipeline components and flow
     - Rationale: Deep understanding of system design
  2. **Chunking Strategy**: Discussed optimal chunk size determination
     - Rationale: Make informed decisions about parameters

## Code Inspiration

### Class Materials
- **Source**: INFO 5940 Course Repository (assignment1 branch)
- **File**: `chat_with_pdf.py` (original template)
- **Usage**: Starting point for basic Streamlit structure
- **Modified**: Extensively enhanced with full RAG implementation

### LangChain Examples
- **Source**: [LangChain Use Cases - Question Answering](https://python.langchain.com/docs/use_cases/question_answering/)
- **Usage**: Reference for implementing conversational retrieval
- **Adapted**: Customized for multi-document support and source attribution

### Streamlit Gallery
- **Source**: [Streamlit App Gallery - Chat Examples](https://streamlit.io/gallery?category=llms-chat)
- **Usage**: UI/UX patterns for chat interfaces
- **Applied**: Chat message display and input handling

## Testing & Quality Assurance

### Manual Testing Approach
- **Documents Tested**:
  - Small .txt files (< 1KB)
  - Large .txt files (> 100KB)
  - Simple PDFs with text
  - Complex PDFs with tables and formatting
  - Multiple documents simultaneously

- **Scenarios Tested**:
  - Single document upload
  - Multiple document upload
  - Follow-up questions
  - Source attribution accuracy
  - Reset functionality
  - Error handling (invalid files, empty documents)

## Design Decisions & Rationale

### Architecture Choices

1. **LangChain over Custom Implementation**
   - **Rationale**: Industry standard, well-tested, extensive community support
   - **Alternative Considered**: Building custom RAG from scratch
   - **Decision**: Use LangChain for reliability and maintainability

2. **ChromaDB over Alternatives (Pinecone, Weaviate)**
   - **Rationale**: Lightweight, no external service required, perfect for assignment scope
   - **Alternatives Considered**: Pinecone (cloud-based), FAISS (Facebook)
   - **Decision**: ChromaDB for simplicity and local operation

3. **RecursiveCharacterTextSplitter**
   - **Rationale**: Preserves document structure better than simple splitting
   - **Alternatives Considered**: CharacterTextSplitter, TokenTextSplitter
   - **Decision**: Recursive splitting for better semantic coherence

### Parameter Choices

1. **Chunk Size: 1000 characters**
   - **Research**: Based on Pinecone article and empirical testing
   - **Rationale**: Balances context vs. precision
   - **Testing**: Tested with 500, 1000, 1500 - 1000 performed best

2. **Chunk Overlap: 200 characters**
   - **Research**: 15-25% overlap recommended in literature
   - **Rationale**: Prevents information loss at boundaries
   - **Testing**: 20% overlap (200/1000) proved optimal

3. **Retrieval K: 4 chunks**
   - **Research**: Common practice in RAG systems
   - **Rationale**: Sufficient context without overwhelming LLM
   - **Testing**: Tested 2, 4, 6 - 4 provided best balance

4. **Temperature: 0.7**
   - **Research**: OpenAI recommendations for balanced creativity
   - **Rationale**: Natural language while maintaining accuracy
   - **Testing**: 0.5 too rigid, 0.9 too creative, 0.7 optimal
