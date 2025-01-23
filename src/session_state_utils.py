import streamlit as st


def initialize_chat_history():
    """Initialize chat history in session state if it doesn't exist."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def get_chat_history():
    """Get the current chat history."""
    initialize_chat_history()
    return st.session_state.chat_history


def add_to_chat_history(human_message, ai_message):
    """Append a new message to the chat history."""
    initialize_chat_history()
    st.session_state.chat_history.append(human_message)
    st.session_state.chat_history.append(ai_message)


def update_chat_history(index, new_entry):
    """Update a specific chat message by index."""
    initialize_chat_history()
    if 0 <= index < len(st.session_state.chat_history):
        st.session_state.chat_history[index] = new_entry
    else:
        raise IndexError("Index out of range.")
