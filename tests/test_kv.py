from skills.registry import registry
import skills.range_query_skills  # noqa: F401 — triggers @registry.register decorators
from skills.runtime import SkillRuntime
from agent.loop import agent_loop
from skills.range_query_skills import kv_user_prompt


def test_agent_performs_kv_range_query() -> None:
    runtime = SkillRuntime(registry)

    messages = [
        {"role": "user", "content": kv_user_prompt},
    ]

    result = agent_loop(registry, runtime, messages)

    assert isinstance(result, str)
    assert result.split("\n")[-1].strip() == "1,3,5,7,10"
