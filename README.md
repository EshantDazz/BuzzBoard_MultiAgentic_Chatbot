# Persistent AI-Driven Chatbot with Multi-Agent Framework

This project showcases a persistent AI-driven chatbot with a multi-agent architecture designed to assist sales representatives and demand generation professionals. The chatbot integrates LangChain, Anthropic, and Groq models for dynamic, personalized responses based on vast datasets. It also features session-based state management for continuous and seamless interactions.

## Key Features

### Multi-Agent Framework
1. **Agent 1: Prospecting Agent**
   - Behavior: Acts as a data miner and lead generator.
   - Capabilities:
     - Identifies high-potential leads using JSON data.
     - Suggests businesses with unmet needs or growth potential.
     - Filters data based on industry, revenue, location, and other signals.

2. **Agent 2: Prospect Insights Agent**
   - Behavior: Functions as a business analyst or market researcher.
   - Capabilities:
     - Analyzes metrics like SEO scores, social media presence, and D-scores.
     - Performs SWOT analysis for prospects.
     - Recommends personalized engagement strategies.

3. **Agent 3: Communication Agent**
   - Behavior: Operates like a creative copywriter.
   - Capabilities:
     - Drafts personalized outreach content (emails, LinkedIn messages, scripts).
     - Adapts tone and content to align with industry and prospect needs.
     - Suggests communication timing and strategies.

### Session Persistence
- **State Management:** Uses Streamlit session state utilities to maintain chat history across interactions.
- **Dynamic Responses:** Each agent streams responses in real time, adapting based on user queries.

### Scalability and Tool Integration
- **Tools:** Leverages pre-built tools like `get_huge_corpus_for_all_companies`, `get_specific_company_details`, and `calculator` to augment agent capabilities.
- **Reframing Responses:** Agents intelligently refine responses to ensure concise and actionable output.

## Tech Stack

### Backend
- **LangChain Core:** For agent chaining, dynamic prompts, and structured response parsing.
- **Anthropic Claude-3.5:** For generating natural language responses and model interactions.
- **Groq LLAMA-3.3:** A versatile model used for supplementary LLM capabilities.

### Frontend
- **Streamlit:** Provides a simple, interactive user interface for chat interactions.

### Utilities
- **Python Dotenv:** For managing environment variables securely.
- **OpenPyxl:** For processing Excel-based datasets.

## Requirements

### Dependencies
Below is the list of required libraries specified in the `requirements.txt`:

```
langchain
langchain_openai
langchain_groq
python-dotenv
streamlit
openpyxl
```

Install these dependencies using pip:

```bash
pip install -r requirements.txt
```

## Setup and Installation

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables:**
   Create a `.env` file in the root directory and add your API keys or configuration variables.
   ```env
   ANTHROPIC_API_KEY=<your-anthropic-api-key>
   GROQ_API_KEY=<your-groq-api-key>
   ```

4. **Run the Application:**
   Start the Streamlit app:
   ```bash
   streamlit run main.py
   ```

## How It Works

### Chat Workflow
1. **User Input:** Users interact via the Streamlit interface, entering queries.
2. **Agent Selection:** The `return_agent_number` function dynamically selects the best-fit agent based on the query context.
3. **Agent Execution:**
   - The chosen agent processes the query, utilizing tools and JSON datasets.
   - The agent streams its response in real time.
4. **Reframed Output:** Responses are refined for clarity and precision before being presented to the user.
5. **Session History:** The chat history is maintained across interactions for a seamless experience.

### Tools Used
- **get_huge_corpus_for_all_companies:** Processes large JSON datasets.
- **get_specific_company_details:** Fetches detailed information about a specific company.
- **calculator:** Handles mathematical operations or calculations as required by the agents.
