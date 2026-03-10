from openai import OpenAI
from skills.registry import SkillRegistry
from skills.runtime import SkillRuntime

API_KEY = ""
BASE_URL = "https://models.sjtu.edu.cn/api/v1"
MODEL = "qwen3coder"
TEMPERATURE = 0

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

def agent_loop(registry: SkillRegistry, runtime: SkillRuntime, messages: list[dict]):

    tools = list(registry.schemas.values())

    while True:

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            temperature=TEMPERATURE,
        )

        msg = response.choices[0].message

        if not msg.tool_calls:
            return msg.content

        tool_call = msg.tool_calls[0]

        print(tool_call)

        result = runtime.run({
            "name": tool_call.function.name,
            "arguments": tool_call.function.arguments
        })

        messages.append(msg)

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })