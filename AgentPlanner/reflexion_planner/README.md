# Reflexion Planner 详细介绍

## 一、简介

Reflexion Planner 是一种“反思式规划架构”。它让 Agent 在执行任务后，对自己的行为和结果进行反思，总结失败原因，并把经验用于下一轮规划。

它的核心目标不是单次执行最优，而是通过多轮尝试逐步改进。

一句话理解：

```text
Reflexion Planner = 执行任务后自我反思，再基于经验重新规划
```

---

## 二、核心流程

```text
任务执行 → 结果评估 → 失败反思 → 经验记录 → 重新规划 → 再执行
```

典型循环：

```text
Attempt → Evaluate → Reflect → Store Memory → Retry
```

---

## 三、架构图

```text
User Goal
   ↓
Planner
   ↓
Executor
   ↓
Result
   ↓
Evaluator
   ↓
Reflector
   ↓
Memory
   ↓
Replanner
   ↓
Final Answer
```

---

## 四、核心组件

| 组件 | 作用 |
|------|------|
| Planner | 生成初始计划 |
| Executor | 执行计划 |
| Evaluator | 判断结果是否成功 |
| Reflector | 分析失败原因和改进策略 |
| Memory | 保存反思经验 |
| Replanner | 根据反思重新规划 |

---

## 五、反思内容

一个有效的 Reflexion 应该包含：

```json
{
  "success": false,
  "failure_reason": "检索结果不够具体，导致回答缺少证据",
  "lesson": "下次需要使用更具体的查询词，并要求返回来源",
  "next_strategy": "改写 query，增加限定关键词，再重新检索"
}
```

---

## 六、适用场景

### 适合

- 代码生成与调试
- 多轮问题求解
- 自动修复任务
- 复杂推理任务
- 需要从失败中学习的 Agent
- 需要积累经验的长期任务

### 不适合

- 简单一次性任务
- 成本极其敏感的任务
- 不能容忍多轮尝试的低延迟场景
- 反思结果难以验证的任务

---

## 七、优点

- 能从失败中改进
- 适合复杂任务迭代
- 可以形成长期经验
- 能提升多轮任务成功率
- 对代码调试类任务很有帮助

---

## 八、缺点

- LLM 调用成本高
- 反思可能不准确
- 需要评估器判断成功失败
- 需要设计 Memory 管理
- 可能陷入错误经验强化

---

## 九、Prompt 模板

### Reflector Prompt

```text
你是一个 Agent 反思器。

请根据任务目标、执行过程和最终结果，分析失败原因并提出下一轮改进策略。

任务目标：
{goal}

执行过程：
{trajectory}

结果：
{result}

评估反馈：
{feedback}

请输出：
1. 是否成功
2. 失败原因
3. 可复用经验
4. 下一轮策略
```

### Replanner Prompt

```text
你是一个重新规划器。

用户目标：
{goal}

历史失败经验：
{reflections}

请生成新的执行计划，避免重复之前的错误。
```

---

## 十、伪代码

```python
def reflexion_agent(user_goal, llm, tools, max_trials=3):
    memory = []

    for trial in range(max_trials):
        plan = generate_plan(user_goal, memory, llm)
        result = execute_plan(plan, tools)
        evaluation = evaluate_result(user_goal, result, llm)

        if evaluation.success:
            return result

        reflection = reflect(
            goal=user_goal,
            plan=plan,
            result=result,
            evaluation=evaluation,
            llm=llm
        )
        memory.append(reflection)

    return summarize_best_effort(user_goal, memory, llm)
```

---

## 十一、工程实现关键点

### 1. 评估器必须可靠

如果 Evaluator 判断错误，Reflector 会基于错误反馈生成错误经验。

### 2. 反思要结构化

不要只保存自然语言，应保存：

- 失败原因
- 错误步骤
- 改进策略
- 是否可复用
- 适用任务类型

### 3. 避免无限重试

必须限制：

- 最大尝试次数
- 最大反思次数
- 最大成本
- 重复失败检测

### 4. Memory 要筛选

不是所有反思都值得长期保存。错误反思应被过滤。

---

## 十二、与其它 Planner 的区别

| 架构 | 区别 |
|------|------|
| ReAct | ReAct 强调实时观察，Reflexion 强调执行后的反思学习 |
| Plan-and-Execute | Plan-and-Execute 强调计划执行，Reflexion 强调失败改进 |
| Workflow-based | Workflow-based 追求稳定流程，Reflexion 追求试错优化 |
| Multi-Agent | Reflexion 可以作为 Reviewer Agent 或 Memory Agent 的能力 |
| Tree Search | Tree Search 同时探索多路径，Reflexion 多轮改进单一路径 |

---

## 十三、总结

Reflexion Planner 适合需要多轮尝试、结果可评估、失败可修正的任务。

它的核心价值是：

```text
让 Agent 不只是失败，而是从失败中总结经验并改进下一次执行
```

生产中常与以下模块组合：

```text
Evaluator + Memory + Replanner + Retry Controller
```
