# Urdu-LLM
v0.1

A first prototype for Urdu text summarization and question answering, built with Streamlit. This version introduces a simple interface where users can paste Urdu text or ask questions. Summarization is handled by a rule-based function that extracts the first two sentences, and Q&A is generated through a placeholder response. Chats are stored in a JSON file to allow saving and revisiting sessions.

This branch demonstrates the core workflow and user interface but does not use real AI models. It is a foundation for later improvements.

v0.2

An improved prototype that builds on v0.1 by integrating the OpenAI API for more natural summarization and question answering in Urdu. The interface has been expanded into a chat-style design, with session history management (save, switch, delete) and dynamic analysis options. Summarization and Q&A are powered by GPT models, while chats continue to be saved in JSON format.

This branch highlights the shift from placeholders to real AI-powered responses. Future work includes database storage, offline/local model integration, and additional features such as file uploads and exporting chat histories.
