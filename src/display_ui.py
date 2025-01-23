import streamlit as st


async def display_score_message(score):
    if score == 1:
        st.info("Congrats the Prospecting Agent has been selected for you")
    elif score == 2:
        st.info("Congrats the Prospect Insights Agent has been selected for you")
    elif score == 3:
        st.info("Congrats the Communication Agent has been selected for you")
    else:
        st.warning("It seems like you have entered some input. Please try again")
