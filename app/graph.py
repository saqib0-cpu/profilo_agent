"""
LangGraph agent powered by Google Gemini (free tier — no credit card needed).
Get a free key at https://aistudio.google.com/app/apikey

Agent loop:
1. Gemini decides whether to answer directly or call a tool
2. If it calls a tool, we run it and feed the result back as a function_response
3. Loop until Gemini gives a final text answer
"""

from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END
import operator
from google import genai
# pyrefly: ignore [missing-import]
from google.genai import types

from app.config import GEMINI_API_KEY, MODEL_NAME
from app.prompts import SYSTEM_PROMPT
from app.tools import TOOLS, TOOL_FUNCTIONS

client = genai.Client(api_key=GEMINI_API_KEY)


class AgentState(TypedDict):
    messages: Annotated[Sequence[dict], operator.add]


# ---------- helpers to convert between our dict format and genai types ----------

def _to_content(msg: dict) -> types.Content:
    parts = []
    for part in msg["parts"]:
        if "text" in part:
            parts.append(types.Part(text=part["text"]))
        elif "function_call" in part:
            fc = part["function_call"]
            p = types.Part(function_call=types.FunctionCall(name=fc["name"], args=fc["args"]))
            if "thought_signature" in part:
                p.thought_signature = part["thought_signature"]
            if "thought" in part:
                p.thought = part["thought"]
            parts.append(p)
        elif "function_response" in part:
            fr = part["function_response"]
            parts.append(types.Part(function_response=types.FunctionResponse(name=fr["name"], response=fr["response"])))
    return types.Content(role=msg["role"], parts=parts)


def _model_part_to_dict(part) -> dict:
    if part.text:
        return {"text": part.text}
    if part.function_call:
        d = {"function_call": {"name": part.function_call.name, "args": dict(part.function_call.args)}}
        if getattr(part, "thought_signature", None):
            d["thought_signature"] = part.thought_signature
        if getattr(part, "thought", None):
            d["thought"] = part.thought
        return d
    return {"text": ""}


# ---------- graph nodes ----------

def call_model(state: AgentState):
    contents = [_to_content(m) for m in state["messages"]]

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=TOOLS,
        ),
    )

    candidate_parts = response.candidates[0].content.parts
    new_parts = [_model_part_to_dict(p) for p in candidate_parts]

    return {"messages": [{"role": "model", "parts": new_parts}]}


def run_tools(state: AgentState):
    last_message = state["messages"][-1]
    response_parts = []

    for part in last_message["parts"]:
        if "function_call" in part:
            fc = part["function_call"]
            fn = TOOL_FUNCTIONS.get(fc["name"])
            result = fn(**fc["args"]) if fn else f"Unknown tool: {fc['name']}"
            response_parts.append({
                "function_response": {"name": fc["name"], "response": {"result": str(result)}}
            })

    return {"messages": [{"role": "user", "parts": response_parts}]}


def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message["role"] == "model":
        if any("function_call" in p for p in last_message["parts"]):
            return "tools"
    return END


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("agent", call_model)
    graph.add_node("tools", run_tools)

    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")

    return graph.compile()


agent_graph = build_graph()


def run_agent(user_message: str, history: list[dict] = None) -> tuple[str, list[dict]]:
    """Runs the agent on one user message given prior history. Returns (reply, updated_history)."""
    messages = (history or []) + [{"role": "user", "parts": [{"text": user_message}]}]
    result = agent_graph.invoke({"messages": messages})

    final_messages = result["messages"]
    final_reply = ""
    for part in final_messages[-1]["parts"]:
        if "text" in part:
            final_reply += part["text"]

    return final_reply, final_messages