# -*- coding:utf-8 -*-
import asyncio

from llms.llm import llm

# chunks = llm.stream("30字简单讲解机器学习的概念")
# for chunk in chunks:
#     print(chunk.text, end="|", flush=True)


# async def do():
#     # 异步流式调用，使用event
#     async for event in llm.astream_events("30字简单讲解机器学习的概念"):
#
#         # event: str
#         # Event names are of the format: `on_[runnable_type]_(start|stream|end)`.
#         """
#         [
#             {
#                 "data": {"input": "hello"},
#                 "event": "on_chain_start",
#                 "metadata": {},
#                 "name": "reverse",
#                 "tags": [],
#             },
#             {
#                 "data": {"chunk": "olleh"},
#                 "event": "on_chain_stream",
#                 "metadata": {},
#                 "name": "reverse",
#                 "tags": [],
#             },
#             {
#                 "data": {"output": "olleh"},
#                 "event": "on_chain_end",
#                 "metadata": {},
#                 "name": "reverse",
#                 "tags": [],
#             },
#         ]
#         """
#         if event["event"] == "on_chat_model_start":
#             print(f"Input: {event['data']['input']}")
#
#         elif event["event"] == "on_chat_model_stream":
#             print(f"Token: {event['data']['chunk'].text}")
#
#         elif event["event"] == "on_chat_model_end":
#             print(f"Full message: {event['data']['output'].text}")
#
#         else:
#             print(event)
#
#
# if __name__ == '__main__':
#     asyncio.run(do())

# outputs = llm.batch(["30字描述 什么是机器学习", "30字描述 什么是神经网络", "30字描述 什么是深度学习"])
outputs = llm.batch_as_completed(["30字描述 什么是机器学习", "30字描述 什么是神经网络", "30字描述 什么是深度学习"])
for output in outputs:
    print(output)
