# Multi-Agent Planner 详细介绍

## 一、简介

Multi-Agent Planner 是多 Agent 协作规划架构。它不是让一个 Agent 完成所有事情，而是把复杂任务分配给多个具有不同角色和能力的 Agent，由协调器统一规划、分发、汇总和决策。

一句话理解：

```text
Multi-Agent Planner = 多个专业 Agent 协作完成复杂任务
```

它适合复杂研发、研究报告、数据分析、代码生成、企业流程自动化等任务。

---

## 二、核心流程

```text
用户目标 → Coordinator 拆解任务 → 分配给专业 Agent → 各 Agent 执行 → 汇总评审 → 输出结果
```

示例：

```text
目标：生成一份 Agent Planner 技术报告

Coordinator Agent：拆解任务
Research Agent：收集资料
Analysis Agent：分析架构
Writer Agent：撰写文档
Reviewer Agent：审查质量
```

---

## 三、架构图

```text
User Goal
   ↓
Coordinator / Manager Agent
   ↓
Task Assignment
   ↓
┌──────────────┬──────────────┬──────────────┐
│ Research     │ Coding       │ Review       │
│ Agent        │ Agent        │ Agent        │
└──────┬───────┴──────┬───────┴──────┬───────┘
       ↓              ↓              ↓
   Sub Results    Sub Results    Feedback
       └──────────────┬──────────────┘
                      ↓
              Aggregator Agent
                      ↓
                Final Answer
```

---

## 四、核心角色

| 角色 | 作用 |
|------|------|
| Coordinator Agent | 总规划、任务拆解、任务分配 |
| Research Agent | 信息收集、资料检索、证据整理 |
| Analysis Agent | 分析比较、推理判断 |
| Coding Agent | 编写代码、执行脚本、修复错误 |
| Tool Agent | 专门调用外部工具 |
| Reviewer Agent | 审查结果、发现问题、提出修改建议 |
| Memory Agent | 管理长期记忆和上下文 |
| Aggregator Agent | 汇总多个 Agent 的输出 |

---

## 五、协作模式

### 1. Manager-Worker 模式

一个 Manager 负责任务拆解和协调，多个 Worker 负责执行。

```text
Manager → Worker A / Worker B / Worker C → Manager 汇总
```

### 2. Debate 模式

多个 Agent 给出不同观点，再由 Judge 判断。

```text
Agent A 观点
Agent B 观点
Agent C 观点
Judge Agent 选择或融合
```

### 3. Reviewer 模式

一个 Agent 生成结果，另一个 Agent 审查和修改。

```text
Writer → Reviewer → Writer 修正 → Final
```

### 4. Pipeline 模式

不同 Agent 按流水线顺序处理任务。

```text
Research → Analysis → Writing → Review
```

---

## 六、适用场景

### 适合

- 复杂研究报告
- 软件研发 Agent
- 自动数据分析
- 多步骤业务流程
- 需要不同专业能力的任务
- 需要结果审查和质量控制的任务

### 不适合

- 简单问答
- 成本敏感任务
- 低延迟任务
- 角色边界不清的任务
- 信息强一致性要求极高但缺少协调机制的任务

---

## 七、优点

- 职责清晰
- 适合复杂任务
- 可以模拟团队协作
- 易于扩展专业能力
- 可加入 Reviewer 提升质量
- 支持并行执行子任务

---

## 八、缺点

- 成本高
- 通信复杂
- 可能重复工作
- 结果可能冲突
- 需要协调器处理一致性
- 调试困难

---

## 九、任务分配结构

```json
{
  "goal": "生成 Agent Planner 技术报告",
  "assignments": [
    {
      "agent": "research_agent",
      "task": "收集主流 Planner 架构资料",
      "expected_output": "资料摘要和来源"
    },
    {
      "agent": "analysis_agent",
      "task": "对比不同 Planner 的优缺点",
      "expected_output": "对比表"
    },
    {
      "agent": "writer_agent",
      "task": "生成最终 Markdown 文档",
      "expected_output": "README.md"
    }
  ]
}
```

---

## 十、伪代码

```python
def multi_agent_planner(user_goal, coordinator, agents):
    assignments = coordinator.plan(user_goal)
    sub_results = {}

    for assignment in assignments:
        agent = agents[assignment.agent]
        result = agent.run(assignment.task)
        sub_results[assignment.agent] = result

    review = agents["reviewer"].run(sub_results)
    final_answer = coordinator.aggregate(user_goal, sub_results, review)

    return final_answer
```

并行版本：

```python
def run_agents_parallel(assignments, agents):
    futures = []
    for assignment in assignments:
        futures.append(run_async(agents[assignment.agent], assignment.task))
    return collect_results(futures)
```

---

## 十一、工程实现关键点

### 1. 明确角色边界

每个 Agent 必须有清晰职责，避免重复工作。

```text
Research Agent 只负责查资料
Writer Agent 只负责写作
Reviewer Agent 只负责审查
```

### 2. 统一通信协议

Agent 之间最好使用结构化消息：

```json
{
  "from": "research_agent",
  "to": "coordinator",
  "task_id": "task_1",
  "status": "completed",
  "result": "..."
}
```

### 3. 协调器处理冲突

多个 Agent 输出冲突时，需要 Coordinator 或 Judge 决策。

### 4. 控制成本

需要限制：

- Agent 数量
- 每个 Agent 最大轮次
- 最大 token
- 最大工具调用次数

### 5. 引入 Reviewer

复杂任务建议加入 Reviewer，提高质量和安全性。

---

## 十二、与其它 Planner 的区别

| 架构 | 区别 |
|------|------|
| Hierarchical | Hierarchical 强调层级拆解，Multi-Agent 强调角色协作 |
| ReAct | ReAct 通常是单 Agent 循环，Multi-Agent 是多个 Agent 协同 |
| Workflow-based | Workflow 强调固定流程，Multi-Agent 强调团队协作 |
| Plan-and-Execute | Plan-and-Execute 单 Planner + Executor，Multi-Agent 多角色执行 |
| Reflexion | Reflexion 可作为 Reviewer 或 Memory Agent 融入 Multi-Agent |

---

## 十三、总结

Multi-Agent Planner 适合复杂任务和需要专业分工的场景。

它的核心价值是：

```text
把一个大而复杂的问题，交给多个专业 Agent 分工协作
```

生产落地时需要重点控制：

```text
角色边界、通信协议、冲突处理、成本控制、结果审查
```
