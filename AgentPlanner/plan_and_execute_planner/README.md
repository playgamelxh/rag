# Plan-and-Execute Planner 详细介绍

## 一、简介

Plan-and-Execute Planner 是一种“先整体规划，再逐步执行”的 Agent 架构。它将复杂任务分成两个相对独立的阶段：

```text
Plan：生成完整任务计划
Execute：按照计划逐步执行
```

相比 ReAct 的“边想边做”，Plan-and-Execute 更强调先建立全局视角，再进行有序执行。

一句话理解：

```text
Plan-and-Execute Planner = 先生成完整路线图，再按步骤执行
```

---

## 二、核心流程

```text
用户目标 → Planner 生成完整计划 → Executor 执行步骤 → 汇总结果 → 输出最终答案
```

执行中可以加入局部重规划：

```text
执行失败 → 局部调整计划 → 继续执行
```

---

## 三、架构图

```text
User Goal
   ↓
Planner
   ↓
Full Plan
   ↓
Step Executor
   ↓
Step Result
   ↓
Plan State Update
   ↓
Final Synthesizer
   ↓
Final Answer
```

---

## 四、核心组件

| 组件 | 作用 |
|------|------|
| Planner | 根据用户目标生成完整计划 |
| Plan Store | 保存计划步骤、依赖和状态 |
| Executor | 逐步执行计划 |
| Tool Caller | 调用外部工具 |
| State Manager | 记录每一步执行结果 |
| Replanner | 可选，在失败时调整计划 |
| Synthesizer | 汇总所有步骤结果生成最终答案 |

---

## 五、计划结构设计

推荐使用结构化计划：

```json
{
  "goal": "生成一份 AI Agent 调研报告",
  "steps": [
    {
      "id": "step_1",
      "task": "收集 Agent Planner 架构资料",
      "tool": "web_search",
      "depends_on": [],
      "status": "pending"
    },
    {
      "id": "step_2",
      "task": "整理主流架构分类",
      "tool": "llm_summarize",
      "depends_on": ["step_1"],
      "status": "pending"
    },
    {
      "id": "step_3",
      "task": "生成最终报告",
      "tool": "llm_writer",
      "depends_on": ["step_2"],
      "status": "pending"
    }
  ]
}
```

---

## 六、执行策略

### 1. 串行执行

适合步骤之间强依赖的任务。

```text
step_1 → step_2 → step_3
```

### 2. 并行执行

适合多个独立子任务。

```text
step_1 ┐
step_2 ├→ step_4
step_3 ┘
```

### 3. 带重规划执行

适合外部环境变化或执行不稳定的任务。

```text
执行失败 → Replanner → 更新剩余步骤
```

---

## 七、适用场景

### 适合

- 长文档生成
- 研究报告生成
- 数据分析流程
- 自动化办公流程
- 多步骤业务处理
- 可拆解且步骤明确的任务

### 不适合

- 每一步都高度依赖实时观察的任务
- 开放式探索任务
- 工具结果不确定性很强的任务
- 对即时反馈要求很高的交互任务

---

## 八、优点

- 全局结构清晰
- 用户可审核计划
- 适合长任务
- 易于记录任务进度
- 可与任务队列结合
- 更容易做步骤级失败重试

---

## 九、缺点

- 初始计划可能错误
- 对动态变化适应性不如 ReAct
- 计划过细会增加执行成本
- 计划过粗会影响执行质量
- 需要维护计划状态

---

## 十、Prompt 模板

### Planner Prompt

```text
你是一个任务规划引擎。

请把用户目标拆解成可执行计划。

要求：
1. 每一步必须具体
2. 标明依赖关系
3. 标明建议使用的工具
4. 标明预期输出
5. 输出 JSON

用户目标：
{user_goal}
```

### Executor Prompt

```text
你是一个任务执行器。

当前总目标：
{goal}

当前步骤：
{current_step}

已有结果：
{previous_results}

请只完成当前步骤，不要执行其它步骤。
```

### Replanner Prompt

```text
当前计划执行失败。

失败步骤：
{failed_step}

失败原因：
{error}

已有结果：
{completed_results}

请调整剩余计划，保持目标不变。
```

---

## 十一、伪代码

```python
def plan_and_execute(user_goal, llm, tools):
    plan = planner_generate_plan(user_goal, llm)
    results = {}

    for step in plan.steps:
        if not dependencies_completed(step, results):
            continue

        try:
            result = execute_step(step, tools, llm, results)
            results[step.id] = result
            step.status = "completed"
        except Exception as e:
            step.status = "failed"
            plan = replan(user_goal, plan, step, str(e), llm)

    return synthesize_final_answer(user_goal, plan, results, llm)
```

---

## 十二、工程实现关键点

### 1. 计划粒度控制

计划太粗：执行器不知道怎么做。

计划太细：步骤太多，成本过高。

推荐每一步满足：

```text
单一目标 + 明确输入 + 明确输出 + 可独立验证
```

### 2. 状态持久化

长任务需要保存：

- 计划内容
- 当前步骤
- 步骤状态
- 中间产物
- 错误信息
- 重试次数

### 3. 支持人工审核

适合高风险任务：

```text
生成计划 → 人工确认 → 执行
```

### 4. 支持局部重规划

不建议失败后完全重来，而是基于已有结果调整剩余计划。

---

## 十三、与其它 Planner 的区别

| 架构 | 区别 |
|------|------|
| Prompt-based | Prompt-based 只生成计划，Plan-and-Execute 包含执行框架 |
| ReAct | ReAct 边执行边规划，Plan-and-Execute 先整体规划 |
| ReWOO | ReWOO 更强调工具占位符和批量执行 |
| Workflow-based | Workflow-based 流程固定，Plan-and-Execute 动态生成计划 |
| Hierarchical | Hierarchical 有多层规划，Plan-and-Execute 通常是单层计划 |

---

## 十四、总结

Plan-and-Execute Planner 适合结构清晰、步骤明确、周期较长的任务。

它的核心价值是：

```text
先建立全局计划，再降低执行过程中的混乱度
```

生产环境中常见组合是：

```text
Plan-and-Execute + Replanner + Human Review + State Store
```
