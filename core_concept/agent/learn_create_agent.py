"""
create_agent 使用 LangGraph 构建基于图的代理运行时。
图由节点（步骤）和边（连接）组成，定义了代理如何处理信息。
代理在这个图中移动，执行诸如模型节点（调用模型）、工具节点（执行工具）或中间件之类的节点。
他底层其实对langgraph的封装。并且统一了一个入口，化繁为简，统一使用。
"""
from typing import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, ModelResponse, wrap_model_call
from langchain.agents.middleware.types import ModelCallResult
# agent的三要素 model tool system-prompt 这三个都在中间件有增强


"""
1 model
静态model 就是创建agent的时候，就指定一个model，然后就一直使用该model
"""

from langchain.chat_models import init_chat_model

from dotenv import load_dotenv
import os

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")

deepseek = init_chat_model(
    "deepseek-ai/DeepSeek-R1",
    model_provider="openai",
    base_url=BASE_URL,
    api_key=API_KEY,
    temperature=1
)

v3 = init_chat_model(
    "deepseek-ai/DeepSeek-V3",
    model_provider="openai",
    base_url=BASE_URL,
    api_key=API_KEY,
    temperature=1
)


@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


# agent1 = create_agent(model=deepseek, tools=[get_weather_for_location])


# 动态模型，其实就是按需加载不同的模型使用，需要使用中间件技术，在调用模型前，替换模型。
# 具体的实现可以参考相应langchain包agent下的middleware
@wrap_model_call
def dynamic_chose_model_to_call(request: ModelRequest,
                                handler: Callable[[ModelRequest], ModelResponse],
                                ) -> ModelCallResult:
    msgs = request.messages
    print("wrap_model_call before")
    req = None
    if len(msgs) > 2:
        # override会生成一个新的request，但是我通过下一次调用 发现，request里面还是旧的，只是达到了长度条件，切换了
        req = request.override(model=deepseek)
        # request.model = deepseek
    else:
        req = request
    ans = handler(req)
    # ans = handler(request)
    print("wrap_model_call after")
    return ans


saver = InMemorySaver()
config = {"configurable": {"thread_id": "jonas"}}
dynamit_agent = create_agent(
    model=v3,  # Default model
    middleware=[dynamic_chose_model_to_call],
    checkpointer=saver,
)

resp1 = dynamit_agent.invoke({
    "messages": [
        SystemMessage("你是一个ai助手"),
        HumanMessage("你是什么模型名称的llm？ 类似gpt deepseek 30字说明")
    ]
}, config=config)

print(resp1)

resp2 = dynamit_agent.invoke({
    "messages": [
        HumanMessage("30字说明 你是什么模型名称的llm？ 类似gpt deepseek ")
    ]
}, config=config)

print(resp2)

resp3 = dynamit_agent.invoke({
    "messages": [
        HumanMessage("你最喜欢做什么？")
    ]
}, config=config)
print(resp3)




"""
2 tool
可以使用@wrap_tool_call 包装tool
"""




"""
3 system prompt
可以使用@dynamic_prompt 包装tool
"""