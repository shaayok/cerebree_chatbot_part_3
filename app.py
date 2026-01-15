import streamlit as st
from retrieval import retrieve_candidates
from reranker import rerank
from composer import compose_answer, fallback_answer

st.set_page_config(page_title="Autism Parent Support", layout="centered")
st.title("Autism Support Chatbot (For Parents)")

question = st.text_area(
    "Ask a question about supporting your child:",
    height=100
)

if st.button("Get guidance") and question.strip():
    with st.spinner("Finding helpful guidance..."):
        candidates = retrieve_candidates(question)
        selected = rerank(question, candidates)

        final_chunks = [
            c for c in candidates
            if c["tip_number"] in selected
        ]

        if final_chunks:
            answer = compose_answer(question, final_chunks)
            source = "Psychologist-provided guidance"
        else:
            answer = fallback_answer(question)
            source = "General guidance"

    st.markdown("### Answer")
    st.write(answer)
    st.caption(f"Source: {source}")
