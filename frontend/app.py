import streamlit as st
import requests
import os
from dotenv import load_dotenv
load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")

st.set_page_config(
            page_title = "AI Medical Chatbot",
            page_icon = "🏥",
            layout = "wide",
            initial_sidebar_state="expanded",
            menu_items = {'Get help':'mailto:kshivayadav7@gmail.com'})

st.markdown("""
<style>
.chat-container {
        max-width: 900px;
        margin: auto;
    }
.user-msg {
        background: #DCF8C6;
        padding: 14px 18px;
        border-radius: 15px;
        margin: 10px 0;
        text-align: right;
        float: right;
        clear: both;
        max-width: 75%;
        box-shadow: 0 3px 6px rgba(0,0,0,0.1);
    }
.user-msg h4 {
        margin: 0 0 6px 0;
        color: #34A853;
    }
.bot-msg {
        background: #F1F6FF;
        padding: 14px 18px;
        border-radius: 15px;
        margin: 10px 0;
        text-align: left;
        float: left;
        clear: both;
        max-width: 75%;
        border-left: 5px solid #2b7cff;
        box-shadow: 0 3px 6px rgba(0,0,0,0.1);
    }
.bot-msg h4 {
        margin: 0 0 6px 0;
        color: #2b7cff;
    }
.footer {
    font-size: 12px;
    color: gray;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.title("🏥 AI Medical Chatbot")
st.markdown("💡 *Ask medical-related questions and get concise, reliable answers powered by AI.*")
st.markdown('---')


st.sidebar.title("ℹ️ About the Project")
st.sidebar.info("""
    This AI-powered medical chatbot uses **Retrieval-Augmented Generation (RAG)**  
    to provide accurate answers from verified medical literature.
    """)
with st.sidebar:
    st.markdown("### 🔌 System Status")
    try:
        requests.get(BACKEND_URL, timeout=3)
        st.success("Backend Online")
    except Exception:
        st.error("Backend Offline")

if st.sidebar.button("🧹 Clear Chat"):
    st.rerun()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

question = st.text_area(
    "🩺 Enter your medical question",
    placeholder="E.g. What are the symptoms of diabetes?",
    height=120
)

submit = st.button("Get Medical Advice",
                   key="get_answer",
                   icon="🚑",
                   type="primary")

if submit:
    if question.strip() == "":
        st.warning("⚠️ Please enter a valid medical question.")
        st.stop()

    st.session_state.chat_history.append(
        {"role": "user", "content": question}
    )

    payload = {
        "question": question
    }
    with st.spinner("🧠 Getting your medical advice..."):
        try:
            response = requests.post(
                                    BACKEND_URL,
                                    json = payload
                                    )
            response.raise_for_status()
            try:
                data = response.json()
            except ValueError:
                st.error("❌ Invalid response received from backend.")
                st.stop()
            result = data.get('answer')
            if not result:
                st.warning("⚠️ No answer returned from the chatbot.")

            else:
                st.session_state.chat_history.append(
                    {"role": "bot", "content": result}
                )
                
                st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

                for chat in st.session_state.chat_history:
                    if chat["role"] == "user":
                        st.markdown(
                            f"<div class='user-msg'>🧑‍💬 {chat['content']}</div>",
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"""
                            <div class='bot-msg'>
                                <h4>🤖 Medibot</h4>
                                {chat['content']}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                st.markdown("</div>", unsafe_allow_html=True)

        except requests.exceptions.ConnectionError:
            st.error("🔌 Unable to connect to the backend service.")

        except requests.exceptions.HTTPError as http_err:
            st.error(f"🚫 HTTP error occurred: {http_err}")

        except requests.exceptions.RequestException as req_err:
            st.error(f"❌ Request error: {req_err}")

        except Exception as e:
            st.error(f"⚠️ Unexpected error occurred: {e}")

st.markdown("---")
st.markdown(
    "<div class='footer'>© 2025 AI Medical Chatbot | For educational purposes only</div>",
    unsafe_allow_html=True
)




