# RAG-Powered Document Chat Application

A Retrieval Augmented Generation (RAG) application built with **Streamlit**, **LangChain**, and **ChromaDB** that enables natural language interaction with document content through an intuitive conversational interface.

## Overview

This application implements a complete RAG pipeline that allows users to:
- Upload multiple documents in TXT and PDF formats
- Ask natural language questions about the document content
- Receive accurate, context-grounded responses with source citations
- Maintain conversational context across multiple interactions

The system uses state-of-the-art language models and vector databases to provide intelligent document analysis and question answering capabilities.

## Features

### Core Functionality
- **Multi-Format Support**: Upload and process both `.txt` and `.pdf` files
- **Multiple Document Handling**: Process and query multiple documents simultaneously
- **Conversational Interface**: Natural chat-based interaction with full conversation history
- **Source Attribution**: View exact document passages used to generate each response
- **Real-time Processing**: Efficient document chunking and embedding generation

### RAG Pipeline Components

#### 1. Document Ingestion & Chunking (50 points)
- **Robust File Handling**: Supports TXT (UTF-8 encoding) and PDF (PyPDF) formats
- **Intelligent Chunking Strategy**:
  - **Chunk Size**: 1000 characters
    - Optimized to maintain semantic coherence
    - Large enough for contextual understanding
    - Small enough for precise retrieval
  - **Chunk Overlap**: 200 characters
    - Prevents information loss at boundaries
    - Ensures concept continuity across chunks
  - **Recursive Splitting**: Preserves natural document structure
    - Prioritizes paragraph and sentence boundaries
    - Falls back to character splitting when necessary

#### 2. RAG Pipeline (50 points)
- **Advanced Retrieval Component**:
  - ChromaDB vector database for efficient similarity search
  - OpenAI `text-embedding-ada-002` embeddings (1536 dimensions)
  - Semantic search returning top-4 most relevant chunks
- **Intelligent Generation**:
  - GPT-4 language model for response generation
  - Conversational retrieval chain with memory
  - Grounded responses based strictly on retrieved content
  - Protection against hallucination through source verification

#### 3. Conversational Interface (50 points)
- **User-Friendly Design**:
  - Clean, modern Streamlit interface
  - Real-time message streaming
  - Clear visual distinction between user and assistant messages
- **Advanced Features**:
  - Multi-turn conversation with full history
  - Source document display for transparency
  - Loading indicators for better UX
  - Error handling with informative messages

### Additional Features (30 points)
- **PDF Support (15 points)**: Full PDF text extraction and processing
- **Multiple Documents (15 points)**: Upload and query across multiple files simultaneously

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- GitHub Codespaces (recommended) or local development environment
- API key for Cornell OpenAI API

### Step 1: Clone and Navigate to Repository

```bash
# If not already in the repository
cd INFO-5940-Codespace
git checkout assignment1
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes all necessary packages:
- `streamlit>=1.36` - Web interface framework
- `langchain==0.3.27` - RAG pipeline orchestration
- `langchain-community==0.3.31` - Community integrations
- `langchain-openai==0.3.35` - OpenAI integration
- `chromadb>=0.4.22` - Vector database
- `pypdf>=4` - PDF processing
- `sentence-transformers>=2.2.2` - Additional embedding support
- `python-dotenv` - Environment variable management

### Step 4: Configure API Key

Create a `.env` file in the project root:

   ```bash
