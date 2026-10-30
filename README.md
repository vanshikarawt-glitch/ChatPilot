# 🤖 ChatPilot – AI-Powered Chatbot

ChatPilot is an AI-powered chatbot web application developed using **Python, Streamlit, and Google Gemini API**. It helps users with questions, coding, learning, writing, and creative ideas through an interactive chat interface.

## 🌐 Live Demo

**Try ChatPilot:** https://chatpilot-6boqtvoo86ytto4cinxcc6.streamlit.app/

## ✨ Key Features

- **AI-Powered Chat:** Generates intelligent responses using Google Gemini API.
- **Conversation Memory:** Remembers previous messages within the same chat session.
- **New Chat:** Start multiple independent conversations.
- **Chat History:** View and switch between previous conversations during the active session.
- **Delete Chat:** Remove unwanted conversations.
- **Quick Suggestions:** Get help with coding, learning, writing, and generating ideas.
- **Modern UI:** Clean and responsive interface with a soft gradient background.
- **Error Handling:** Handles API connection failures and timeouts.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Web application interface |
| Google Gemini API | AI response generation |
| HTML & CSS | UI styling |
| Python-dotenv | Environment variable management |
| Git & GitHub | Version control |
| Streamlit Community Cloud | Application deployment |

## ⚙️ Installation and Setup

**1. Clone the repository**

```bash
git clone https://github.com/vanshikarawt-glitch/ChatPilot.git
```

**2. Open the project directory**

```bash
cd ChatPilot
```

**3. Install required libraries**

```bash
pip install -r requirements.txt
```

**4. Configure the API key**

Create a `.env` file in the project folder:

```env
GEMINI_API_KEY=your_api_key_here
```

Never share or commit your actual API key.

**5. Run the application**

```bash
streamlit run app.py
```

## 🧠 How ChatPilot Works

1. The user enters a message in the chatbox.
2. The application prepares the message and conversation history.
3. The request is sent to the Google Gemini API.
4. Gemini generates a response.
5. ChatPilot displays the answer and updates the current session's chat history.

## 📌 Current Limitations

- Chat history is stored temporarily using Streamlit Session State.
- User login and registration are not currently available.
- Conversations are not permanently stored in a database.
- AI responses depend on Gemini API availability and rate limits.

## 🚀 Future Enhancements

- User login and registration
- Database integration for permanent chat history
- Chat export and download options
- Improved reliability and additional AI features

## 🔗 Project Links

**GitHub Repository:** https://github.com/vanshikarawt-glitch/ChatPilot

**Live Website:** https://chatpilot-6boqtvoo86ytto4cinxcc6.streamlit.app/
