from langchain_core.messages import HumanMessage
from langgraph.constants import START, END
from langgraph.graph import StateGraph, MessagesState


class MyState(MessagesState):
    user_name: str
    user_age: int | None
    user_location: str | None


def geet_to_user(state: MyState):
    print(state)
    return {
        "messages": [
            {"role": "ai", "content": f"hello {state['user_name']}"}
        ]
    }


hello_graph = StateGraph(state_schema=MyState)

hello_graph.add_node(geet_to_user)
hello_graph.add_edge(START, "geet_to_user")

hello_graph.add_edge("geet_to_user", END)

hello_wf = hello_graph.compile()
resp = hello_wf.invoke({
    "messages": [HumanMessage("hi mock_ai")],
    "user_name": "jonas"
})

print(type(resp))
print(resp)
