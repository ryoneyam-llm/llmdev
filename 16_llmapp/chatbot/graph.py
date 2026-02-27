import os
from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

# Stateクラスの定義
class State(TypedDict):
    messages: Annotated[list, add_messages]

def build_graph(model_name: str):
    """
    Web検索機能を持つチャットボットグラフを構築

    Args:
        model_name: 使用するOpenAIモデルの名前

    Returns:
        コンパイル済みのグラフ
    """
    # ツールの定義
    tool = TavilySearchResults(max_results=2)
    tools = [tool]

    # LLMの作成
    llm = ChatOpenAI(model=model_name, temperature=0.7)
    llm_with_tools = llm.bind_tools(tools)

    # チャットボットノードの定義
    def chatbot(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    # グラフの作成
    graph_builder = StateGraph(State)

    # ノードの追加
    graph_builder.add_node("chatbot", chatbot)
    tool_node = ToolNode(tools=tools)
    graph_builder.add_node("tools", tool_node)

    # エッジの追加
    graph_builder.add_conditional_edges(
        "chatbot",
        tools_condition,
    )
    graph_builder.add_edge("tools", "chatbot")
    graph_builder.set_entry_point("chatbot")

    # メモリの追加
    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)

    return graph

def stream_graph_updates(graph: StateGraph, user_input: str, thread_id: str = "1"):
    """
    グラフを実行してメッセージをストリーミング

    Args:
        graph: 実行するグラフ
        user_input: ユーザーの入力メッセージ
        thread_id: スレッドID（会話履歴の識別用）

    Returns:
        AIの最終応答テキスト
    """
    config = {"configurable": {"thread_id": thread_id}}

    # グラフを実行
    events = list(graph.stream(
        {"messages": [("user", user_input)]},
        config,
        stream_mode="values"
    ))

    # 最後のイベントからAIメッセージを取得
    if events:
        last_event = events[-1]
        messages = last_event.get("messages", [])
        if messages:
            # 最後のメッセージ（AIの応答）を返す
            return messages[-1].content

    return "応答を生成できませんでした。"
