"""
This module provides asynchronous functions to determine which agent should handle a given query and
to get streaming responses from different agents (Agent 1, Agent 2, Agent 3) after they invoke
various tools. These functions utilize Claude models (Anthropic) and a Llama model (Groq)
through LangChain.
"""

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
from langchain_core.messages import HumanMessage

from src.session_state_utils import get_chat_history

load_dotenv()

# Instantiate language models with desired parameters.
llm_claud = ChatAnthropic(
    model="claude-3-5-sonnet-20241022", temperature=0, max_retries=2
)
llm_claud_basic = ChatAnthropic(
    model="claude-3-5-haiku-20241022", temperature=0, max_retries=2
)
llm_llama = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, max_retries=3)

# Create a task allocation chain that produces a structured output (TaskAllocationResponse).
llm_task_allocation = llm_claud.with_structured_output(TaskAllocationResponse)
task_allocation_chain = task_allocator_prompt | llm_task_allocation


async def return_agent_number(query: str) -> int:
    """
    Determine which agent is most suitable for the given query.
    The function uses the `task_allocation_chain` to score and select the agent.

    Args:
        query (str): The user query or prompt.

    Returns:
        int: The integer representing the chosen agent number.
    """
    chat_history = get_chat_history()  # Retrieve the conversation history
    # Invoke the task allocation chain with the query and chat history
    agent_selected = task_allocation_chain.invoke(
        {"query": query, "chat_history": chat_history}
    ).score
    return agent_selected


async def return_agent1_response(query: str):
    """
    Use Agent 1 to process a given query asynchronously.
    Invokes relevant tools (if specified in the chain response) and streams the final output.

    Args:
        query (str): The user query or prompt.

    Yields:
        str: Chunks of the streaming response from Agent 1.
    """
    # Define the tools available to Agent 1
    tools = [
        get_huge_corpus_for_all_companies,
        get_specific_company_details,
        calculator,
    ]

    with st.spinner("Agent 1 is preparing your response..."):
        # Bind the tools to the Claude LLM
        llm_tools_agent_1 = llm_claud.bind_tools(tools)
        # Chain for Agent 1 to process the user query
        agent1_chain = agent1_prompt | llm_tools_agent_1
        chat_history = get_chat_history()
        # Get the initial answer (including any tool calls) from Agent 1
        answer = await agent1_chain.ainvoke(
            {"query": query, "chat_history": chat_history}
        )
        messages = []

        # If any tool is called by Agent 1, invoke those tools and accumulate their outputs
        if answer.tool_calls:
            messages.extend(chat_history)
            messages.append(HumanMessage(query))
            messages.append(answer)
            for tool_call in answer.tool_calls:
                selected_tool = {
                    "get_huge_corpus_for_all_companies": get_huge_corpus_for_all_companies,
                    "get_specific_company_details": get_specific_company_details,
                    "calculator": calculator,
                }[tool_call["name"].lower()]

                # Execute the tool and append its result
                tool_msg = await selected_tool.ainvoke(tool_call)
                messages.append(tool_msg)

            # After all tool calls, get the final response
            response = await llm_tools_agent_1.ainvoke(messages)
            response = response.content
        else:
            # If no tool calls are made, just use the answer as is
            response = answer.content

    # Reframe the response from Agent 1 and stream it
    with st.spinner("Your response from Agent 1 will be streaming"):
        reframe_chain = reframe_agent1_response | llm_claud | StrOutputParser()
        async for chunk in reframe_chain.astream(
            {"query": query, "response": response}
        ):
            yield chunk  # Yield each chunk of output as it is streamed


async def return_agent2_reponse(query: str):
    """
    Use Agent 2 to process a given query asynchronously.
    Invokes relevant tools (if specified in the chain response) and streams the final output.

    Args:
        query (str): The user query or prompt.

    Yields:
        str: Chunks of the streaming response from Agent 2.
    """
    # Define the tools available to Agent 2
    tools = [get_specific_company_details, calculator]

    with st.spinner("Agent 2 is preparing your response..."):
        # Bind the tools to the Claude LLM
        llm_tools_agent_2 = llm_claud.bind_tools(tools)
        # Chain for Agent 2 to process the user query
        agent2_chain = agent2_prompt | llm_tools_agent_2
        chat_history = get_chat_history()
        # Get the initial answer (including any tool calls) from Agent 2
        answer = await agent2_chain.ainvoke(
            {"query": query, "chat_history": chat_history}
        )
        messages = []

        # If any tool is called by Agent 2, invoke those tools and accumulate their outputs
        if answer.tool_calls:
            messages.extend(chat_history)
            messages.append(HumanMessage(query))
            messages.append(answer)
            for tool_call in answer.tool_calls:
                selected_tool = {
                    "get_specific_company_details": get_specific_company_details,
                    "calculator": calculator,
                }[tool_call["name"].lower()]

                # Execute the tool and append its result
                tool_msg = await selected_tool.ainvoke(tool_call)
                messages.append(tool_msg)

            # After all tool calls, get the final response
            response = await llm_tools_agent_2.ainvoke(messages)
            response = response.content
        else:
            # If no tool calls are made, just use the answer as is
            response = answer.content

    # Reframe the response from Agent 2 and stream it
    with st.spinner("Your response from Agent 2 will be streaming"):
        reframe_chain = reframe_agent2_response | llm_claud | StrOutputParser()
        async for chunk in reframe_chain.astream(
            {"query": query, "response": response}
        ):
            yield chunk  # Yield each chunk of output as it is streamed


async def return_agent3_reponse(query: str):
    """
    Use Agent 3 to process a given query asynchronously.
    Invokes relevant tools (if specified in the chain response) and streams the final output.

    Args:
        query (str): The user query or prompt.

    Yields:
        str: Chunks of the streaming response from Agent 3.
    """
    # Define the tools available to Agent 3
    tools = [get_specific_company_details]

    with st.spinner("Agent 3 is preparing your response..."):
        # Bind the tools to the Claude LLM
        llm_tools_agent_3 = llm_claud.bind_tools(tools)
        # Chain for Agent 3 to process the user query
        agent3_chain = agent3_prompt | llm_tools_agent_3
        chat_history = get_chat_history()
        # Get the initial answer (including any tool calls) from Agent 3
        answer = await agent3_chain.ainvoke(
            {"query": query, "chat_history": chat_history}
        )
        messages = []

        # If any tool is called by Agent 3, invoke those tools and accumulate their outputs
        if answer.tool_calls:
            print(answer)
            messages.extend(chat_history)
            messages.append(HumanMessage(query))
            messages.append(answer)
            for tool_call in answer.tool_calls:
                print(tool_call)
                selected_tool = {
                    "get_specific_company_details": get_specific_company_details
                }[tool_call["name"].lower()]

                # Execute the tool and append its result
                tool_msg = await selected_tool.ainvoke(tool_call)
                messages.append(tool_msg)

            # After all tool calls, get the final response
            response = await llm_tools_agent_3.ainvoke(messages)
            response = response.content
        else:
            # If no tool calls are made, just use the answer as is
            response = answer.content

    # Reframe the response from Agent 3 and stream it
    with st.spinner("Your response from Agent 3 will be streaming"):
        reframe_chain = reframe_agent3_response | llm_claud | StrOutputParser()
        async for chunk in reframe_chain.astream(
            {"query": query, "response": response}
        ):
            yield chunk  # Yield each chunk of output as it is streamed
