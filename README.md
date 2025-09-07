# 🤖 Multi-PDFs Chat Agent with Google Gemini AI

An **AI-powered chatbot** built with **Streamlit, LangChain, FAISS, and Google Gemini AI** that allows users to upload and interact with **multiple PDF files**.  
It performs **semantic search** over the documents and provides **context-aware answers** through a conversational interface.

🔗 **Live Demo:** [Try it here](https://hariss-chatbot.streamlit.app/)  

---

## 📌 Overview
Managing and extracting insights from lengthy PDFs can be time-consuming.  
This project solves that problem by enabling users to **chat with multiple PDFs** — upload files, ask natural language questions, and get instant, accurate answers directly from the content.
##  Flow:

- PDFs are uploaded → text is extracted.
- Text is chunked into manageable parts.
- Each chunk is embedded with Gemini → stored in FAISS.
- On user query → relevant chunks are retrieved.
- Gemini LLM generates a response with context.

The system uses:
- **Gemini embeddings** for semantic understanding  
- **FAISS vector database** for fast document retrieval  
- **LangChain QA pipeline** for structured reasoning  
- **Streamlit** for a clean, interactive UI  

---
## 🏗️ Architecture Overview

- **PDF Extraction:** `PyPDF2` reads all uploaded pages.
- **Chunking:** `RecursiveCharacterTextSplitter` from LangChain.
- **Embeddings:** Google’s `embedding-001` model (Gemini).
- **Vector Storage:** FAISS local DB.
- **LLM Model:** Gemini `gemini-1.5-pro-latest`.
- **Prompt:** Custom chain for accurate and safe answers.
- **Frontend:** Streamlit app with sidebar UI.
  
---
## 🚀 Features
- 📄 **Multi-PDF Upload** – process multiple documents in one session  
- 🔍 **Semantic Search** – powered by FAISS & Gemini embeddings  
- 🤖 **Conversational Q&A** – context-aware answers only from PDFs  
- ⛔ **Hallucination Control** – replies *“Not in context”* if answer is missing  
- 🧾 **Chunk-based Processing** – handles large PDFs efficiently  
- 🌐 **Streamlit Web UI** – responsive, beginner-friendly interface  
- ⚡ **Live Deployment** – hosted on Streamlit Cloud  

---

## 📊 Performance

- ✅ Real-time Q&A after processing
- ✅ Works with multiple PDFs simultaneously
- 📉 Performance varies with PDF quality (e.g., scanned vs text-based)
- 🚫 Does not fabricate answers — limited strictly to uploaded docs

---

## 📁 Project Structure

```text
Multi-PDFs_ChatApp_AI-Agent-main/
├── chatapp.py                  # Main Streamlit App
├── check_models.py             # Gemini model lister
├── requirements.txt            # Python dependencies
├── .env                        # API key config (DO NOT COMMIT)
├── img/
│   ├── Robot.jpg
│   └── ChatGPT Image Apr 14, 2025.png
├── faiss_index/                # Auto-generated FAISS vector index
└── README.md

```
## 🛠 Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/MultiPDF-ChatAgent.git
cd MultiPDF-ChatAgent
```
### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 3️⃣ Google API Key
```bash
GOOGLE_API_KEY=your_actual_key
```
### 4️⃣ Deploy with Streamlit
```bash
 streamlit run chatapp.py
```
## 🌐 Deployment

This app is deployed on Streamlit Cloud.
Secrets (GOOGLE_API_KEY) are securely managed in the Streamlit dashboard.

👉 Want to deploy your own? Just:

Push repo to GitHub

Deploy on Streamlit Cloud

Add your API key under Secrets

---

## ⚠️ Important
- Do NOT commit your .env file.
- To keep it out of version control, add this line to .gitignore:
```bash
   echo ".env" >> .gitignore
```
## 🛠 Future Enhancements
-🗂 Support for DOCX, TXT files

-🧾 Summarization of PDF content

-🗣 Voice-based querying

-🔐 User authentication & session storage

-📜 Auto-report generation from conversations

## 👨‍💻 Author
**SHAIK HARRISS RAZVI**  
🔗 [LinkedIn](https://www.linkedin.com/in/hariss-razvi-shaik-31b037333/) | [GitHub](https://github.com/Hariss22H)

## 💡 Acknowledgments
- Google Generative AI (Gemini)
- LangChain
- FAISS by Facebook AI Research
- Streamlit
