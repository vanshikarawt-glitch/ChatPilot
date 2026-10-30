
import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="ChatPilot | AI Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------
# GEMINI API CONNECTION
# -----------------------------------

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={
        "timeout": 30000,
        "retry_options": {
            "attempts": 2,
            "initial_delay": 1
        }
    }
)

MODEL_NAME = "gemini-3.5-flash-lite"

# -----------------------------------
# WEBSITE DESIGN
# -----------------------------------

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            ellipse at 70% 25%,
            rgba(184, 211, 255, 0.65),
            transparent 48%
        ),
        radial-gradient(
            ellipse at 42% 80%,
            rgba(255, 187, 218, 0.55),
            transparent 50%
        ),
        linear-gradient(
            135deg,
            #FFFFFF 0%,
            #F4F0FF 45%,
            #EAF4FF 100%
        );
    color: #282838;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #EAE7F0;
}

.sidebar-brand {
    font-size: 25px;
    font-weight: 800;
    color: #303246;
    padding: 10px 0 22px;
}

.sidebar-subtitle {
    color: #9292A4;
    font-size: 12px;
    letter-spacing: 1px;
    margin-top: 20px;
    margin-bottom: 10px;
}

.hero {
    text-align: center;
    padding: 90px 10px 35px;
}

.hero-icon {
    font-size: 58px;
    margin-bottom: 20px;
}

.hero-title {
    font-size: 46px;
    font-weight: 800;
    color: #29283B;
    margin-bottom: 12px;
    line-height: 1.2;
}

.hero-subtitle {
    font-size: 18px;
    color: #757589;
    line-height: 1.7;
}

.stButton > button {
    background: rgba(255, 255, 255, 0.85);
    border: 1px solid #EAE7F0;
    border-radius: 16px;
    color: #35354A;
    padding: 12px 14px;
}

.stButton > button:hover {
    background: #F1EDFF;
    border-color: #B9ACEC;
    color: #46407A;
}

button[kind="primary"] {
    background: #47415D !important;
    color: white !important;
    border: none !important;
}

[data-testid="stChatInput"] {
    border-radius: 20px;
    background: #FFFFFF;
    border: 1px solid #E4DFF0;
    box-shadow: 0 8px 30px rgba(75, 70, 110, 0.08);
}

[data-testid="stChatMessage"] {
    background: rgba(255, 255, 255, 0.65);
    border: 1px solid rgba(230, 225, 245, 0.8);
    border-radius: 18px;
    margin-bottom: 12px;
}

