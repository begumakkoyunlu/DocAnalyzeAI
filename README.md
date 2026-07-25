# DocAnalyze AI

DocAnalyze AI is a local **Retrieval-Augmented Generation (RAG)** application for intelligent PDF document analysis. Built with **Python**, **Streamlit**, and **Microsoft Foundry Local SDK**, the application enables users to upload one or more PDF documents, ask questions in natural language, and receive context-aware answers supported by evidence extracted directly from the uploaded documents. The entire pipeline runs locally, leveraging semantic retrieval and a local large language model.

---

## Features

- Upload one or multiple PDF documents
- Automatic PDF text extraction
- Intelligent document chunking
- Semantic search using vector embeddings
- Cosine similarity retrieval
- Local LLM inference with Phi-4 Mini
- Conversation history
- Source citation (document name and page number)
- Evidence extraction from source documents
- Chat export functionality

---

## Architecture

```
PDF Documents
      │
      ▼
 PDF Reader
      │
      ▼
 Document Chunking
      │
      ▼
 Embedding Generation
      │
      ▼
 In-Memory Vector Store
      │
      ▼
 Cosine Similarity Retrieval
      │
      ▼
      Phi-4 Mini
      │
      ▼
Answer + Evidence + Source Citation
```

---

## Tech Stack

- Python
- Streamlit
- Microsoft Foundry Local SDK
- Phi-4 Mini
- Qwen3 Embedding Model
- NumPy
- PyPDF

---

## Project Structure

```text
DocAnalyzeAI/
│
├── data/
│   └── Sample_Financial_Report.pdf
│
├── app.py
├── build_vector_store.py
├── chunking.py
├── embedding.py
├── pdf_reader.py
├── rag.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

Clone the repository.

```bash
git clone https://github.com/your-username/DocAnalyzeAI.git
cd DocAnalyzeAI
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate the environment.

### Windows

```bash
.venv\Scripts\activate
```

Install the required dependencies.

```bash
pip install -r requirements.txt
```

---

## Running the Application

Launch the application with Streamlit.

```bash
streamlit run app.py
```

The application will automatically open in your default web browser.

---

## Usage

1. Launch the application.
2. Upload one or more PDF documents.
3. Ask questions about the uploaded documents.
4. The application retrieves the most relevant document chunks.
5. Phi-4 Mini generates an answer using the retrieved context.
6. The response includes:
   - AI-generated answer
   - Supporting evidence
   - Source document
   - Page number

A sample financial report is included in the **data/** directory for demonstration and testing purposes.

---

## Example Questions

- What is the company's revenue?
- What is the net income?
- Summarize the financial report.
- What are the company's main business risks?
- What are the total assets?

---

## Future Improvements

- FAISS vector database integration
- OCR support for scanned PDF documents
- Streaming response generation
- Hybrid keyword and semantic retrieval
- Multi-language document support

---

## Author

**Begüm Akkoyunlu**

Third-Year Business Administration Student at TED University

AI Intern

---

## License

This project is intended for educational and portfolio purposes.