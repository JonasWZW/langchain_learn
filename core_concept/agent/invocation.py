from dataclasses import dataclass
from typing import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, ModelResponse, wrap_model_call
from langchain.agents.middleware.types import ModelCallResult

from langchain.chat_models import init_chat_model

from dotenv import load_dotenv
import os

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolRuntime

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")

deepseek_v3 = init_chat_model(
    "deepseek-ai/DeepSeek-v3",
    model_provider="openai",
    base_url=BASE_URL,
    api_key=API_KEY,
    temperature=1
)


@dataclass
class UserContext:
    user_name: str
    user_age: int | None = None


@tool
def get_user_location(runtime: ToolRuntime[UserContext]) -> str:
    """获取用户的地址

    Returns:
        用户的地址
    """
    writer = runtime.stream_writer
    writer("进入工具调用函数")
    context = runtime.context
    # print(f"context {context}")
    writer("正在获取用户信息")
    # context MyContext(user_name='zhangsan', user_age=25)
    writer("正在查询用户地址")
    if context.user_name == "zhangsan":
        return "wuhan"
    elif context.user_name == "lisi":
        return "shanghai"
    else:
        return "China"


saver = InMemorySaver()
config = {"configurable": {"thread_id": "1"}}
deepseek_v3_agent = create_agent(
    model=deepseek_v3,
    checkpointer=saver,
    tools=[get_user_location]
)

# LangChain 的流式系统允许您将代理运行的实时反馈呈现给您的应用程序。

# updates
"""
resp1 = deepseek_v3_agent.stream({
    "messages": [
        SystemMessage("你是一个ai助手"),
        HumanMessage("我现在的地址是哪里？")
    ]
}, config=config, context=UserContext(user_name="jonas"), stream_mode="updates")

for chunk in resp1:
    for step, data in chunk.items():
        print(f"step: {step}")
        print(f"content: {data['messages'][-1].content_blocks}")
"""
# step: model
# content: [{'type': 'tool_call', 'name': 'get_user_location', 'args': {}, 'id': '019a8c89f2f710518060cbc4b59bc7f7'}]
# context UserContext(user_name='jonas', user_age=None)
# step: tools
# content: [{'type': 'text', 'text': 'China'}]
# step: model
# content: [{'type': 'text', 'text': '您当前的地址是中国。如果您需要更具体的位置信息，请提供更多上下文或确认是否需要进一步帮助。'}]


# custom
"""
resp2 = deepseek_v3_agent.stream({
    "messages": [
        SystemMessage("你是一个ai助手"),
        HumanMessage("我现在的地址是哪里？")
    ]
}, config=config, context=UserContext(user_name="jonas"), stream_mode="custom")
for chunk in resp2:
    print(chunk)
"""
# 进入工具调用函数
# 正在获取用户信息
# 正在查询用户地址


# ["custom", "updates"]
resp3 = deepseek_v3_agent.stream({
    "messages": [
        SystemMessage("你是一个ai助手"),
        HumanMessage("我现在的地址是哪里？")
    ]
}, config=config, context=UserContext(user_name="jonas"), stream_mode=["custom", "updates"])
for stream_mode, chunk in resp3:
    print(f"stream_mode: {stream_mode}")
    print(f"content: {chunk}")
# stream_mode: updates
# content: {'model': {'messages': [AIMessage(content='', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 15, 'prompt_tokens': 88, 'total_tokens': 103, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 0, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-ai/DeepSeek-v3', 'system_fingerprint': '', 'id': '019a8c8e713a2b20c3ebafb889f8639a', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--b9ee270d-4508-4400-97a4-797a8511950a-0', tool_calls=[{'name': 'get_user_location', 'args': {}, 'id': '019a8c8e76059bc884c22ce1fd7723d5', 'type': 'tool_call'}], usage_metadata={'input_tokens': 88, 'output_tokens': 15, 'total_tokens': 103, 'input_token_details': {}, 'output_token_details': {'reasoning': 0}})]}}
# stream_mode: custom
# content: 进入工具调用函数
# stream_mode: custom
# content: 正在获取用户信息
# stream_mode: custom
# content: 正在查询用户地址
# stream_mode: updates
# content: {'tools': {'messages': [ToolMessage(content='China', name='get_user_location', id='d3faef06-e220-4580-8b60-32847b6164e6', tool_call_id='019a8c8e76059bc884c22ce1fd7723d5')]}}
# stream_mode: updates
# content: {'model': {'messages': [AIMessage(content='您当前的地址显示为“China”。如果您需要更具体的信息，请告诉我。', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 17, 'prompt_tokens': 111, 'total_tokens': 128, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 0, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-ai/DeepSeek-v3', 'system_fingerprint': '', 'id': '019a8c8e76dafd985ee16a3b5e0603e7', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--7efa980e-eba9-4cf5-824f-f4cde17d91a4-0', usage_metadata={'input_tokens': 111, 'output_tokens': 17, 'total_tokens': 128, 'input_token_details': {}, 'output_token_details': {'reasoning': 0}})]}}
