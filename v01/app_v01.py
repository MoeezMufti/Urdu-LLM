import streamlit as st
import json
import os
from datetime import datetime
import uuid

# Initialize session state
if 'current_chat_id' not in st.session_state:
    st.session_state.current_chat_id = str(uuid.uuid4())
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'chats' not in st.session_state:
    st.session_state.chats = {}

# File paths
CHATS_FILE = "chats_v02.json"

def load_chats():
    """Load all chats from file"""
    if os.path.exists(CHATS_FILE):
        try:
            with open(CHATS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_chats(chats_data):
    """Save all chats to file"""
    try:
        with open(CHATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(chats_data, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def simple_summarize(text):
    """Simple Urdu text summarization"""
    sentences = text.split('۔')
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) > 2:
        summary = '۔'.join(sentences[:2]) + '۔'
        return f"📄 **خلاصہ:** {summary}"
    return f"📄 **خلاصہ:** {text}"

def simple_qa(text, question):
    """Simple Q&A response"""
    return f"🤖 **جواب:** آپ کے سوال '{question}' کے بارے میں - یہ متن کی بنیاد پر جواب ہے۔ اصل متن میں موجود معلومات کے مطابق جواب فراہم کیا گیا ہے۔"

def delete_chat(chat_id):
    """Delete a specific chat"""
    all_chats = load_chats()
    if chat_id in all_chats:
        del all_chats[chat_id]
        save_chats(all_chats)
        
        # If we're deleting the current chat, create a new one
        if chat_id == st.session_state.current_chat_id:
            create_new_chat()
        else:
            st.rerun()

def create_new_chat():
    """Create a new chat session"""
    st.session_state.current_chat_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.rerun()

def switch_chat(chat_id):
    """Switch to an existing chat"""
    all_chats = load_chats()
    if chat_id in all_chats:
        st.session_state.current_chat_id = chat_id
        st.session_state.messages = all_chats[chat_id].get('messages', [])
        st.rerun()

def save_current_chat():
    """Save current chat to file"""
    if st.session_state.messages:  # Only save if there are messages
        all_chats = load_chats()
        
        # Create chat title from first user message
        title = "New Chat"
        for msg in st.session_state.messages:
            if msg['role'] == 'user':
                title = msg['content'][:50] + "..." if len(msg['content']) > 50 else msg['content']
                break
        
        all_chats[st.session_state.current_chat_id] = {
            'title': title,
            'timestamp': datetime.now().isoformat(),
            'messages': st.session_state.messages
        }
        
        save_chats(all_chats)

def add_message(role, content):
    """Add message to current chat"""
    st.session_state.messages.append({
        'role': role,
        'content': content,
        'timestamp': datetime.now().isoformat()
    })
    save_current_chat()

# Page config
st.set_page_config(
    page_title="Urdu Notebook v0.2",
    page_icon="🗨️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for ChatGPT-like styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
    }
    
    .user-message {
        background-color: #2c2c2c;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    
    .assistant-message {
        background-color: #1a1a1a;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #28a745;
        border: 1px solid #404040;
    }
    
    .chat-input-container {
        position: sticky;
        bottom: 0;
        background: white;
        padding: 1rem;
        border-top: 1px solid #e0e0e0;
    }
    
    .sidebar-chat-item {
        padding: 0.5rem;
        margin: 0.2rem 0;
        border-radius: 5px;
        cursor: pointer;
        border: 1px solid #e0e0e0;
    }
    
    .sidebar-chat-item:hover {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar - Chat History
with st.sidebar:
    st.markdown("### 🗨️ Urdu Notebook v0.2")
    
    # New Chat Button
    if st.button("➕ نئی بات چیت", use_container_width=True, type="primary"):
        create_new_chat()
    
    st.markdown("---")
    st.markdown("### 📚 محفوظ کردہ چیٹس")
    
    # Load and display chat history
    all_chats = load_chats()
    
    if all_chats:
        # Sort chats by timestamp (newest first)
        sorted_chats = sorted(all_chats.items(), 
                            key=lambda x: x[1].get('timestamp', ''), 
                            reverse=True)
        
        for chat_id, chat_data in sorted_chats:
            title = chat_data.get('title', 'Unnamed Chat')
            timestamp = chat_data.get('timestamp', '')
            
            # Format timestamp
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                time_str = dt.strftime("%m/%d %H:%M")
            except:
                time_str = ""
            
            # Create columns for chat item and delete button
            col1, col2 = st.columns([4, 1])
            
            with col1:
                # Create clickable chat item
                is_current = chat_id == st.session_state.current_chat_id
                
                if st.button(
                    f"💬 {title}\n📅 {time_str}",
                    key=f"chat_{chat_id}",
                    use_container_width=True,
                    disabled=is_current
                ):
                    switch_chat(chat_id)
            
            with col2:
                # Delete button for each chat
                if st.button("🗑️", key=f"del_{chat_id}", help="Delete this chat"):
                    delete_chat(chat_id)
        
        # Delete all chats button
        st.markdown("---")
        if st.button("🗑️ تمام چیٹس ڈیلیٹ کریں", use_container_width=True, type="secondary"):
            if st.button("⚠️ تصدیق کریں", key="confirm_delete_all", use_container_width=True):
                delete_all_chats()
    else:
        st.info("ابھی کوئی چیٹ محفوظ نہیں")
    
    st.markdown("---")
    st.markdown("### ℹ️ معلومات")
    st.markdown("- **v0.2**: ChatGPT Style Interface")
    st.markdown("- **v0.1**: Simple Form Interface")

# Main Chat Interface
st.markdown('<div class="main-header"><h1>🗨️ Urdu Notebook Assistant v0.2</h1><p><i>AI-Powered Urdu Summarizer & Q&A Chat</i></p></div>', unsafe_allow_html=True)

# Chat messages container
chat_container = st.container()

with chat_container:
    # Display chat messages
    if st.session_state.messages:
        for message in st.session_state.messages:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="user-message">
                    <strong>👤 آپ:</strong><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="assistant-message">
                    <strong>🤖 اسسٹنٹ:</strong><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
    else:
        # Welcome message for new chat
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #666;">
            <h3>🌟 خوش آمدید!</h3>
            <p>یہاں اردو متن پیسٹ کریں یا اپلوڈ کریں</p>
            <p>خلاصہ حاصل کریں یا سوالات پوچھیں</p>
        </div>
        """, unsafe_allow_html=True)

# Chat input section
st.markdown("---")

# Input options
input_type = st.radio("انپٹ کی قسم:", ["💬 Chat Message", "📄 Urdu Text for Analysis"], horizontal=True)

if input_type == "💬 Chat Message":
    # Regular chat input
    user_input = st.text_area(
        "یہاں اپنا پیغام لکھیں:",
        height=100,
        placeholder="سوال پوچھیں یا اردو متن کے بارے میں بات کریں..."
    )
    
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        if st.button("📤 بھیجیں", type="primary"):
            if user_input.strip():
                # Always ensure only one user message exists - either update or replace
                user_messages = [i for i, msg in enumerate(st.session_state.messages) if msg['role'] == 'user']
                
                if user_messages:
                    # Update the last user message
                    st.session_state.messages[user_messages[-1]]['content'] = user_input
                else:
                    # Add first user message
                    add_message("user", user_input)
                
                # Remove any existing assistant messages to avoid duplication
                st.session_state.messages = [msg for msg in st.session_state.messages if msg['role'] != 'assistant']
                
                # Add new assistant response
                response = f"🤖 آپ کے پیغام کا شکریہ! آپ نے کہا: '{user_input[:50]}...'"
                add_message("assistant", response)
                st.rerun()

else:  # Text Analysis
    # Text analysis input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        text_input = st.text_area(
            "اردو متن یہاں پیسٹ کریں:",
            height=150,
            placeholder="یہاں اردو ناول، کہانی یا کوئی بھی متن پیسٹ کریں..."
        )
    
    with col2:
        st.markdown("### 🎯 Actions")
        
        if st.button("📄 خلاصہ بنائیں", use_container_width=True):
            if text_input.strip():
                add_message("user", f"📝 **متن تجزیے کے لیے:**\n\n{text_input[:200]}...")
                summary = simple_summarize(text_input)
                add_message("assistant", summary)
                st.rerun()
            else:
                st.warning("پہلے متن داخل کریں!")
        
        if st.button("❓ سوال پوچھیں", use_container_width=True):
            if text_input.strip():
                # Show question input
                st.session_state.show_question_input = True
            else:
                st.warning("پہلے متن داخل کریں!")
    
    # Question input (shown when "Ask Question" is clicked)
    if getattr(st.session_state, 'show_question_input', False):
        st.markdown("### ❓ سوال پوچھیں")
        question = st.text_input("آپ کا سوال:", placeholder="مثال: اہم کردار کون ہے؟")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔍 جواب دیں"):
                if question.strip() and text_input.strip():
                    add_message("user", f"❓ **سوال:** {question}")
                    answer = simple_qa(text_input, question)
                    add_message("assistant", answer)
                    st.session_state.show_question_input = False
                    st.rerun()
        
        with col2:
            if st.button("❌ منسوخ"):
                st.session_state.show_question_input = False
                st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <small>🚀 <strong>Urdu Notebook Assistant v0.2</strong> | ChatGPT-Style Interface | Academic Prototype</small>
</div>
""", unsafe_allow_html=True)