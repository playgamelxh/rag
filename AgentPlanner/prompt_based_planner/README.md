# Prompt-based Planner 详细介绍

## 一、简介

Prompt-based Planner 是最简单、最直接的 Agent Planner 架构。它不依赖复杂状态机、任务图或工具调度框架，而是通过一段精心设计的 Prompt，让 LLM 直接把用户目标拆解成计划步骤。

它通常用于 Agent 系统的早期原型，也常用于简单任务拆解、文档大纲生成、工作流辅助和低风险自动化场景。

一句话理解：

```text
Prompt-based Planner = 用提示词让 LLM 直接生成任务计划
```

---

## 二、核心流程

```text
用户目标 → 规划 Prompt → LLM 输出步骤列表 → Executor 执行 / 用户手动执行
```

典型输出：

```text
目标：写一份大模型推理引擎调研报告

计划：
1. 收集主流推理引擎资料
2. 对比各引擎的定位和适用场景
3. 整理核心技术点
4. 输出报告大纲
5. 编写最终报告
```

---

## 三、架构图

```text
User Input
   ↓
Prompt Template
   ↓
LLM Planner
   ↓
Plan Text / Plan JSON
   ↓
Executor / Human Review
```

---

## 四、核心组件

| 组件 | 作用 |
|------|------|
| User Goal | 用户输入的任务目标 |
| Prompt Template | 约束 LLM 如何生成计划 |
| LLM Planner | 根据 Prompt 输出计划 |
| Plan Parser | 可选，把自然语言计划转成结构化步骤 |
| Executor | 可选，执行计划步骤 |
| Human Reviewer | 可选，人工确认计划是否合理 |

---

## 五、Prompt 模板

### 自然语言计划模板

```text
你是一个任务规划助手。

请把用户目标拆解为清晰、可执行、按顺序排列的步骤。

要求：
1. 每一步必须具体
2. 每一步只做一件事
3. 如果有依赖关系，需要按依赖顺序排列
4. 不要执行任务，只输出计划

用户目标：
{user_goal}
```

### JSON 结构化计划模板

```text
你是一个任务规划引擎。

请把用户目标拆解为 JSON 格式的计划。

输出格式：
{
  "goal": "用户目标",
  "steps": [
    {
      "id": "step_1",
      "task": "具体任务",
      "depends_on": [],
      "expected_output": "预期产出"
    }
  ]
}

用户目标：
{user_goal}
```

---

## 六、适用场景

### 适合

- 简单任务拆解
- 学习计划生成
- 文档大纲生成
- 报告写作规划
- 产品需求拆解
- 低风险手动执行任务

### 不适合

- 强依赖工具调用的任务
- 需要动态观察反馈的任务
- 高风险自动执行任务
- 多分支复杂流程
- 长周期任务管理

---

## 七、优点

- 实现成本最低
- 不需要复杂框架
- 非常适合原型验证
- 输出结果容易理解
- 可以作为其它 Planner 的前置规划阶段

---

## 八、缺点

- 计划可能过于理想化
- 缺少执行反馈
- 不能自动处理失败
- 对复杂任务容易遗漏步骤
- 很难判断计划是否真正完成

---

## 九、工程实现建议

### 1. 使用结构化输出

自然语言计划可读性强，但不利于程序执行。工程中建议转成 JSON：

```json
{
  "goal": "构建 RAG 知识库",
  "steps": [
    {
      "id": "step_1",
      "task": "收集文档",
      "status": "pending"
    },
    {
      "id": "step_2",
      "task": "进行文本切分",
      "status": "pending"
    }
  ]
}
```

### 2. 加入计划审核

可以让 LLM 自检计划：

```text
请检查以上计划是否遗漏关键步骤、是否存在依赖顺序错误。
```

### 3. 加入人工确认

对于会触发真实执行的任务，建议加入人工确认：

```text
Plan → Human Review → Execute
```

### 4. 和 Executor 解耦

Prompt-based Planner 只负责生成计划，不直接执行。

```text
Planner：生成步骤
Executor：执行步骤
Evaluator：评估结果
```

---

## 十、伪代码

```python
def prompt_based_plan(user_goal, llm):
    prompt = build_planning_prompt(user_goal)
    plan_text = llm.generate(prompt)
    plan = parse_plan(plan_text)
    return plan
```

结构化版本：

```python
def prompt_based_json_plan(user_goal, llm):
    prompt = build_json_planning_prompt(user_goal)
    output = llm.generate(prompt)
    plan = json.loads(output)
    validate_plan_schema(plan)
    return plan
```

---

## 十一、与其它 Planner 的区别

| 架构 | 区别 |
|------|------|
| ReAct | ReAct 会边执行边观察，Prompt-based 通常只生成一次计划 |
| Plan-and-Execute | Plan-and-Execute 更强调计划与执行框架，Prompt-based 更轻量 |
| ReWOO | ReWOO 会生成工具占位符，Prompt-based 不一定涉及工具 |
| Workflow-based | Workflow-based 有固定流程，Prompt-based 更自由但更不可控 |
| Multi-Agent | Multi-Agent 有多角色协作，Prompt-based 通常是单 LLM 规划 |

---

## 十二、总结

Prompt-based Planner 是最适合入门的 Planner 架构。它简单、直观、低成本，适合快速验证 Agent 规划能力。

但它的缺点也明显：缺少执行反馈、失败恢复和状态管理。

因此，它更适合作为：

```text
简单任务规划器 / 原型规划器 / 更复杂 Planner 的基础模块
```
