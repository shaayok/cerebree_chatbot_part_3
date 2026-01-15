import streamlit as st
from retrieval import retrieve_candidates
from reranker import rerank
from composer import compose_answer, fallback_answer

# st.set_page_config(
#     page_title="CereAura – Autism Parent Support",
#     layout="centered"
# )
ASSISTANT_AVATAR = "logo.png"
USER_AVATAR = "👤"   # or None if you prefer default

st.set_page_config(
    page_title="CereAura – Autism Parent Support",
    page_icon="logo.png",
    layout="centered"
)
st.markdown(
    """
    <style>
    /* Overall app background */
    .stApp {
        background-color: #FFFBEA;
    }

    /* Main content container */
    .block-container {
        padding-left: 4rem;
        padding-right: 4rem;
        max-width: 1400px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title(" CereAura – Autism Support Chatbot")
st.caption("Supportive, psychologist-informed guidance for parents")
left_spacer, main_col, right_spacer = st.columns([1, 3, 1])
with left_spacer:
    st.markdown("#### 🌱 Gentle reminder")
    st.markdown(
        """
        <div style="
            background-color:#FFFFFF;
            padding:16px;
            border-radius:12px;
            box-shadow:0 2px 6px rgba(0,0,0,0.05);
            font-size:14px;
        ">
        Progress doesn’t happen all at once.<br><br>
        Small, consistent moments of support
        can make a meaningful difference over time.
        </div>
        """,
        unsafe_allow_html=True
    )
with right_spacer:
    st.markdown("#### 🧠 About CereAura")
    st.markdown(
        """
        <div style="
            background-color:#FFFFFF;
            padding:16px;
            border-radius:12px;
            box-shadow:0 2px 6px rgba(0,0,0,0.05);
            font-size:14px;
        ">
        Guidance here is based on
        psychologist-provided,
        evidence-based strategies
        designed for everyday parenting.
        </div>
        """,
        unsafe_allow_html=True
    )



# -----------------------------
# Initialize chat history
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello 👋 I’m really glad you’re here.\n\n"
                "You can ask me questions about supporting your child with autism — "
                "communication, routines, emotions, transitions, or daily challenges.\n\n"
                "What’s on your mind today?"
            )
        }
    ]

# -----------------------------
# Display chat history
# -----------------------------
with main_col:
    for msg in st.session_state.messages:
        avatar = ASSISTANT_AVATAR if msg["role"] == "assistant" else USER_AVATAR
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

# -----------------------------
# Chat input
# -----------------------------
    user_input = st.chat_input(
        "Type your question here..."
    )

if user_input:
    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user",avatar=USER_AVATAR):
        st.write(user_input)

    # Generate assistant response
    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
        with st.spinner("Thinking carefully about this..."):
            candidates = retrieve_candidates(user_input)
            selected = rerank(user_input, candidates)

            final_chunks = [
                c for c in candidates
                if c["tip_number"] in selected
            ]

            if final_chunks:
                answer = compose_answer(user_input, final_chunks)
            else:
                answer = fallback_answer(user_input)

            st.write(answer)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
