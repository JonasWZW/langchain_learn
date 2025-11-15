# -*- coding:utf-8 -*-
import asyncio

from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from llms.llm import llm


# 1. 定义带有 stream_writer 的工具
@tool
def get_weather(city: str, runtime: ToolRuntime) -> str:
    """Get weather for a given city."""
    # 获取 stream_writer
    writer = runtime.stream_writer

    # 使用 writer "直播" 工具的内部进度
    writer(f"正在连接天气服务器...")
    # 模拟网络延迟
    asyncio.run(asyncio.sleep(1))

    writer(f"成功连接，正在查询城市: {city}")
    asyncio.run(asyncio.sleep(1))

    writer(f"已获取 {city} 的天气数据！")
    asyncio.run(asyncio.sleep(0.5))

    # 返回最终结果
    return f"在 {city}，天气总是晴朗的！"


# 2. 创建 Agent
tools = [get_weather]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="You are a helpful assistant.",
)


# 3. 使用 astream_events 捕获所有事件，包括来自 stream_writer 的事件
async def main():
    async for event in agent.astream_events(
            {"messages": [{"role": "user", "content": "请问北京的天气怎么样？"}]}, stream_mode="custom"
    ):
        kind = event["event"]
        # print(event["event"])
        # print(event["data"])

        # 当有 LLM 的 token 输出时，打印出来
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                print(f"🤖 LLM: {content}", flush=True)

        # 当工具开始或结束时，打印提示
        elif kind == "on_tool_start":
            print(f"\n--- 🛠️ 调用工具: {event['name']} ({event['data'].get('input')}) ---")
        elif kind == "on_tool_end":
            print(f"--- ✅ 工具结束: {event['name']} (输出: {event['data'].get('output')}) ---\n")

        # 关键！捕获来自 stream_writer 的事件
        elif kind == "on_tool_stream":
            # event['data']['chunk'] 就是 writer.write() 写入的内容
            chunk = event["data"]["chunk"]
            print(f"   ⚙️ 工具进度: {chunk}", flush=True)


# 运行主函数
asyncio.run(main())
