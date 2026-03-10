from typing import List

from skills.registry import registry
from examples.example_graph import example_graph

graph_user_prompt = """
TODO: add user prompt
"""

@registry.register(
    name="neighbors",
    description="TODO: add description",
    parameters={
        "type": "object",
        "properties": {
            # TODO: add parameters
        },
        "required": []
    }
)
def neighbors(node: str) -> List[str]:
    return example_graph.get(node, [])