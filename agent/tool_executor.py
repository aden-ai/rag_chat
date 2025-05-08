# File: tool_executor.py
import json
from agent.tool_definitions import get_executive_orders_by_president

TOOLS = {
    "get_executive_orders_by_president": get_executive_orders_by_president
}

def execute_tool_call(tool_json: str):
    tool_call = json.loads(tool_json)
    fn_name = tool_call['name']
    args = tool_call['arguments']
    return TOOLS[fn_name](**args)
