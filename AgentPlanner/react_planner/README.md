# ReAct Planner 详细介绍

## 一、简介

ReAct Planner 是 Agent Planner 中最经典、最常用的一类架构。ReAct 来自两个词：

```text
Reasoning + Acting = ReAct
```

它的核心思想是让 LLM 不只是一次性生成答案，而是在执行任务时不断循环：

```text
思考下一步 → 调用工具 → 观察结果 → 再思考 → 再行动 → 最终回答
```

ReAct Planner 非常适合需要外部工具参与的 Agent 场景，例如搜索、数据库查询、代码执行、文件读取、RAG 检索、API 调用等。

---

## 二、核心流程

ReAct 的标准循环可以表示为：

```text
Thought → Action → Observation → Thought → Action → Observation → Final Answer
```

### 1. Thought

LLM 根据当前目标、历史上下文和观察结果，推理下一步应该做什么。

示例：

```text
Thought: 用户想知道某个技术的最新进展，我需要先搜索相关资料。
```

### 2. Action

LLM 选择一个工具，并生成工具调用参数。

示例：

```text
Action: web_search
Action Input: {"query": "ReAct agent planner architecture"}
```

### 3. Observation

工具执行后返回结果，作为下一轮推理的输入。

示例：

```text
Observation: 搜索结果显示 ReAct 是一种结合推理和行动的 Agent 方法。
```

### 4. Final Answer

当 Planner 判断信息足够、目标完成时，生成最终答案。

示例：

```text
Final Answer: ReAct Planner 是一种让 Agent 在思考、行动和观察之间循环的规划架构。
```

---

## 三、架构图

```text
User Goal
   ↓
LLM Planner
   ↓
Thought
   ↓
Action Selection
   ↓
Tool Executor
   ↓
Observation
   ↓
State / Memory Update
   ↓
LLM Planner
   ↓
Final Answer
```

更完整的工程结构：

```text
┌──────────────────┐
│    User Input     │
└─────────┬────────┘
          ↓
┌──────────────────┐
│   Prompt Builder  │
└─────────┬────────┘
          ↓
┌──────────────────┐
│    LLM Planner    │
│ Thought / Action  │
└─────────┬────────┘
          ↓
┌──────────────────┐
│   Action Parser   │
└─────────┬────────┘
          ↓
┌──────────────────┐
│  Tool Executor    │
└─────────┬────────┘
          ↓
┌──────────────────┐
│   Observation     │
└─────────┬────────┘
          ↓
┌──────────────────┐
│ State / Memory    │
└─────────┬────────┘
          ↓
┌──────────────────┐
│ Stop Condition    │
└──────────────────┘
```

---

## 四、ReAct Planner 的核心组件

### 1. LLM Planner

负责生成 Thought 和 Action。

输入通常包括：

- 用户目标
- 系统约束
- 可用工具列表
- 历史 Thought / Action / Observation
- 当前任务状态

输出通常包括：

- 下一步思考
- 工具名称
- 工具参数
- 是否生成最终答案

---

### 2. Tool Registry

Tool Registry 是工具注册表，告诉 Planner 当前有哪些工具可用。

每个工具应该包含：

| 字段 | 说明 |
|------|------|
| name | 工具名称 |
| description | 工具功能描述 |
| input_schema | 输入参数结构 |
| output_schema | 输出结构 |
| permission | 权限要求 |
| timeout | 超时时间 |
| cost | 调用成本 |

示例：

```json
{
  "name": "web_search",
  "description": "搜索互联网信息",
  "input_schema": {
    "query": "string"
  },
  "output_schema": {
    "results": "array"
  }
}
```

---

### 3. Action Parser

Action Parser 负责把 LLM 输出解析成可执行的工具调用。

常见解析方式：

- 正则解析
- JSON 解析
- Function Calling
- XML / YAML 解析
- DSL 解析

推荐使用结构化输出：

```json
{
  "thought": "我需要查询相关资料",
  "action": "web_search",
  "action_input": {
    "query": "ReAct Planner"
  }
}
```

---

### 4. Tool Executor

Tool Executor 负责实际执行工具调用。

它需要处理：

- 参数校验
- 权限校验
- 超时控制
- 错误捕获
- 结果格式化
- 日志记录

---

### 5. Observation Manager

Observation Manager 负责把工具结果转成 LLM 可以理解的观察信息。

好的 Observation 应该：

- 简洁
- 结构化
- 保留关键信息
- 避免无关噪声
- 必要时做摘要压缩

