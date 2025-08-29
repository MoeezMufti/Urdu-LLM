# Urdu-LLM
A prototype web application for Urdu text summarization and question answering. Built with Streamlit and integrated with the OpenAI API, it provides a chat-style interface for interactive analysis. Chats are saved in a JSON file with support for multiple sessions.

This project is intended as an academic prototype: simple, functional, and expandable. Future work includes database storage, user authentication, offline/local model integration, and document analysis features.

# Getting Started
1. Clone the Repository
*git clone <repo-link>*
*cd urdu-notebook*

2. Install Dependencies
*pip install -r requirements.txt*

3. Set up Environment

*Create a .env file in the project root and add your OpenAI key:*
*OPENAI_API_KEY=your_api_key_here*

4. Run the App
*streamlit run app_v02.py*

# Limitations
Summarization and question answering depend on the OpenAI API and are therefore subject to internet connectivity, rate limits, and quota restrictions.
Chat storage relies on a JSON file, which is not scalable for multiple users.
Streamlit is primarily a prototyping tool; the system would need a different architecture for production deployment.
This project is intended as a prototype for academic exploration. Its purpose is to demonstrate a workflow for Urdu text analysis through summarization and question answering.
