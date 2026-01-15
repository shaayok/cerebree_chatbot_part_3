import streamlit as st
from retrieval import retrieve_candidates
from reranker import rerank
from composer import compose_answer, fallback_answer

ASSISTANT_AVATAR = "logo.png"
USER_AVATAR = "👤"

# -----------------------------
# Page config (WIDE)
# -----------------------------
st.set_page_config(
    page_title="CereAura – Autism Parent Support",
    page_icon="logo.png",
    layout="wide"
)

# -----------------------------
# Background + layout styling
# -----------------------------
st.markdown(
    """
    <style>
    /* OVERRIDE STREAMLIT THEME VARIABLES */
    :root {
        --text-color: #1f2937;
        --primary-text-color: #1f2937;
        --secondary-text-color: #4b5563;
        --background-color: #FFFBEA;
    }

    /* App background */
    .stApp {
        background-color: #FFFBEA;
    }

    /* Titles & headers */
    h1, h2, h3, h4, h5, h6,
    [data-testid="stTitle"] {
        color: #1f2937 !important;
    }

    /* Normal text */
    p, li {
        color: #1f2937;
    }

    /* Chat messages */
    .stChatMessage p {
        color: #1f2937;
    }

    /* Chat input */
    .stChatInput textarea {
        color: #1f2937 !important;
        background-color: #ffffff !important;
    }

    /* Send button */
    .stChatInput button {
        color: #2563eb !important;
        opacity: 1 !important;
        pointer-events: auto !important;
    }

    .stChatInput button:hover {
        color: #1d4ed8 !important;
    }

    /* Captions */
    .stCaption {
        color: #4b5563;
    }

    /* Layout width */
    .block-container {
        max-width: 1400px;
        padding-left: 4rem;
        padding-right: 4rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


header_left, header_right = st.columns([5, 1])

with header_left:
    st.title("CereAura – Autism Support Assistant")
    st.caption("Supportive, psychologist-informed guidance for parents")

with header_right:
    st.image(
        "top_right.png",
        width=120
    )

# st.title("CereAura – Autism Support Chatbot")
# st.caption("Supportive, psychologist-informed guidance for parents")

# -----------------------------
# Layout columns
# -----------------------------
left_spacer, main_col, right_spacer = st.columns([1, 3, 1])

with left_spacer:
    st.markdown("#### 🌱 Gentle reminder")
    st.markdown(
        """
        <div style="background-color:#FFFFFF;
        color:#1F2937;
        padding:16px;
        border-radius:12px;
        box-shadow:0 2px 6px rgba(0,0,0,0.05);
        font-size:14px;
        line-height:1.6;">
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
        <div style="background-color:#FFFFFF;
        color:#1F2937;
        padding:16px;
        border-radius:12px;
        box-shadow:0 2px 6px rgba(0,0,0,0.05);
        font-size:14px;
        line-height:1.6;">
        Guidance here is based on psychologist-provided,
        evidence-based strategies for everyday parenting.
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
# Render chat + input
# -----------------------------
with main_col:
    # Render messages
    for msg in st.session_state.messages:
        avatar = ASSISTANT_AVATAR if msg["role"] == "assistant" else USER_AVATAR
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

    # Chat input MUST be last
    user_input = st.chat_input("Type your question here...")

# -----------------------------
# Handle new input
# -----------------------------
# -----------------------------
# Handle new input (WITH spinner)
# -----------------------------
if user_input:
    # 1. Save user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    # 2. Render assistant bubble + spinner
    with main_col:
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

    # 3. Save assistant message AFTER generation
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    # 4. Rerun to replace spinner with final text
    st.rerun()