---

### 6. State / Memory Manager

负责保存 ReAct 循环过程中的状态。

常见状态包括：

- 用户目标
- 当前步骤数
- 已调用工具
- 工具返回结果
- 中间结论
- 错误信息
- 已完成任务

---

### 7. Stop Controller

负责判断是否停止循环。

常见停止条件：

- LLM 输出 Final Answer
- 达到最大步骤数
- 达到最大工具调用次数
- 连续多次工具失败
- 结果置信度足够
- 用户目标已经满足
- 出现安全风险

---

## 五、Prompt 设计

### 基础 Prompt 模板

```text
你是一个可以使用工具的智能 Agent。

你的任务是完成用户目标。

你可以使用以下工具：
{tools}

你必须按照以下格式输出：

Thought: 你对当前任务的思考
Action: 要调用的工具名称，或者 Final Answer
Action Input: 工具输入参数
Observation: 工具返回结果由系统提供

当你认为任务已经完成时，输出：
Final Answer: 最终答案

用户目标：
{user_input}

历史步骤：
{history}
```

### 结构化 Prompt 模板

更推荐在工程中使用 JSON 输出：

```text
你是一个 ReAct Planner。

请根据用户目标、可用工具和历史观察，决定下一步动作。

输出必须是 JSON：
{
  "thought": "你的思考",
  "action": "工具名称或 final_answer",
  "action_input": {},
  "final_answer": "如果 action 是 final_answer，则填写最终答案"
}

可用工具：
{tools}

用户目标：
{user_input}

历史记录：
{history}
```

---

## 六、执行示例

### 用户目标

```text
帮我查一下 vLLM 和 Ollama 的区别，并总结适合场景。
```

### 第 1 轮

```text
Thought: 我需要先了解 vLLM 的定位和特点。
Action: web_search
Action Input: {"query": "vLLM high throughput LLM serving PagedAttention"}
```

```text
Observation: vLLM 是高吞吐 LLM 推理服务框架，核心技术包括 PagedAttention 和连续批处理。
```

### 第 2 轮

```text
Thought: 我还需要了解 Ollama 的定位。
Action: web_search
Action Input: {"query": "Ollama local LLM runtime"}
```

```text
Observation: Ollama 是本地大模型运行工具，支持模型下载、运行和本地 API。
```

### 第 3 轮

```text
Thought: 现在信息足够，可以总结两者区别。
Final Answer: vLLM 适合服务端高并发推理，Ollama 适合个人电脑本地运行和开发集成。
```

---

## 七、伪代码实现

```python
def react_agent(user_input, tools, llm, max_steps=8):
    history = []

    for step in range(max_steps):
        prompt = build_prompt(user_input=user_input, tools=tools, history=history)
        planner_output = llm.generate(prompt)
        action = parse_action(planner_output)

        if action.name == "final_answer":
            return action.final_answer

        tool = tools.get(action.name)
        if tool is None:
            observation = f"工具不存在：{action.name}"
        else:
            try:
                result = tool.run(action.input)
                observation = format_observation(result)
            except Exception as e:
                observation = f"工具执行失败：{str(e)}"

        history.append({
            "thought": action.thought,
            "action": action.name,
            "action_input": action.input,
            "observation": observation
        })

    return summarize_unfinished_result(history)
```

---

## 八、工程实现细节

### 1. 输出格式要强约束

ReAct 早期常用自然语言格式：

```text
Thought:
Action:
Action Input:
```

但生产环境更推荐 JSON 或 Function Calling，因为更容易解析和校验。

### 2. 工具要做白名单限制

Planner 只能调用注册过的工具，不能让模型自由生成任意命令。

```text
允许：search、retrieve、calculator、database_query
禁止：rm、delete_all、exec_raw_shell
```

### 3. 工具结果要压缩

工具返回结果可能很长，如果全部放入上下文，会导致 token 膨胀。

常见处理方式：

- 只保留 top-k 结果
- 对结果做摘要
- 保留结构化字段
- 丢弃无关内容

### 4. 防止无限循环

必须设置：

- 最大循环次数
- 最大工具调用次数
- 最大连续失败次数
- 重复 action 检测
- 任务完成判断

### 5. 增加失败恢复策略

常见失败包括：

| 失败类型 | 恢复方式 |
|----------|----------|
| 工具不存在 | 提醒 Planner 只能使用工具列表中的工具 |
| 参数错误 | 返回 schema 错误，让 Planner 修正参数 |
| 查询无结果 | 让 Planner 改写 query |
| 工具超时 | 重试或换工具 |
| 结果不足 | 继续调用补充工具 |

