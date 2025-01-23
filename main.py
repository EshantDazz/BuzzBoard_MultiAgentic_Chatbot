import streamlit as st
from datetime import datetime
import asyncio

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


async def chatbot_response_stream(user_input: str):
    """
    Simulates an async stream of tokens. Replace this with actual
    streaming logic (e.g., from an LLM or another async source).
    """
    # Example tokens (you'd replace this with real streaming content)
    tokens = [
        "Hello",
        ", ",
        "this",
        " ",
        "is",
        " ",
        "a",
        " ",
        "streaming",
        " ",
        "response!",
    ]

    for token in tokens:
        # Yield one token at a time
        yield token
        # Simulate a delay between tokens
        await asyncio.sleep(0.1)


async def main():
    st.title("Persistent Chatbot with Streaming")

    # Display chat history at the top with color-coded backgrounds
    st.write("## Chat History")
    for chat in st.session_state.chat_history:
        # User message in a dark-gray box with white text
        st.markdown(
            f"""
            <div style="background-color: #2f2f2f; color: #ffffff;
                        padding: 10px; margin-bottom: 5px; border-radius: 5px;">
                <strong>You ({chat['timestamp']}):</strong> {chat['user']}
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Bot message in a dark-blue box with white text
        st.markdown(
            f"""
            <div style="background-color: #1f3c56; color: #ffffff;
                        padding: 10px; margin-bottom: 15px; border-radius: 5px;">
                <strong>Bot:</strong> {chat['bot']}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Use a form to handle input submission
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Enter your question:", key="user_input")
        submit_button = st.form_submit_button("Send")

        if submit_button and user_input.strip():
            # We'll create a placeholder to display the streaming text
            bot_response_placeholder = st.empty()

            # Show a spinner while streaming
            with st.spinner("Bot is thinking..."):
                partial_response = ""
                # 3. Stream tokens from the async generator
                async for token in chatbot_response_stream(user_input):
                    partial_response += token
                    # Update the placeholder in real-time
                    bot_response_placeholder.markdown(
                        f"""
                        <div style="background-color: #1f3c56; color: #ffffff;
                                    padding: 10px; border-radius: 5px;">
                            <strong>Bot (in-progress):</strong> {partial_response}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                # Once streaming is done, store the final response in session state
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.chat_history.append(
                    {
                        "timestamp": timestamp,
                        "user": user_input,
                        "bot": partial_response,
                    }
                )

            # Rerun the app to display the updated history
            st.rerun()


if __name__ == "__main__":
    asyncio.run(main())