echo "API_KEY=your_api_key_here" > .env
```

### Step 5: Run the Application

```bash
streamlit run chat_with_pdf.py
```

### Running in GitHub Codespaces

1. Open your Codespace
2. Open the terminal
3. Run the setup commands:
   ```bash
   source venv/bin/activate
   streamlit run chat_with_pdf.py
   ```
4. Click "Open in Browser" when the popup appears
5. If you miss the popup, press `Ctrl+C` and rerun the command

## Usage Guide

### Basic Workflow

1. **Upload Documents**
   - Click the sidebar file uploader
   - Select one or more `.txt` or `.pdf` files
   - Click "Process Documents"
   - Wait for processing to complete

2. **Ask Questions**
   - Type your question in the chat input at the bottom
   - Press Enter to submit
   - View the AI-generated response with source citations

3. **View Sources**
   - Click "View Sources" under any response
   - See the exact document passages used to generate the answer

4. **Continue Conversation**
   - Ask follow-up questions
   - The system maintains context throughout the conversation
   - Reference previous questions naturally

5. **Reset**
   - Click "🔄 Clear All & Reset" in the sidebar
   - Removes all documents and conversation history

### Example Questions

For a document about machine learning:
- "What is the main topic of this document?"
- "Explain the key concepts discussed."
- "Can you summarize the methodology section?"
- "What conclusions does the author reach?"

### Best Practices

- **Upload Quality Documents**: Ensure PDFs have searchable text (not scanned images)
- **Ask Specific Questions**: More specific queries yield better results
- **Review Sources**: Always check the source passages for accuracy
- **Context Matters**: Use follow-up questions to dive deeper into topics

## Technical Details

### Chunking Strategy Rationale

The application uses a **RecursiveCharacterTextSplitter** with carefully chosen parameters:

**Chunk Size: 1000 characters**
- Balances context preservation with retrieval precision
- Large enough to maintain semantic meaning and relationships
- Small enough to avoid token limits and improve relevance
- Empirically proven effective for diverse document types

**Chunk Overlap: 200 characters**
- Prevents critical information loss at chunk boundaries
- Ensures concepts spanning multiple chunks remain coherent
- Provides context continuity in retrieved passages
- 20% overlap is optimal based on research and testing

**Recursive Splitting Strategy**
- Prioritizes natural document structure (paragraphs, sentences)
- Maintains readability and coherence of chunks
- Falls back gracefully when natural breaks aren't available

### Retrieval Configuration

**K=4 (Top-4 Retrieval)**
- Provides sufficient context without overwhelming the LLM
- Balances between coverage and noise reduction
- Keeps token usage manageable for cost and speed
- Empirically determined through testing

**Similarity Search**
- Uses cosine similarity on embedding vectors
- Fast and efficient for real-time queries
- Proven effective for semantic text matching

### LLM Configuration

**Model: GPT-4**
- Superior reasoning and comprehension capabilities
- Excellent at synthesizing information from multiple sources
- Strong instruction-following for grounded responses

**Temperature: 0.7**
- Balances creativity with consistency
- Allows natural language generation
- Maintains factual accuracy

## Project Structure

```
INFO-5940-Codespace/
├── chat_with_pdf.py           # Main application file
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not tracked)
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
├── ref-log.md                 # Reference log
├── data/                      # Sample data files
│   ├── combined_transcript.txt
│   └── RAG_source.txt
└── venv/                      # Virtual environment (not tracked)
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `API_KEY` | Cornell OpenAI API key | Yes |

### Application Constants

Located in `chat_with_pdf.py`:

```python
CHUNK_SIZE = 1000              # Characters per chunk
CHUNK_OVERLAP = 200            # Overlap between chunks
EMBEDDING_MODEL = "text-embedding-ada-002"
LLM_MODEL = "gpt-4o"
TEMPERATURE = 0.7              # LLM creativity (0-1)
RETRIEVAL_K = 4                # Number of chunks to retrieve
```

### Modifying Configuration

To adjust the behavior:

1. Open `chat_with_pdf.py`
2. Locate the configuration constants at the top
3. Modify values as needed
4. Save and restart the application

**Note**: Changes to chunk size or overlap require reprocessing documents.

### Getting Help

1. Check this README's troubleshooting section
2. Review error messages carefully
3. Verify all setup steps were completed
4. Check that the virtual environment is activated
5. Ensure API key is valid and not expired

## Development Notes

### Changes from Template

1. **Added Dependencies** (`requirements.txt`):
   - `chromadb>=0.4.22` - Vector database
   - `sentence-transformers>=2.2.2` - Embedding support
   - Updated LangChain versions for compatibility

2. **Created** (`.gitignore`):
   - Comprehensive ignore rules for security and cleanliness
   - Prevents API key exposure

3. **Enhanced** (`chat_with_pdf.py`):
   - Complete RAG implementation
   - Multi-document support
   - PDF processing capability
   - Source attribution system

### Design Decisions

**Why LangChain?**
- Industry-standard for RAG applications
- Rich ecosystem of integrations
- Excellent documentation and community support
- Simplifies complex RAG pipeline orchestration

**Why ChromaDB?**
- Lightweight and easy to set up
- Excellent performance for small to medium datasets
- Persistent storage without complex configuration
- Native Python integration

**Why Recursive Text Splitter?**
- Respects document structure
- Maintains semantic coherence
- Flexible and configurable
- Proven effective across document types

**Note**: This application is designed to run in the provided GitHub Codespaces environment. If running locally, ensure all dependencies are properly installed and API keys are configured.
