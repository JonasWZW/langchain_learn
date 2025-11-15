# -*- coding:utf-8 -*-
from langchain.tools import tool
from langchain_core.messages import AIMessageChunk
from pydantic import BaseModel, Field

from llms.llm import llm


@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"It's sunny in {location}."


model_with_tools = llm.bind_tools([get_weather])

# response = model_with_tools.invoke("What's the weather like in Boston?")
#
# for tool_call in response.tool_calls:
#     # View tool calls made by the model
#     print(f"id: {tool_call['id']}")
#     # 通过name 达到关联，从而调用本地的tool，即 get_weather.invoke(**tool_call['args'])
#     print(f"Tool: {tool_call['name']}")
#     print(f"Args: {tool_call['args']}")
#     print(tool_call)
#
# resp = get_weather.invoke(tool_call)
# print(resp)
# print(type(resp))

"""
id: 019a863cd337a53a6bfd850d393c9b2d
Tool: get_weather
Args: {'location': 'Boston'}
{'name': 'get_weather', 'args': {'location': 'Boston'}, 'id': '019a863cd337a53a6bfd850d393c9b2d', 'type': 'tool_call'}
content="It's sunny in Boston." name='get_weather' tool_call_id='019a863cd337a53a6bfd850d393c9b2d'
<class 'langchain_core.messages.tool.ToolMessage'>
"""

# 流式调用，chunk __add__ 重载了
gathered = None
for chunk in model_with_tools.stream("What's the weather in Boston?"):
    gathered = chunk if gathered is None else gathered + chunk
    print(gathered.tool_calls)


llm.invoke()
