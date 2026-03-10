from typing import Optional

from skills.registry import registry
from examples.example_kv import example_kv_store


kv_user_prompt = """
TODO: add user prompt
"""

@registry.register(
    name="kv_get",
    description="TODO: add description",
    parameters={
        "type": "object",
        "properties": {
            # TODO: add parameters
        },
        "required": []
    }
)
def kv_get(key: int) -> Optional[str]:
    return example_kv_store.get(key)