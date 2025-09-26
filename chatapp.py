import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings

# ✅ HuggingFace Embeddings (free & local, no API quota needed)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = text_splitter.split_text(text)
    return [chunk for chunk in chunks if chunk.strip()]


def get_vector_store(text_chunks):
    # Use HuggingFace embeddings here
    text_chunks = [chunk for chunk in text_chunks if chunk.strip()]

    if len(text_chunks) > 200:  # Avoid too large PDFs for demo
        text_chunks = text_chunks[:200]

    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context.
    If the answer is not in the provided context just say, 
    "answer is not available in the context". Don't provide wrong answers.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    model = ChatGoogleGenerativeAI(
        model="models/gemini-1.5-flash",   # ✅ use stable version
        temperature=0.3
    )

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    # ✅ new recommended usage
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain




def user_input(user_question):
    if not os.path.exists("faiss_index"):
        st.warning("⚠️ Please upload and process your PDF files first before asking a question.")
        return

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    if not docs:
        st.info("🤔 I couldn’t find anything relevant in your PDFs. Try rephrasing your question.")
        return

    chain = get_conversational_chain()

    try:
        # ✅ use invoke instead of calling chain directly
        response = chain.invoke({"input_documents": docs, "question": user_question})
        st.write("Reply:", response.get("output_text", "No response generated."))
    except Exception as e:
        if "429" in str(e):
            st.error("⚠️ You’ve reached the daily usage limit for the AI service. Please try again later.")
        elif "404" in str(e):
            st.error("⚠️ The selected model is not available. Try changing the model name in your code.")
        else:
            st.error("⚠️ Oops! Something went wrong. Please try again.")


def main():
    st.set_page_config("Multi PDF Chatbot", page_icon=":scroll:")
    st.header("Multi-PDF's 📚 - Chat Agent 🤖")

    if "docs_ready" not in st.session_state:
        st.session_state.docs_ready = False

    user_question = st.text_input("Ask a Question from the PDF Files uploaded .. ✍️📝")

    if user_question:
        if not st.session_state.docs_ready:
            st.warning("⚠️ Please upload and process your PDF files first before asking a question.")
        else:
            user_input(user_question)

    with st.sidebar:
        st.image("img/Robot.jpg")
        st.write("---")

        st.title("📁 PDF File's Section")
        pdf_docs = st.file_uploader(
            "Upload your PDF Files & \n Click on the Submit & Process Button ",
            accept_multiple_files=True,
            type=["pdf"]
        )

        if st.button("Submit & Process"):
            if not pdf_docs:
                st.warning("⚠️ Please upload at least one PDF file before processing.")
            else:
                with st.spinner("Processing..."):
                    raw_text = get_pdf_text(pdf_docs)
                    if not raw_text.strip():
                        st.error("⚠️ Uploaded PDF seems empty or unreadable. Try another file.")
                        st.session_state.docs_ready = False
                    else:
                        text_chunks = get_text_chunks(raw_text)
                        get_vector_store(text_chunks)
                        st.session_state.docs_ready = True
                        st.success("✅ PDFs processed successfully! You can now ask questions.")

        st.write("---")
        st.image("img/ChatGPT Image Apr 14, 2025, 04_27_49 PM.png")
        st.markdown(
            """
            AI App created by 
            <a href="https://www.linkedin.com/in/hariss-razvi-shaik-31b037333/" target="_blank" style="text-decoration:none;">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="15" style="vertical-align:middle; margin-right:8px; margin-left:8px;">
            <span style="font-size:14px; vertical-align:middle;"><b>SHAIK HARRISS RAZVI</b></span>
            </a>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """ 
        <div style="position: fixed; bottom: 0; left: 0; width: 100%; 
        background-color: #0E1117; padding: 15px; text-align: center;"> 
        © <a href="https://github.com/Hariss22H" target="_blank">SHAIK HARRISS RAZVI</a> | Made with ❤️ 
        </div> 
        """, unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
