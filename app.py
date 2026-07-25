import streamlit as st
import tempfile
from io import StringIO
from datetime import datetime

from rag import (
    embed_question,
    retrieve_top_chunks,
    load_chat_model,
)

from build_vector_store import build_vector_store

st.set_page_config(
    page_title="DocAnalyze AI",
    page_icon="📄",
    layout="wide"
)

st.title("📄 DocAnalyze AI")

st.caption(
    "AI-powered document analysis with Local RAG, semantic search, and evidence-backed responses."
)

st.write(
    "Upload one or more PDF documents, ask questions in natural language, and receive evidence-backed answers."
)
# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


uploaded_files = st.file_uploader(
    "Upload PDF files",
    type="pdf",
    accept_multiple_files=True
)

if uploaded_files:

    st.success(f"{len(uploaded_files)} PDF uploaded successfully!")

    pdf_files = []

    for uploaded_file in uploaded_files:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp_file:

            tmp_file.write(uploaded_file.getbuffer())

            pdf_files.append(
                {
                    "path": tmp_file.name,
                    "name": uploaded_file.name
                }
            )

    vector_store = build_vector_store(pdf_files)

       # Show previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.write(message["content"])

            if message["role"] == "assistant":

                if "sources" in message:

                    shown_sources = set()

                    for chunk in message["sources"]:

                        source = (
                            chunk["file_name"],
                            chunk["page"]
                        )

                        if source not in shown_sources:

                            shown_sources.add(source)

                            st.caption(
                                f"📄 {chunk['file_name']} — Page {chunk['page']}"
                            )

                    if "evidence" in message:

                        st.caption(
                            f"Evidence: {message['evidence']}"
                        )
    question = st.chat_input("Ask a question")

    if question:

        st.session_state.last_question = question

        with st.chat_message("user"):
            st.write(question)

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.spinner(
            "🔍 Searching documents and generating response..."
        ):

            question_vector = embed_question(question)

            if (
                "summarize" in question.lower()
                or "all" in question.lower()
            ):
                top_k = len(vector_store)
            else:
                top_k = 1

            top_chunks = retrieve_top_chunks(
                question_vector,
                vector_store,
                top_k=top_k
            )

            context = "\n\n".join(
                chunk["text"]
                for chunk in top_chunks
            )

            chat_client = load_chat_model()

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful AI assistant. "
                        "Answer ONLY using the provided context. "
                        "Use previous conversation if it helps. "
                        "If the answer is not available in the uploaded documents, say so."
                    )
                }
            ]

            for message in st.session_state.messages[-6:]:
                messages.append(
                    {
                        "role": message["role"],
                        "content": message["content"]
                    }
                )

            messages.append(
                {
                    "role": "user",
                    "content": f"""
Context:
{context}

Question:
{question}

Instructions:
1. Answer the question using ONLY the provided context.
2. After the answer, write a new line beginning with "Evidence:"
3. The evidence must be the shortest COMPLETE sentence from the context that directly supports the answer.
4. Copy the sentence exactly as it appears in the document.
5. Do not paraphrase or summarize the sentence.
6. If no supporting sentence exists, write "Evidence: No supporting evidence found."
"""
                }
            )

            response = chat_client.complete_chat(
                messages=messages
            )

            full_response = response.choices[0].message.content

            if "Evidence:" in full_response:
                answer, evidence = full_response.split("Evidence:", 1)
                answer = answer.strip()
                evidence = evidence.strip()
            else:
                answer = full_response
                evidence = "No supporting evidence found."

            st.session_state.last_sources = top_chunks
            st.session_state.last_evidence = evidence
        # Show assistant response
        with st.chat_message("assistant"):

            st.write(answer)

            shown_sources = set()

            for chunk in top_chunks:

                source = (
                    chunk["file_name"],
                    chunk["page"]
                )

                if source not in shown_sources:

                    shown_sources.add(source)

                    st.caption(
                        f"📄 {chunk['file_name']} — Page {chunk['page']}"
                    )

            st.caption(
                f"Evidence: {evidence}"
            )


        # Save assistant response with sources
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": top_chunks,
                "evidence": evidence
            }
        )

    # Export chat
    chat_text = StringIO()

    for message in st.session_state.messages:

        role = "You" if message["role"] == "user" else "Assistant"

        chat_text.write(f"{role}:\n")
        chat_text.write(f"{message['content']}\n")

        if message["role"] == "assistant":

            if "sources" in message:

                chat_text.write("\nSources:\n")

                shown_sources = set()

                for chunk in message["sources"]:

                    source = (
                        chunk["file_name"],
                        chunk["page"]
                    )

                    if source not in shown_sources:

                        shown_sources.add(source)

                        chat_text.write(
                            f"• {chunk['file_name']} — Page {chunk['page']}\n"
                        )

                if "evidence" in message:

                    chat_text.write(
                        f"  Evidence: {message['evidence']}\n"
                    )

        chat_text.write("\n")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    st.download_button(
        label="📥 Export Chat",
        data=chat_text.getvalue(),
        file_name=f"DocAnalyzeAI_Chat_{timestamp}.txt",
        mime="text/plain"
    )