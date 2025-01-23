from langchain_anthropic import ChatAnthropic
import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from core.prompts.task_allocator import task_allocator_prompt
from core.pydantic_structured_response_classes.task_allocator_pd import (
    TaskAllocationResponse,
)
from core.tools.agent_tools import (
    get_huge_corpus_for_all_companies,
    get_specific_company_details,
    calculator,
)
from core.prompts.agent1 import agent1_prompt, reframe_agent1_response
from core.prompts.agent2 import agent2_prompt, reframe_agent2_response
from core.prompts.agent3 import agent3_prompt, reframe_agent3_response
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from src.session_state_utils import (
    initialize_chat_history,
    get_chat_history,
    update_chat_history,
)

load_dotenv()


llm_claud = ChatAnthropic(
    model="claude-3-5-sonnet-20241022", temperature=0, max_retries=2
)
llm_claud_basic = ChatAnthropic(
    model="claude-3-5-haiku-20241022", temperature=0, max_retries=2
)
llm_llama = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, max_retries=3)

llm_task_allocation = llm_claud.with_structured_output(TaskAllocationResponse)
task_allocation_chain = task_allocator_prompt | llm_task_allocation


async def return_agent_number(query):
    chat_history = get_chat_history()
    agent_selected = (
        task_allocation_chain.invoke({"query": query, "chat_history": chat_history})
    ).score
    return agent_selected


async def return_agent1_response(query):
    tools = [
        get_huge_corpus_for_all_companies,
        get_specific_company_details,
        calculator,
    ]
    with st.spinner("Agent 1 is preparing your response..."):
        llm_tools_agent_1 = llm_claud.bind_tools(tools)
        agent1_chain = agent1_prompt | llm_tools_agent_1
        chat_history = get_chat_history()
        answer = await agent1_chain.ainvoke(
            {"query": query, "chat_history": chat_history}
        )
        if answer.tool_calls:
            messages = [HumanMessage(query)]
            messages.append(answer)
            for tool_call in answer.tool_calls:
                selected_tool = {
                    "get_huge_corpus_for_all_companies": get_huge_corpus_for_all_companies,
                    "get_specific_company_details": get_specific_company_details,
                    "calculator": calculator,
                }[tool_call["name"].lower()]

                tool_msg = await selected_tool.ainvoke(tool_call)

                messages.append(tool_msg)

            response = await llm_tools_agent_1.ainvoke(messages)
            response = response.content
        with st.spinner("Your response from Agent 1 will be streaming"):
            reframe_chain = reframe_agent1_response | llm_claud | StrOutputParser()
            async for chunk in reframe_chain.astream(
                {"query": query, "response": response}
            ):
                yield chunk  # Yield each chunk of output as it is streamed
    return


async def return_agent2_reponse(query):
    tools = [get_specific_company_details, calculator]
    with st.spinner("Agent 2 is preparing your response..."):
        llm_tools_agent_2 = llm_claud.bind_tools(tools)
        agent2_chain = agent1_prompt | llm_tools_agent_2
        chat_history = get_chat_history()
        answer = await agent2_chain.ainvoke(
            {"query": query, "chat_history": chat_history}
        )

        if answer.tool_calls:
            messages = [HumanMessage(query)]
            messages.append(answer)
            for tool_call in answer.tool_calls:
                selected_tool = {
                    "get_specific_company_details": get_specific_company_details,
                    "calculator": calculator,
                }[tool_call["name"].lower()]

                tool_msg = await selected_tool.ainvoke(tool_call)

                messages.append(tool_msg)
            response = await llm_tools_agent_2.ainvoke(messages)
            response = response.content
        with st.spinner("Your response from Agent 2 will be streaming"):
            reframe_chain = reframe_agent2_response | llm_claud | StrOutputParser()
            async for chunk in reframe_chain.astream(
                {"query": query, "response": response}
            ):
                yield chunk  # Yield each chunk of output as it is streamed
    return


async def return_agent3_reponse(query):
    tools = [get_specific_company_details]
    with st.spinner("Agent 3 is preparing your response..."):
        llm_tools_agent_3 = llm_claud.bind_tools(tools)
        agent3_chain = agent3_prompt | llm_tools_agent_3

        chat_history = get_chat_history()
        answer = await agent3_chain.ainvoke(
            {"query": query, "chat_history": chat_history}
        )

        if answer.tool_calls:
            print(answer)
            messages = [HumanMessage(query)]
            messages.append(answer)
            for tool_call in answer.tool_calls:
                print(tool_call)
                selected_tool = {
                    "get_specific_company_details": get_specific_company_details
                }[tool_call["name"].lower()]

                tool_msg = await selected_tool.ainvoke(tool_call)

                messages.append(tool_msg)
            response = await llm_tools_agent_3.ainvoke(messages)
            response = response.content

    with st.spinner("Your response from Agent 3 will be streaming"):
        reframe_chain = reframe_agent3_response | llm_claud | StrOutputParser()
        async for chunk in reframe_chain.astream(
            {"query": query, "response": response}
        ):
            yield chunk  # Yield each chunk of output as it is streamed
    return