### 6. 加入 Evaluator

ReAct 默认依赖 LLM 自己判断是否完成，但生产环境可以加入 Evaluator：

```text
Planner → Tool → Observation → Evaluator → Continue / Stop / Replan
```

Evaluator 可以判断：

- 是否回答了用户问题
- 是否有证据支撑
- 是否存在幻觉
- 是否需要继续查询
- 是否触发安全风险

---

## 九、适合 ReAct 的任务

### 适合

- 搜索增强问答
- RAG Agent
- 数据库查询 Agent
- 代码解释和调试 Agent
- API 调用 Agent
- 多工具辅助任务
- 需要根据观察结果调整下一步的任务

### 不太适合

- 完全固定流程的企业任务
- 强安全约束的高风险动作
- 超长周期任务
- 需要大规模并行执行的任务
- 对延迟极度敏感的任务

---

## 十、ReAct 与其他 Planner 的区别

| 架构 | 与 ReAct 的区别 |
|------|-----------------|
| Prompt-based | 只生成计划，不根据工具结果动态调整 |
| Plan-and-Execute | 先生成完整计划，ReAct 是边执行边规划 |
| ReWOO | 先规划工具调用占位符，ReAct 每步都观察反馈 |
| LLMCompiler | 编译成任务图，ReAct 是线性循环执行 |
| Reflexion | 更强调执行后的反思记忆，ReAct 更强调实时观察 |
| Workflow-based | 工作流更可控，ReAct 更灵活 |
| Multi-Agent | 多 Agent 强调角色协作，ReAct 可作为单个 Agent 的内部循环 |

---

## 十一、常见问题

### 1. ReAct 为什么容易循环？

因为 LLM 可能不断认为信息还不够，或者重复调用相同工具。解决方式：

- 限制最大步数
- 检测重复 action
- 加入完成度评估
- 要求模型说明继续调用工具的必要性

### 2. ReAct 为什么会工具调用错误？

常见原因：

- 工具描述不清楚
- 参数 schema 不明确
- Prompt 没有限定工具列表
- LLM 输出格式不稳定

解决方式：

- 使用 JSON Schema
- 使用 Function Calling
- 工具描述写清输入输出
- 对参数做校验并返回错误信息

### 3. ReAct 如何和 RAG 结合？

RAG 中的检索器可以作为一个工具：

```text
Action: retrieve_documents
Action Input: {"query": "用户问题"}
Observation: 返回相关文档片段
```

然后 Planner 根据检索结果决定：

- 是否继续检索
- 是否改写 query
- 是否调用 rerank
- 是否生成最终答案

### 4. ReAct 如何做生产化？

生产化需要补充：

- 工具白名单
- 参数校验
- 超时控制
- 日志追踪
- 状态持久化
- 权限控制
- 人工确认
- 监控告警
- 成本控制

---

## 十二、推荐实现路线

### 第一步：最小 ReAct Agent

实现：

```text
用户输入 → LLM 输出 Thought / Action → 手动模拟 Observation → 最终答案
```

### 第二步：接入真实工具

建议先接入：

- calculator
- search
- retrieve_documents
- read_file

### 第三步：结构化输出

把自然语言格式改为 JSON：

```json
{
  "thought": "...",
  "action": "...",
  "action_input": {},
  "final_answer": "..."
}
```

### 第四步：增加状态管理

记录：

- step
- thought
- action
- observation
- token cost
- error

### 第五步：增加 Evaluator 和 Guardrails

让系统具备：

- 完成度判断
- 安全限制
- 失败恢复
- 人工确认

---

## 十三、总结

ReAct Planner 是理解 Agent Planner 的基础架构。它最大的价值是把 LLM 的语言推理能力和外部工具执行能力连接起来，使 Agent 可以动态地观察环境、调整计划并完成任务。

一句话总结：

```text
ReAct Planner = LLM 推理下一步 + 工具执行动作 + 根据观察结果继续规划
```

它适合大多数入门和中级 Agent 场景，尤其适合：

- RAG Agent
- 搜索 Agent
- 工具调用 Agent
- 数据查询 Agent
- 代码辅助 Agent

但如果进入生产环境，需要重点补齐：

```text
结构化输出、工具白名单、状态管理、停止条件、失败恢复、安全控制、评估器
```
