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


@dataclass
class MyResponse:
    user_name: str
    user_location: str
    weather_condition: str


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
    response_format=MyResponse
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
# context MyContext(user_name='zhangsan', user_age=25)
# <class 'dict'>
# {'messages': [HumanMessage(content='外面的天气怎么样？', additional_kwargs={}, response_metadata={}, id='7f937ad2-1d05-4455-95c4-249eebd71aaf'), AIMessage(content='', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 13, 'prompt_tokens': 276, 'total_tokens': 289, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 0, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-ai/DeepSeek-V3', 'system_fingerprint': '', 'id': '019a881505575f2c26ca13c28739a64f', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--bda2fc0e-6008-40d9-b268-5a459bd50a7c-0', tool_calls=[{'name': 'get_user_location', 'args': {}, 'id': '019a88150ac0defceba312eb3dfea8a8', 'type': 'tool_call'}], usage_metadata={'input_tokens': 276, 'output_tokens': 13, 'total_tokens': 289, 'input_token_details': {}, 'output_token_details': {'reasoning': 0}}), ToolMessage(content='wuhan', name='get_user_location', id='9183e0dd-dabd-4afc-b25e-be1664fe0fe5', tool_call_id='019a88150ac0defceba312eb3dfea8a8'), AIMessage(content='', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 30, 'prompt_tokens': 300, 'total_tokens': 330, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 0, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-ai/DeepSeek-V3', 'system_fingerprint': '', 'id': '019a88150b7abd39e76eee37e5b8e7c5', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--c8b63657-08e5-4c35-b2ee-12b10b97073b-0', tool_calls=[{'name': 'get_weather', 'args': {'city': 'wuhan'}, 'id': '019a881516b4403148203013c83d71e9', 'type': 'tool_call'}], usage_metadata={'input_tokens': 300, 'output_tokens': 30, 'total_tokens': 330, 'input_token_details': {}, 'output_token_details': {'reasoning': 0}}), ToolMessage(content='sunny', name='get_weather', id='3e1d6ae5-ae74-48f2-a691-05beb2d97a87', tool_call_id='019a881516b4403148203013c83d71e9'), AIMessage(content='', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 29, 'prompt_tokens': 330, 'total_tokens': 359, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 0, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-ai/DeepSeek-V3', 'system_fingerprint': '', 'id': '019a881516ed6bd91d0f509700ef626b', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--734c81f1-bafc-4e1b-a5f2-4d8c526c80c0-0', tool_calls=[{'name': 'MyResponse', 'args': {'user_name': 'user', 'user_location': 'wuhan', 'weather_condition': 'sunny'}, 'id': '019a881521221f51fdafe74acbbfbd81', 'type': 'tool_call'}], usage_metadata={'input_tokens': 330, 'output_tokens': 29, 'total_tokens': 359, 'input_token_details': {}, 'output_token_details': {'reasoning': 0}}), ToolMessage(content="Returning structured response: MyResponse(user_name='user', user_location='wuhan', weather_condition='sunny')", name='MyResponse', id='d1392360-d615-4926-921b-85e5e6e7fec8', tool_call_id='019a881521221f51fdafe74acbbfbd81')], 'structured_response': MyResponse(user_name='user', user_location='wuhan', weather_condition='sunny')}
# Returning structured response: MyResponse(user_name='user', user_location='wuhan', weather_condition='sunny')


# user_name='user'
# 这里有错误，是因为 get_user_location(runtime: ToolRuntime[MyContext]) 对于llm是不可见的，大模型不知道
