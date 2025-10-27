# Quick Start Guide

Get up and running with the RAG Document Chat Application in 5 minutes!

## Prerequisites

- GitHub Codespaces or Python 3.9+ environment
- API key from Cornell (provided by instructor)

## Setup (5 Steps)

### 1. Navigate to the project and checkout the correct branch

```bash
cd INFO-5940-Codespace
git checkout assignment1
```

### 2. Create and activate virtual environment

```bash
# Create venv
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
# venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Streamlit (UI framework)
- LangChain (RAG pipeline)
- ChromaDB (vector database)
- PyPDF (PDF processing)
- And all necessary dependencies

### 4. Set up API key

Create a `.env` file in the project root:

```bash
echo "API_KEY=your_actual_api_key_here" > .env
```

**Important:** Replace `your_actual_api_key_here` with your actual API key!

### 5. Run the application

```bash
streamlit run chat_with_pdf.py
```

The application will open in your browser automatically!

## Using the Application

1. **Upload Documents**
   - Click "Browse files" in the sidebar
   - Select one or more `.txt` or `.pdf` files
   - Click "🚀 Process Documents"
   - Wait for processing (you'll see progress indicators)

2. **Ask Questions**
   - Type your question in the chat input at the bottom
   - Press Enter
   - View the AI response with source citations

3. **Continue the Conversation**
   - Ask follow-up questions
   - The system remembers context from previous exchanges

4. **Reset**
   - Click "🔄 Clear All & Reset" to start fresh

## Example Workflow

```
1. Upload a document about machine learning
2. Ask: "What is this document about?"
3. Ask: "Can you explain the main concepts?"
4. Ask: "What are the practical applications mentioned?"
```

## Troubleshooting

### API Key Error
```bash
# Verify .env file exists and has correct format
cat .env
# Should show: API_KEY=sk-xxxxx...
```

### Import Errors
```bash
# Ensure venv is activated - you should see (venv) in your terminal
# If not:
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Application won't start
```bash
# Check Python version
python --version  # Should be 3.9 or higher

# Verify Streamlit installation
streamlit --version

# Try running with full Python path
python -m streamlit run chat_with_pdf.py
```

## GitHub Codespaces Specific

If running in Codespaces:

1. When you run `streamlit run chat_with_pdf.py`, a popup will appear
2. Click "Open in Browser"
3. If you miss the popup:
   - Press `Ctrl+C` to stop
   - Run the command again
   - The popup should reappear
