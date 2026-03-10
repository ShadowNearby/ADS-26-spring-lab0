# Lab0 Warmup：用 AI Skill 在数据结构上实现更高层接口

## 1. 背景与目标

底层数据结构往往只暴露最基础的接口，但上层业务需要更复杂的能力。本 Lab 中，你将设计 prompt 和 function schema，让 LLM 通过多轮调用这些基础工具来完成更高层的任务。

## 2. 代码结构

```
agent/loop.py                 # Agent Loop：驱动 LLM ↔ 工具的多轮对话
skills/registry.py            # SkillRegistry：注册工具及其 JSON Schema
skills/runtime.py             # SkillRuntime：执行 tool_call 并返回结果
skills/graph_skills.py        # 图工具 neighbors（需补全）
skills/range_query_skills.py  # KV 工具 kv_get（需补全）
examples/example_graph.py     # 示例图数据
examples/example_kv.py        # 示例 KV 数据
tests/test_graph.py           # 图任务测试
tests/test_kv.py              # KV 任务测试
main.py                       # 入口：python main.py 或 pytest
```

## 3. 框架说明

框架由三个组件构成，建议阅读源码理解细节：

1. **SkillRegistry** (`skills/registry.py`)：通过 `@registry.register(name, description, parameters)` 装饰器注册工具函数，同时生成 OpenAI Tools 格式的 JSON Schema。
2. **SkillRuntime** (`skills/runtime.py`)：接收 LLM 发出的 `tool_call`，解析参数并执行对应的 Python 函数。
3. **agent_loop** (`agent/loop.py`)：循环调用 LLM → 若返回 `tool_calls` 则执行工具并将结果追加到对话 → 若无 `tool_calls` 则返回最终文本答案。

整体流程：

```
User Prompt → LLM → tool_calls? ─Yes→ SkillRuntime 执行 → 结果追加到对话 → 回到 LLM
                        │
                        No → 返回最终答案
```

## 4. 任务

你需要在两个 skill 文件中补全 **`user_prompt`**（任务提示）和 **`@registry.register`** 中的 `description` / `parameters`（工具描述与 JSON Schema）。

### 4.1 配置环境

- 获取 API key 在 `https://form.sjtu.edu.cn/infoplus/form/net_ai_api_apply/start?locale=zh`
- 在 agent/loop.py 中设置 API key: API_KEY
- 安装依赖: `uv sync && source .venv/bin/activate`

### 4.2 图任务：找到从 A 最远的节点

**需修改文件**：`skills/graph_skills.py`

底层数据（`examples/example_graph.py`）：

```python
example_graph = {
    "A": ["B", "C"],
    "B": ["C"],
    "C": ["A", "B", "E"],
    "D": ["E"],
    "E": ["C", "D", "F"],
    "F": ["E", "G"],
    "G": ["F"]
}
```

已有的工具函数：

```python
def neighbors(node: str) -> List[str]:
    return example_graph.get(node, [])
```

**你需要做的**：
1. 编写 `graph_user_prompt`，引导 LLM 从 `A` 出发，通过反复调用 `neighbors` 探索图，找到距离 A 最远的节点。
2. 补全 `@registry.register` 的 `description` 和 `parameters`。

**测试判定**（`tests/test_graph.py`）：取 LLM 输出最后一行，去除空白后应等于 `"G"`。

### 4.3 KV 任务：范围查询

**需修改文件**：`skills/range_query_skills.py`

底层数据（`examples/example_kv.py`）：

```python
example_kv_store = ExampleKeyValueStore({
    1: "apple",
    3: "banana",
    5: "cherry",
    7: "date",
    10: "elderberry",
})
```

已有的工具函数：

```python
def kv_get(key: int) -> Optional[str]:
    return example_kv_store.get(key)
```

**你需要做的**：
1. 编写 `kv_user_prompt`，引导 LLM 逐个调用 `kv_get` 检查区间 `[1, 10]` 内每个整数 key，收集返回非空值的 key，按升序拼成逗号分隔字符串。
2. 补全 `@registry.register` 的 `description` 和 `parameters`。

**测试判定**（`tests/test_kv.py`）：取 LLM 输出最后一行，去除空白后应等于 `"1,3,5,7,10"`。

> 提示：LLM 无法直接遍历 KV 存储，必须通过 prompt 引导它逐个调用 `kv_get` 来探测。

## 5. Lab要求

### 5.1 代码实现

- 阅读并理解 `SkillRegistry`、`SkillRuntime`、`agent_loop` 的实现。
- 补全 `skills/graph_skills.py` 和 `skills/range_query_skills.py` 中的 TODO 部分。
- 本地运行 `pytest` 确保两个测试通过。（由于LLM的不确定性，只要LLM能正确调用工具并给出正确答案，截图提交即可）

### 5.2 报告

在 `report.md` 报告中回答以下问题（详见 `docs/report_questions.md`）：

## 6. 评分与提交

### 评分标准

| 项目 | 占比 | 说明 |
|------|------|------|
| 通过测试 | 80% | 正确调用工具并给出正确答案 |
| 报告 | 20% | 设计思路、问题分析与反思 |

### 提交方式

- 运行 `./submit.sh <学号>` 生成 zip 文件提交代码及 `report.md`。
