# ReWOO Planner 详细介绍

## 一、简介

ReWOO 是 Reasoning Without Observation 的缩写，即“无观察推理”。它是一种把规划、工具执行和结果汇总拆开的 Agent Planner 架构。

ReAct 是每执行一步工具就观察一次，再决定下一步；而 ReWOO 会先生成完整的推理计划和工具调用占位符，然后再统一执行工具，最后由 Solver 汇总结果。

一句话理解：

```text
ReWOO Planner = 先完整规划工具调用，再批量执行，最后统一求解
```

---

## 二、核心流程

```text
用户目标 → Planner 生成计划和工具占位符 → Worker 执行工具 → Solver 汇总结果
```

典型结构：

```text
Plan: 我需要查询 A 和 B，再比较它们
E1: Search[A]
E2: Search[B]
Plan: 根据 E1 和 E2 做对比
Solver: 使用 E1、E2 的结果生成最终答案
```

---

## 三、架构图

```text
User Goal
   ↓
Planner
   ↓
Plan + Evidence Slots
   ↓
Worker Executor
   ↓
Evidence Results
   ↓
Solver
   ↓
Final Answer
```

---

## 四、核心组件

| 组件 | 作用 |
|------|------|
| Planner | 生成完整推理路径和工具调用占位符 |
| Evidence Slot | 工具调用的占位符，如 E1、E2 |
| Worker | 执行工具调用，填充 Evidence |
| Solver | 根据计划和 Evidence 生成最终答案 |
| Tool Registry | 提供可调用工具列表 |
| Result Store | 存储 E1、E2 等中间结果 |

---

## 五、计划格式

### 文本格式

```text
Plan: 需要查询 vLLM 的核心特性
E1: Search[vLLM PagedAttention continuous batching]
Plan: 需要查询 Ollama 的核心特性
E2: Search[Ollama local LLM runtime]
Plan: 对比 E1 和 E2，生成适用场景总结
```

### JSON 格式

```json
{
  "goal": "对比 vLLM 和 Ollama",
  "plans": [
    {
      "id": "E1",
      "tool": "web_search",
      "input": {
        "query": "vLLM PagedAttention continuous batching"
      },
      "purpose": "查询 vLLM 的核心特性"
    },
    {
      "id": "E2",
      "tool": "web_search",
      "input": {
        "query": "Ollama local LLM runtime"
      },
      "purpose": "查询 Ollama 的核心特性"
    }
  ],
  "solve_instruction": "根据 E1 和 E2 对比两者定位和适用场景"
}
```

---

## 六、ReWOO 的关键特点

### 1. 规划和观察解耦

Planner 在没有工具结果的情况下先生成完整计划。

### 2. 工具调用可以并行

多个 Evidence Slot 如果没有依赖，可以并行执行。

```text
E1 ┐
E2 ├→ Solver
E3 ┘
```

### 3. LLM 调用次数更少

相比 ReAct 每一步都要调用 LLM，ReWOO 通常只需要：

```text
Planner 一次 + Solver 一次
```

### 4. 成本更可控

适合工具调用数量明确、流程较稳定的任务。

---

## 七、适用场景

### 适合

- 多信息源查询
- 多 API 并行调用
- 研究报告资料收集
- 对比分析任务
- 成本敏感的 Agent 执行
- 工具结果相互依赖较弱的任务

### 不适合

- 每一步都需要根据观察动态调整的任务
- 工具结果不确定性很强的任务
- 需要复杂失败恢复的任务
- 高度交互式任务

---

## 八、优点

- 减少 LLM 调用次数
- 工具调用可以并行
- 成本更可控
- 计划结构清晰
- 适合批量信息获取

---

## 九、缺点

- 初始计划错误会影响整体结果
- 缺少中途动态反馈
- 工具失败时恢复不如 ReAct 灵活
- 对 Planner 一次性规划能力要求较高

---

## 十、伪代码

```python
def rewoo_agent(user_goal, llm, tools):
    plan = generate_rewoo_plan(user_goal, llm)
    evidence_results = {}

    for evidence in plan.evidence_slots:
        tool = tools[evidence.tool]
        result = tool.run(evidence.input)
        evidence_results[evidence.id] = result

    final_answer = solve_with_evidence(
        goal=user_goal,
        plan=plan,
        evidence=evidence_results,
        llm=llm
    )

    return final_answer
```

并行执行版本：

```python
def execute_evidence_slots_parallel(evidence_slots, tools):
    futures = []
    for evidence in evidence_slots:
        futures.append(run_async(tools[evidence.tool], evidence.input))
    return collect_results(futures)
```

---

## 十一、工程实现关键点

### 1. Evidence ID 必须稳定

所有工具调用结果都要有唯一 ID，例如：

```text
E1、E2、E3
```

Solver 依赖这些 ID 引用结果。

### 2. 工具调用之间要标明依赖

如果 E3 依赖 E1，应明确表示：

```json
{
  "id": "E3",
  "depends_on": ["E1"]
}
```

### 3. Worker 要做错误隔离

某个 Evidence 失败时，不应直接让整个任务崩溃，可以返回：

```json
{
  "id": "E2",
  "status": "failed",
  "error": "search timeout"
}
```

### 4. Solver 要感知缺失证据

如果部分 Evidence 失败，Solver 应说明限制，而不是编造结果。

---

## 十二、与其它 Planner 的区别

| 架构 | 区别 |
|------|------|
| ReAct | ReAct 每步观察反馈，ReWOO 先规划后统一执行 |
| Plan-and-Execute | ReWOO 更强调 Evidence Slot 和工具调用占位符 |
| LLMCompiler | LLMCompiler 更像任务图调度，ReWOO 更轻量 |
| Prompt-based | Prompt-based 不一定有工具调用结构 |
| Workflow-based | Workflow-based 流程预定义，ReWOO 动态生成工具计划 |

---

## 十三、总结

ReWOO Planner 适合“信息收集 + 汇总分析”类任务，尤其适合多个工具调用可以并行的场景。

它的核心价值是：

```text
减少多轮 LLM 调用，提高工具执行并行度，降低成本
```

如果任务需要高度动态反馈，优先使用 ReAct；如果任务可以提前规划工具调用，ReWOO 会更高效。
