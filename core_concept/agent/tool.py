# 工具是agent对于llm的扩展，是llm的手和脚，帮助llm感知外部世界

from langchain.tools import tool
from langchain_core.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.types import Command


# 可以通过tool装饰器里面的参数，对工具进行描述。

@tool(parse_docstring=True)  # 使用google docstring 理解工具
def search_database(query: str, limit: int = 10) -> str:
    """Search the customer database for records matching the query.

    Args:
        query: Search terms to look for
        limit: Maximum number of results to return

    Returns
        str: result of search
    """
    return f"Found {limit} results for '{query}'"


print(search_database)

"""ToolRuntime 是langchain提供给我们，访问运行时信息

State - Mutable data that flows through execution (e.g., messages, counters, custom fields)

Context - Immutable configuration like user IDs, session details, or application-specific configuration
create_agent 的时候指定context_schema，然后调用的时候，传入context参数

@dataclass
class UserContext:
    user_id: str
agent = create_agent(
    model,
    tools=[get_account_info],
    context_schema=UserContext,
    system_prompt="You are a financial assistant."
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's my current balance?"}]},
    context=UserContext(user_id="user123")
)


Store - Persistent long-term memory across conversations

Stream Writer - Stream custom updates as tools execute

Config - RunnableConfig for the execution

Tool Call ID - ID of the current tool call
"""

from langchain.tools import tool, ToolRuntime
# @tool ，工具是agent很重要的东西。
# 访问ToolRuntime的各个属性
@tool
def summarize_conversation(
    runtime: ToolRuntime
) -> str:
    """Summarize the conversation so far."""
    messages = runtime.state["messages"]
    # runtime.state
    # runtime.context
    # runtime.store
    # runtime.stream_writer
    # runtime.context
    # runtime.tool_call_id
    human_msgs = sum(1 for m in messages if m.__class__.__name__ == "HumanMessage")
    ai_msgs = sum(1 for m in messages if m.__class__.__name__ == "AIMessage")
    tool_msgs = sum(1 for m in messages if m.__class__.__name__ == "ToolMessage")

    return f"Conversation has {human_msgs} user messages, {ai_msgs} AI responses, and {tool_msgs} tool results"

# 我们还可以通过@tool修改状态，Command这个对象
@tool
def clear_conversation() -> Command:
    """Clear the conversation history."""

    return Command(
        update={
            "messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES)],
        }
    )
