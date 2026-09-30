# INTERN FAQ - Offline-First AI-Powered Knowledge Assistant

> **Microsoft AI Innovators Summer Internship Project**

![Python](https://img.shields.io/badge/Python-3.14-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Async-009688.svg)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector%20DB-red.svg)
![Bootstrap 5](https://img.shields.io/badge/Bootstrap-5-purple.svg)

---

## 🌟 Overview

**INTERN FAQ** is a professional, offline-first Retrieval-Augmented Generation (RAG) web application designed specifically to streamline onboarding and operational queries for interns and employees. Powered by semantic search vector databases and modern LLM embeddings, it bridges the gap between static internal documentation and instant, context-aware answers.

Developed during the **Microsoft AI Innovators Summer Internship**, this project showcases clean client-server architecture, fast in-memory vector indexing, and localized document processing without relying on expensive, complex cloud inference APIs.

---

## 🚀 Key Features

*   **Semantic RAG Engine**: Converts raw Markdown documents (`faq.md`) into dense vector embeddings using `sentence-transformers` (`all-MiniLM-L6-v2`) and indexes them in an in-memory **Qdrant** vector database for high-precision semantic search.
*   **Asynchronous FastAPI Backend**: Ensures non-blocking query handling, seamless JSON data exchange, and robust CORS configuration.
*   **Responsive Web UI**: Built with **Bootstrap 5** for an intuitive, modern, and mobile-friendly conversational dashboard.
*   **Client-Side PDF Report Generation**: Leverages `html2pdf.js` to instantly transform the complete internal FAQ dataset or active session summaries into downloadable, formatted PDF guides.
*   **Offline-First & Privacy-Centric**: Runs locally, ensuring internal company or internship guidelines remain secure.

---

## 📸 Application Screenshots

### 1. Home Page
`/static/photos/home.png`

### 2. Interactive Semantic Query Interface
> *Users can type natural language questions or keywords to query the internal knowledge base instantly.*
`static/photos/answer.png`

### 3. Full-Document PDF Export
> *Generates a structured, beautifully formatted PDF report containing the entire FAQ knowledge repository.*
`/static/photos/output.png`

---

## 🛠️ Tech Stack

*   **Backend**: Python, FastAPI, Uvicorn
*   **Vector Database**: Qdrant (`qdrant-client`)
*   **Embeddings**: `sentence-transformers` (`all-MiniLM-L6-v2`)
*   **Frontend**: HTML5, JavaScript (ES6+), Bootstrap 5, `html2pdf.js`
*   **Data Source**: Markdown (`faq.md`)

---

## ⚙️ Project Structure 

office-rag-assistant/
│
├── main.py              # FastAPI server, Qdrant indexing, and search endpoints
├── faq.md               # Core knowledge base data source
├── static/              # Frontend assets directory
│   ├── UI.html          # Main user interface markup
│   ├── index.js         # Client-side event listeners and API handlers
│   └── style.css        # Responsive Web UI
└── README.md            # Project documentation

---

## 📦 Installation & Quick StartFollow these steps to run the project locally:

Clone the repository:

Bash
git clone [https://github.com/your-username/intern-faq.git](https://github.com/your-username/intern-faq.git)
cd intern-faq
Install the required dependencies:

Bash
pip install fastapi uvicorn qdrant-client sentence-transformers
Run the FastAPI server:

Bash
python -m uvicorn main:app --reload
Access the application:
Open your browser and navigate to:
http://127.0.0.1:8000

---

## 💡 API Endpoints

The FastAPI backend exposes the following core endpoints for client-server communication:

*   `GET /`: Serves the frontend web interface (`index.html`).
*   `POST /api/ask`: Accepts a JSON payload containing the user query and performs an in-memory vector search via Qdrant to return the best semantic match.
    *   **Request Body**: `{"query": "your question here"}`
    *   **Response**: `{"question": "Matched FAQ Question", "answer": "Detailed answer..."}`
*   `GET /api/all-faq`: Fetches the raw content of the `faq.md` file to power the client-side full-document PDF export feature.

---

## 🎨 UI & UX Highlights

*   **Responsive Dashboard**: Built with Bootstrap 5, providing a clean chat-like interaction card and instant feedback states.
*   **One-Click PDF Compilation**: Automatically aggregates internal documentation into a downloadable, cleanly styled PDF report (`ofis-staj-tum-faq-rehberi.pdf`) with highlighted questions.
*   **Zero External Inference Cost**: Runs locally using lightweight sentence transformers, ensuring complete data privacy and fast response times without hitting external cloud rate limits.

---

## 🛡️ License

This project is developed as part of the **Microsoft AI Innovators Summer Internship** program and is open-source under the [MIT License](LICENSE).