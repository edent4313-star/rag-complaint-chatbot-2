from turtle import pd

import streamlit as st
from src.rag_pipeline import run_rag
#from src.retrirver import retrieve

# Page Configuration
st.set_page_config(
    page_title="Complaint Analysis Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Customer Complaint RAG Chatbot")
st.markdown(
    "Ask questions about customer complaints and receive AI-generated answers with supporting sources."
)

# Initialize session state
if "answer" not in st.session_state:
    st.session_state.answer = ""

if "sources" not in st.session_state:
    st.session_state.sources = []

# User Question
question = st.text_input(
    "Enter your question:",
    placeholder="Example: What are common complaints about credit cards?"
)

col1, col2 = st.columns([1, 1])

# Ask Button
with col1:
    ask_button = st.button("Ask")

# Clear Button
with col2:
    clear_button = st.button("Clear")

# Clear functionality
if clear_button:
    st.session_state.answer = ""
    st.session_state.sources = []
    st.rerun()

# Ask functionality
if ask_button:

    if question.strip():

        with st.spinner("Generating answer..."):

            try:
                result = run_rag(question)

                # If run_rag returns answer and sources
                if isinstance(result, tuple):
                    answer, sources = result
                else:
                    answer = result
                    sources = []

                st.session_state.answer = answer
                st.session_state.sources = sources

            except Exception as e:
                st.error(f"Error: {e}")

# Display Answer
if st.session_state.answer:

    st.subheader("AI Answer")

    st.write(st.session_state.answer)

    # Display Sources
    if isinstance(st.session_state.sources, pd.DataFrame) and not st.session_state.sources.empty:

        st.subheader("Sources Used")

        for i, source in enumerate(
                st.session_state.sources,
                start=1
        ):

            with st.expander(f"Source {i}"):

                st.write(source)