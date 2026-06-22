# LLMCompiler Planner 详细介绍

## 一、简介

LLMCompiler Planner 是一种“编译式规划架构”。它把用户的自然语言目标转换成类似程序执行图的任务结构，然后由调度器按照依赖关系执行。

它和传统编译器有相似思想：

```text
自然语言任务 → 中间表示 IR / DAG → 调度执行 → 汇总结果
```

一句话理解：

```text
LLMCompiler Planner = 把 Agent 任务编译成可调度的任务图
```

---

## 二、核心流程

```text
用户目标 → LLM 编译任务图 → 调度器分析依赖 → 并行 / 串行执行 → 汇总输出
```

---

## 三、架构图

```text
User Goal
   ↓
LLM Compiler
   ↓
Task Graph / DAG
   ↓
Scheduler
   ↓
Tool Executors
   ↓
Result Aggregator
   ↓
Final Answer
```

---

## 四、核心组件

| 组件 | 作用 |
|------|------|
| Compiler Planner | 把用户任务编译成任务图 |
| Intermediate Representation | 中间表示，如 JSON DAG |
| Dependency Analyzer | 分析任务依赖关系 |
| Scheduler | 按依赖调度任务执行 |
| Executor Pool | 并行执行工具或子任务 |
| Aggregator | 汇总中间结果 |
| Error Handler | 处理失败、重试和降级 |

---

## 五、任务图结构

推荐使用 DAG 表达任务：

```json
{
  "goal": "生成一份行业分析报告",
  "tasks": [
    {
      "id": "task_1",
      "name": "搜索行业背景",
      "tool": "web_search",
      "input": {
        "query": "AI Agent market overview"
      },
      "depends_on": []
    },
    {
      "id": "task_2",
      "name": "搜索技术趋势",
      "tool": "web_search",
      "input": {
        "query": "AI Agent technology trends"
      },
      "depends_on": []
    },
    {
      "id": "task_3",
      "name": "汇总分析报告",
      "tool": "llm_writer",
      "input": {
        "sources": ["task_1", "task_2"]
      },
      "depends_on": ["task_1", "task_2"]
    }
  ]
}
```

---

## 六、调度策略

### 1. 拓扑排序

按照依赖关系执行：

```text
无依赖任务 → 依赖完成后的任务 → 汇总任务
```

### 2. 并行调度

无依赖任务可以并行：

```text
task_1 ┐
task_2 ├→ task_3
task_4 ┘
```

### 3. 失败重试

任务失败后可以：

- 原任务重试
- 替换工具
- 降级执行
- 触发重新编译任务图

---

## 七、适用场景

### 适合

- 多工具复杂任务
- 数据分析 Agent
- 研究报告 Agent
- 并行信息收集
- 自动化工作流
- 大量 API 调用编排

### 不适合

- 简单单步任务
- 高度开放式探索任务
- 每一步都需要人工交互确认的任务
- 无法明确依赖关系的任务

---

## 八、优点

- 支持并行执行
- 任务依赖清晰
- 适合复杂任务调度
- 容易做性能优化
- 便于记录执行状态
- 更接近工程化工作流系统

---

## 九、缺点

- 实现复杂度高
- 对任务图格式要求严格
- Planner 输出错误会导致调度失败
- 需要调度器和状态管理
- 调试成本较高

---

## 十、伪代码

```python
def llmcompiler_agent(user_goal, llm, tools):
    graph = compile_task_graph(user_goal, llm)
    validate_dag(graph)

    results = {}
    ready_tasks = find_ready_tasks(graph, results)

    while ready_tasks:
        batch_results = execute_parallel(ready_tasks, tools, results)
        results.update(batch_results)
        ready_tasks = find_ready_tasks(graph, results)

    return aggregate_results(user_goal, graph, results, llm)
```

---

## 十一、工程实现关键点

### 1. DAG 校验

必须检查：

- 是否有环
- 依赖任务是否存在
- 工具是否存在
- 参数是否合法

### 2. 中间表示稳定

推荐 JSON Schema 校验任务图。

### 3. 调度器独立

不要让 LLM 直接执行任务，LLM 只负责编译任务图。

```text
LLM 负责规划
Scheduler 负责调度
Executor 负责执行
```

### 4. 任务结果可引用

后续任务可以引用前面任务输出：

```json
{
  "input": {
    "context_from": ["task_1", "task_2"]
  }
}
```

### 5. 支持重新编译

当任务图无法继续执行时，可以让 LLM 基于失败状态重新编译剩余任务图。

---

## 十二、与其它 Planner 的区别

| 架构 | 区别 |
|------|------|
| ReWOO | ReWOO 是轻量工具占位符，LLMCompiler 是完整任务图 |
| Plan-and-Execute | Plan-and-Execute 偏顺序步骤，LLMCompiler 强调 DAG 调度 |
| ReAct | ReAct 动态循环，LLMCompiler 先编译任务图 |
| Workflow-based | Workflow-based 流程预定义，LLMCompiler 动态生成流程 |
| Multi-Agent | Multi-Agent 强调角色协作，LLMCompiler 强调任务编排 |

---

## 十三、总结

LLMCompiler Planner 适合复杂、可并行、依赖关系明确的 Agent 任务。

它的核心价值是：

```text
把自然语言任务转成可执行、可调度、可优化的任务图
```

如果要构建工程化复杂 Agent，LLMCompiler 思路非常重要，但实现成本也高于 ReAct 和 Plan-and-Execute。
