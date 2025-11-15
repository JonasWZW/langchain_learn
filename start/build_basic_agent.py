from langchain.agents import create_agent
from langchain_core.tools import tool

from models import deepseek


@tool(parse_docstring=True)
def get_weather(city: str) -> str:
    """Get weather for a given city.

    Args:
        city: 城市名称

    Returns:
        天气情况的描述
    """
    return f"It's always sunny in {city}!"


agent = create_agent(
    model=deepseek,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
resp = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
print(type(resp))
print(resp)
