import streamlit as st
from datetime import datetime
import asyncio

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


async def chatbot_response(user_input):
    # Simulate async chatbot logic (replace with actual async logic if needed)
    await asyncio.sleep(2)  # Simulate processing delay
    return f"You said: {user_input}"


async def main():
    st.title("Persistent Chatbot")

    # Display chat history at the top
    st.write("## Chat History")
    for chat in st.session_state.chat_history:
        st.markdown(f"**You ({chat['timestamp']}):** {chat['user']}")
        st.markdown(f"**Bot:** {chat['bot']}")

    # Use a form to handle input submission
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Enter your question:", key="user_input")
        submit_button = st.form_submit_button("Send")

        if submit_button and user_input.strip():
            # Show loading spinner
            with st.spinner("Bot is thinking..."):
                response = await chatbot_response(user_input)

            # Add the query and response to chat history
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.chat_history.append(
                {"timestamp": timestamp, "user": user_input, "bot": response}
            )

            # Rerun the app immediately to reflect the updated chat history
            st.rerun()


if __name__ == "__main__":
    asyncio.run(main())
