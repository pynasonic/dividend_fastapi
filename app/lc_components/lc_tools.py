import os

from langchain.tools import tool
from typing import Dict, Any
from tavily import TavilyClient
from app.config import get_settings_singleton

# print(os.environ["TAVILY_API_KEY"])
tavily_client = TavilyClient()


# @tool("square_root")
@tool("square_root", description="Calculate the square root of a number")
def tool_math(x: float) -> float:
    return x ** 0.5



@tool("tavily", description="search online")
def tool_tavily(query: str) -> Dict[str, Any]:
    """Search the web for information"""
    return tavily_client.search(query)

