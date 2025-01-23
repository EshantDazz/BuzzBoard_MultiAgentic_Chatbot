import streamlit as st

import asyncio


from src.session_state_utils import (
    initialize_chat_history,
    get_chat_history,
    add_to_chat_history,
)
from src.display_ui import display_score_message
from src.ai_workflow import (
    return_agent1_response,
    return_agent2_reponse,
    return_agent3_reponse,
)
from langchain_core.messages import HumanMessage, AIMessage

from src.ai_workflow import return_agent_number


async def main():
    st.title("Persistent Chatbot with Streaming")

    # Initialize chat history
    initialize_chat_history()

    # Display chat history
    st.write("## Chat History")
    for i in range(0, len(get_chat_history()), 2):  # Iterate over pairs of messages
        human_message = get_chat_history()[i]
        ai_message = (
            get_chat_history()[i + 1] if i + 1 < len(get_chat_history()) else None
        )

        st.markdown(
            f"""
            <div style="background-color: #2f2f2f; color: #ffffff;
                        padding: 10px; margin-bottom: 5px; border-radius: 5px;">
                <strong>You:</strong> {human_message.content}
            </div>
            """,
            unsafe_allow_html=True,
        )

        if ai_message:
            st.markdown(
                f"""
                <div style="background-color: #1f3c56; color: #ffffff;
                            padding: 10px; margin-bottom: 15px; border-radius: 5px;">
                    <strong>Bot:</strong> {ai_message.content}
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Use a form to handle input
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Enter your question:", key="user_input")
        submit_button = st.form_submit_button("Send")

        if submit_button and user_input.strip():
            bot_response_placeholder = st.empty()
            with st.spinner(
                "Analyzing task requirements and assigning the best-fit agent…"
            ):
                agent_selected = await return_agent_number(user_input)
                print(f"Agent Selected: {agent_selected}")
                await display_score_message(agent_selected)

            if agent_selected == 1:
                partial_response = ""
                async for chunk in return_agent1_response(user_input):
                    partial_response += chunk
                    bot_response_placeholder.markdown(
                        f"""
                        <div style="background-color: #1f3c56; color: #ffffff;
                                    padding: 10px; border-radius: 5px;">
                            <strong>Eshant Bot (Agent 1 in-progress):</strong> {partial_response}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                add_to_chat_history(
                    HumanMessage(content=user_input),
                    AIMessage(content=partial_response),
                )
            elif agent_selected == 2:
                partial_response = ""
                async for chunk in return_agent2_reponse(user_input):
                    partial_response += chunk
                    bot_response_placeholder.markdown(
                        f"""
                        <div style="background-color: #1f3c56; color: #ffffff;
                                    padding: 10px; border-radius: 5px;">
                            <strong>Eshant Bot (Agent 2 in-progress):</strong> {partial_response}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                add_to_chat_history(
                    HumanMessage(content=user_input),
                    AIMessage(content=partial_response),
                )
            elif agent_selected == 3:
                partial_response = ""
                async for chunk in return_agent3_reponse(user_input):
                    partial_response += chunk
                    bot_response_placeholder.markdown(
                        f"""
                        <div style="background-color: #1f3c56; color: #ffffff;
                                    padding: 10px; border-radius: 5px;">
                            <strong>Eshant Bot (Agent 3 in-progress):</strong> {partial_response}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                add_to_chat_history(
                    HumanMessage(content=user_input),
                    AIMessage(content=partial_response),
                )

            else:
                st.warning(
                    "It looks like the input provided is not valid or relevant to the project. Could you please review and try again?"
                )
                await asyncio.sleep(5)

            # Rerun to update the UI
            st.rerun()


if __name__ == "__main__":
    asyncio.run(main())
