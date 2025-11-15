# 接下来，构建一个实用的天气预报代理程序，以演示关键的生产概念：
# 详细的系统提示有助于改善代理行为
# 创建可与外部数据集成的工具
# 一致响应的模型配置
# 结构化输出， 结果可预测
# 用于类似聊天互动的对话记忆
# 创建并运行代理 ，创建一个功能齐全的代理
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolRuntime

from models import deepseek

system_prompt = """
你是一个天气预报专家，现在需要你协助用户，解决用户关于天气相关的问题。
"""


@tool(parse_docstring=True)
def get_weather(city: str) -> str:
    """获取城市的天气情况

    Args:
        city: 城市名称

    Returns:
        对应城市的天气情况
    """
    if city == "wuhan":
        return "sunny"
    elif city == "shanghai":
        return "cloud"
    else:
        return "rain"


@dataclass
class MyContext:
    user_name: str
    user_age: int


@tool
def get_user_location(runtime: ToolRuntime[MyContext]) -> str:
    """获取用户的地址

    Returns:
        用户的地址
    """
    context = runtime.context
    print(f"context {context}")
    # context MyContext(user_name='zhangsan', user_age=25)
    if context.user_name == "zhangsan":
        return "wuhan"
    elif context.user_name == "lisi":
        return "shanghai"
    else:
        return "China"


saver = InMemorySaver()

weather_agent = create_agent(
    model=deepseek,
    tools=[get_weather, get_user_location],
    system_prompt=system_prompt,
    context_schema=MyContext,
    name="weather_agent",
    checkpointer=saver,
)

config = {"configurable": {"thread_id": "1"}}

response1 = weather_agent.invoke(
    {"messages": [{"role": "user", "content": "外面的天气怎么样？"}]},
    config=config,
    context=MyContext(user_name="zhangsan", user_age=25)
)
print(type(response1))
print(response1)
print(response1["messages"][-1].content)
# <class 'dict'>
# {'messages': [HumanMessage(content='外面的天气怎么样？', additional_kwargs={}, response_metadata={}, id='6526784c-bac7-499e-bfb0-f8137f973148'), AIMessage(content='', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 15, 'prompt_tokens': 169, 'total_tokens': 184, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 0, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-ai/DeepSeek-V3', 'system_fingerprint': '', 'id': '019a88044d7f9aa046508e43988df09f', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--a9ece8f2-752d-4f16-9ea1-e5cbbc0ea54c-0', tool_calls=[{'name': 'get_user_location', 'args': {}, 'id': '019a88045a59ccfa78957efc98573c2b', 'type': 'tool_call'}], usage_metadata={'input_tokens': 169, 'output_tokens': 15, 'total_tokens': 184, 'input_token_details': {}, 'output_token_details': {'reasoning': 0}}), ToolMessage(content='wuhan', name='get_user_location', id='d96292a7-2205-41f3-b467-2416d86b4a60', tool_call_id='019a88045a59ccfa78957efc98573c2b'), AIMessage(content='', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 20, 'prompt_tokens': 193, 'total_tokens': 213, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 0, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-ai/DeepSeek-V3', 'system_fingerprint': '', 'id': '019a88045b1d4e3d478a0f2530f2d7b2', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--23919ae8-1fed-4c7c-9e21-fa062969ec0c-0', tool_calls=[{'name': 'get_weather', 'args': {'city': 'wuhan'}, 'id': '019a880461faaa261e99c3550f26b6e8', 'type': 'tool_call'}], usage_metadata={'input_tokens': 193, 'output_tokens': 20, 'total_tokens': 213, 'input_token_details': {}, 'output_token_details': {'reasoning': 0}}), ToolMessage(content='sunny', name='get_weather', id='6f30615f-27c4-4a2d-997c-875434558a58', tool_call_id='019a880461faaa261e99c3550f26b6e8'), AIMessage(content='武汉目前的天气是晴天。', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 6, 'prompt_tokens': 223, 'total_tokens': 229, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 0, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-ai/DeepSeek-V3', 'system_fingerprint': '', 'id': '019a880462cb9f14cb0a782146e7ccec', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--701b531a-c77f-4e68-bdbe-87e84ed6926f-0', usage_metadata={'input_tokens': 223, 'output_tokens': 6, 'total_tokens': 229, 'input_token_details': {}, 'output_token_details': {'reasoning': 0}})]}
# 武汉目前的天气是晴天。