.footer-text {
    text-align: center;
    font-size: 12px;
    color: #9995A8;
    margin-top: 24px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# CHAT SESSION SETUP
# -----------------------------------

if "chats" not in st.session_state:
    st.session_state.chats = {
        "1": {
            "title": "New Chat",
            "messages": []
        }
    }

if "chat_counter" not in st.session_state:
    numeric_ids = [
        int(chat_id)
        for chat_id in st.session_state.chats
        if str(chat_id).isdigit()
    ]
    st.session_state.chat_counter = max(numeric_ids, default=0)

if (
    "active_chat" not in st.session_state
    or st.session_state.active_chat not in st.session_state.chats
):
    st.session_state.active_chat = list(
        st.session_state.chats.keys()
    )[-1]


# -----------------------------------
# CHAT MANAGEMENT FUNCTIONS
# -----------------------------------

def create_chat():
    st.session_state.chat_counter += 1

    chat_id = str(st.session_state.chat_counter)

    st.session_state.chats[chat_id] = {
        "title": "New Chat",
        "messages": []
    }

    st.session_state.active_chat = chat_id


def start_new_chat():
    current_id = st.session_state.active_chat

    current_messages = st.session_state.chats[
        current_id
    ]["messages"]

    # Don't create repeated empty chats
    if not current_messages:
        return

    create_chat()


def delete_chat(chat_id):
    if chat_id in st.session_state.chats:
        del st.session_state.chats[chat_id]

    if not st.session_state.chats:
        create_chat()

    elif (
        st.session_state.active_chat
        not in st.session_state.chats
    ):
        st.session_state.active_chat = list(
            st.session_state.chats.keys()
        )[-1]


# Remove old unused empty chats
for chat_id in list(st.session_state.chats.keys()):

    if chat_id != st.session_state.active_chat:

        if not st.session_state.chats[chat_id]["messages"]:
            del st.session_state.chats[chat_id]


# -----------------------------------
# SIDEBAR
# -----------------------------------

with st.sidebar:

    st.markdown(
        '<div class="sidebar-brand">✨ ChatPilot</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "＋ New Chat",
        use_container_width=True,
        type="primary"
    ):
        start_new_chat()
        st.rerun()

    st.markdown(
        '<div class="sidebar-subtitle">YOUR WORKSPACE</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "⌂ Home",
        use_container_width=True
    ):
        start_new_chat()
        st.rerun()

    st.markdown(
        '<div class="sidebar-subtitle">RECENT CHATS</div>',
        unsafe_allow_html=True
    )

    for chat_id in reversed(
        list(st.session_state.chats.keys())
    ):

        chat = st.session_state.chats[chat_id]

        col_chat, col_delete = st.columns([5, 1])

        with col_chat:

            if st.button(
                "💬 " + chat["title"][:23],
                key=f"open_{chat_id}",
                use_container_width=True
            ):
                st.session_state.active_chat = chat_id
                st.rerun()

        with col_delete:

            if st.button(
                "🗑",
                key=f"delete_{chat_id}",
                help="Delete this chat"
            ):
                delete_chat(chat_id)
                st.rerun()

    st.divider()

    st.caption("Your personal AI assistant")
    st.caption("Powered by Gemini AI")


# -----------------------------------
# CURRENT CONVERSATION
# -----------------------------------

current_chat = st.session_state.chats[
    st.session_state.active_chat
]

messages = current_chat["messages"]

suggested_prompt = None


# -----------------------------------
# HOME PAGE
# -----------------------------------

if len(messages) == 0:

    st.markdown(
        '<div class="hero">'
        '<div class="hero-icon">✨</div>'
        '<div class="hero-title">'
        'Welcome to ChatPilot'
        '</div>'
        '<div class="hero-subtitle">'
        'Your all-in-one AI assistant for learning, '
        'coding, creativity and everyday ideas.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        if st.button(
            "💬 Ask Anything",
            use_container_width=True
        ):
            suggested_prompt = "What can you help me with?"

    with col2:
        if st.button(
            "💻 Write Code",
            use_container_width=True
        ):
            suggested_prompt = "Write a simple Python program."

    with col3:
        if st.button(
            "📚 Explain Concepts",
            use_container_width=True
        ):
            suggested_prompt = (
                "Explain artificial intelligence in simple words."
            )

    col4, col5, col6 = st.columns(3, gap="medium")

    with col4:
        if st.button(
            "💡 Generate Ideas",
            use_container_width=True
        ):
            suggested_prompt = "Give me five creative project ideas."

    with col5:
        if st.button(
            "✍️ Help Me Write",
            use_container_width=True
        ):
            suggested_prompt = "Help me write a professional email."

    with col6:
        if st.button(
            "🎓 Study Assistant",
            use_container_width=True
        ):
            suggested_prompt = "Give me useful Python study tips."

    st.write("")
    st.write("")


# -----------------------------------
# DISPLAY PREVIOUS MESSAGES
# -----------------------------------

for message in messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# -----------------------------------
# CHAT INPUT
# -----------------------------------

with st.container():

    user_input = st.chat_input(
        "Ask ChatPilot anything..."
    )

if suggested_prompt:
    user_input = suggested_prompt


# -----------------------------------
# GENERATE AI RESPONSE
# -----------------------------------

if user_input:

    # Save user message
    messages.append({
        "role": "user",
        "content": user_input
    })

    # Create conversation title
    if current_chat["title"] == "New Chat":
        current_chat["title"] = user_input[:25]

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    # -----------------------------------
    # CONVERSATION MEMORY
    # -----------------------------------

    conversation = []

    # Send the latest 20 valid messages to Gemini
    # Skip error replies and unsuccessful turns

    valid_messages = []

    for index, message in enumerate(messages):

        if message.get("error"):
            continue

        if message["role"] == "user":

            is_latest = index == len(messages) - 1

            has_successful_reply = (
                index + 1 < len(messages)
                and messages[index + 1]["role"] == "assistant"
                and not messages[index + 1].get("error")
            )

            if is_latest or has_successful_reply:
                valid_messages.append(message)

        elif message["role"] == "assistant":
            valid_messages.append(message)

    for message in valid_messages[-20:]:

        role = (
            "model"
            if message["role"] == "assistant"
            else "user"
        )

        conversation.append(
            types.Content(
                role=role,
                parts=[
                    types.Part.from_text(
                        text=message["content"]
                    )
                ]
            )
        )

    # -----------------------------------
    # GEMINI API REQUEST
    # -----------------------------------

    with st.chat_message("assistant"):

        with st.spinner("ChatPilot is thinking..."):

            error_occurred = False

            try:

                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=conversation
                )

                bot_reply = (
                    response.text
                    or "Sorry, I could not generate an answer."
                )

            except Exception as e:

                error_occurred = True

                error_code = getattr(
                    e, "code",
                    getattr(e, "status_code", "Unknown")
                )

                print(
                    "Gemini API Error:",
                    type(e).__name__,
                    error_code
                )

                bot_reply = (
                    f"AI Error: {type(e).__name__} "
                    f"(Code: {error_code})"
                )

        st.write(bot_reply)

    # Save assistant message
    messages.append({
        "role": "assistant",
        "content": bot_reply,
        "error": error_occurred
    })

    # Refresh to display chat above input
    st.rerun()


# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown(
    '<div class="footer-text">'
    'ChatPilot • Your intelligent AI companion'
    '</div>',
    unsafe_allow_html=True
)
