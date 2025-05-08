import openai
import json
from agent.tool_executor import execute_tool_call

openai.api_base = "http://localhost:11434/v1"
openai.api_key = "ollama"  # dummy for local

async def process_query_with_agent(user_input: str):
    response = openai.ChatCompletion.create(
        model="qwen:0.5b",
        messages=[
            {"role": "system", "content": "You are a helpful assistant with access to tools."},
            {"role": "user", "content": user_input}
        ],
        functions=[
            {
                "name": "get_executive_orders_by_president",
                "description": "Fetch executive orders",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "president": {"type": "string"},
                        "month": {"type": "string"}
                    },
                    "required": ["president", "month"]
                }
            }
        ],
        function_call="auto"
    )

    msg = response['choices'][0]['message']

    if msg.get("function_call"):
        result = execute_tool_call(json.dumps(msg["function_call"]))
        final_response = openai.ChatCompletion.create(
            model="qwen:0.5b",
            messages=[
                {"role": "system", "content": "You are a helpful assistant with access to tools."},
                {"role": "user", "content": user_input},
                msg,
                {"role": "function", "name": msg['function_call']['name'], "content": result}
            ]
        )
        return final_response['choices'][0]['message']['content']

    return msg['content']
