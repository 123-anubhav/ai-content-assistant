import os

import requests
import streamlit as st

from dotenv import load_dotenv


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)


# --------------------------------------------------
# Streamlit page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="📚",
    layout="wide"
)


# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 25px;
    }

    .book-info {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Session state
# --------------------------------------------------

if "book_id" not in st.session_state:
    st.session_state.book_id = None

if "filename" not in st.session_state:
    st.session_state.filename = None

if "pages" not in st.session_state:
    st.session_state.pages = 0

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    '<div class="main-title">📚 AI Content Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Upload a book and ask questions using AI'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# Sidebar - Book Upload
# --------------------------------------------------

with st.sidebar:

    st.header("📖 Book")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        if st.button(
            "🚀 Upload & Process",
            use_container_width=True
        ):

            with st.spinner(
                "Uploading and indexing book..."
            ):

                try:

                    response = requests.post(
                        f"{BACKEND_URL}/books/upload",
                        files={
                            "file": (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                "application/pdf"
                            )
                        },
                        timeout=300
                    )

                    if response.status_code == 200:

                        data = response.json()

                        st.session_state.book_id = data.get(
                            "book_id"
                        )

                        st.session_state.filename = data.get(
                            "filename",
                            uploaded_file.name
                        )

                        st.session_state.pages = data.get(
                            "total_pages",
                            0
                        )

                        st.session_state.chat_history = []

                        st.success(
                            "Book uploaded successfully!"
                        )

                    else:

                        st.error(
                            f"Upload failed: "
                            f"{response.text}"
                        )

                except requests.exceptions.RequestException as e:

                    st.error(
                        f"Could not connect to FastAPI: {e}"
                    )


# --------------------------------------------------
# Book information
# --------------------------------------------------

if st.session_state.book_id:

    st.markdown(
        '<div class="book-info">',
        unsafe_allow_html=True
    )

    st.write(
        f"📕 **Book:** "
        f"{st.session_state.filename}"
    )

    st.write(
        f"📄 **Pages:** "
        f"{st.session_state.pages}"
    )

    st.write(
        f"🆔 **Book ID:** "
        f"{st.session_state.book_id}"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# --------------------------------------------------
# Main Chat
# --------------------------------------------------

if not st.session_state.book_id:

    st.info(
        "👈 Upload a PDF from the sidebar to start."
    )

else:

    st.subheader("💬 Ask Your Book")

    # ----------------------------------------------
    # Display previous messages
    # ----------------------------------------------

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):

            st.markdown(
                message["content"]
            )

            if (
                message["role"] == "assistant"
                and message.get("pages")
            ):

                pages = message["pages"]

                st.caption(
                    "📄 Retrieved pages: "
                    + ", ".join(
                        str(page)
                        for page in pages
                    )
                )


    # ----------------------------------------------
    # Chat input
    # ----------------------------------------------

    question = st.chat_input(
        "Ask something about this book..."
    )


    if question:

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)


        # ------------------------------------------
        # Call FastAPI
        # ------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner(
                "Searching the book..."
            ):

                try:

                    response = requests.post(
                        f"{BACKEND_URL}/books/"
                        f"{st.session_state.book_id}/ask",

                        json={
                            "question": question
                        },

                        timeout=180
                    )


                    if response.status_code == 200:

                        data = response.json()

                        answer = data.get(
                            "answer",
                            "No answer returned."
                        )

                        pages = data.get(
                            "pages",
                            []
                        )

                        st.markdown(answer)

                        if pages:

                            st.caption(
                                "📄 Retrieved pages: "
                                + ", ".join(
                                    str(page)
                                    for page in pages
                                )
                            )

                        st.session_state.chat_history.append(
                            {
                                "role": "assistant",
                                "content": answer,
                                "pages": pages
                            }
                        )

                    else:

                        st.error(
                            f"Backend error: "
                            f"{response.text}"
                        )


                except requests.exceptions.RequestException as e:

                    st.error(
                        f"Could not connect to FastAPI: {e}"
                    )