import logging
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

from state import AgentState
from tools.scheme_tools import check_eligibility, get_scheme_details

load_dotenv()

# Suppress Logs
logging.getLogger("httpx").setLevel(logging.WARNING)

# 1. Setup Tools
tools = [check_eligibility, get_scheme_details]

# 2. Setup Model (Groq - Free & Fast)
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)
llm_with_tools = llm.bind_tools(tools)

# 3. System Prompt (The Persona)
SYSTEM_PROMPT = """
You are 'Telangana Bandhu', a government service agent.
1. YOU MUST SPEAK ONLY IN TELUGU (Telugu Script).
2. Your goal is to help citizens check eligibility for schemes.
3. Ask for 'Age', 'Occupation', and 'Land' if missing.
4. Keep answers short (2-3 sentences) for voice output.
"""

# 4. Define Logic Nodes
def assistant(state: AgentState):
    messages = state.messages
    # Inject System Prompt if missing
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# 5. Build Graph
builder = StateGraph(AgentState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

agent_graph = builder.compile(checkpointer=InMemorySaver())