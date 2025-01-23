from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


task_allocator_system_prompt = """
You are a task allocator Agent. You will be given a query and based on that you need to understand which Agent will further work 
with your query. Your task is to understand the query carefully and decide which Agent will take over the task and move forward.
"""


task_allocator_user_prompt = """
Here is your query <query> " {query} " </query>
The descriptions and Options of the Agents you will be choosing are as below:

Agent 1: 
Prospecting Agent:
Role: Helps sales reps discover high-potential leads tailored to their preferences.
Capabilities:
Identifies new prospects based on industry, location, and key signals (e.g., SEO, local presence).
Uses BuzzBoard data to find businesses with unmet needs or growth potential.
Suggests prospects similar to high-performing customers in the CRM.
Example Query:

1. Find businesses in the Computer Contractors category with low local presence but high google ads spend.
2. Find businesses in the Computer Contractors category in Texas, with low local presence but high google ads spend.


Agent 2:
Prospect Insights Agent:
Role: Delivers deep analysis of selected prospects to aid decision-making.
Capabilities:
Analyzes BuzzBoard metrics like D-Score, SEO Score, and Social Media Presence.
Flags opportunities for improvement (e.g., missing local SEO, weak social strategy).
Performs SWOT analysis and provides a tailored value proposition for the prospect.
Recommends personalized engagement strategies based on insights.
Example Query:

"What are the strengths and weaknesses of ABC Plumbing?"


Agent 3: 
Communication Agent:
Role: Crafts personalized communication for effective prospect engagement.
Capabilities:
Drafts emails, LinkedIn messages, or scripts based on prospect data.
Adapts tone and content to align with the prospect’s industry and needs.
Offers pre-built templates for follow-ups, introductions, or negotiations.
Suggests communication timing based on the prospect's peak activity.
Example Query:

"Draft a personalized email for a xyz business and prose my product based on their needs”


Now you need to return me back a score:
if you think this task should be taken by Agent 1 then return score 1, if Agent 2 then return 2 and if Agent then return 3
If you thing the input is garbage string value or nuisance then return -1 
"""


task_allocator_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", task_allocator_system_prompt),
        MessagesPlaceholder("chat_history"),  # This allows passing in previous messages
        ("user", task_allocator_user_prompt),
    ]
)
