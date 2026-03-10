from skills.registry import registry
import skills.graph_skills  # noqa: F401 — triggers @registry.register decorators
from skills.runtime import SkillRuntime
from agent.loop import agent_loop
from skills.graph_skills import graph_user_prompt


def test_agent_finds_farthest_node_from_a() -> None:
    runtime = SkillRuntime(registry)

    messages = [
        {"role": "user", "content": graph_user_prompt},
    ]

    result = agent_loop(registry, runtime, messages)

    assert isinstance(result, str)
    assert result.split("\n")[-1].strip() == "G"

