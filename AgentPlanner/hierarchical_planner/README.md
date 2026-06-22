# Hierarchical Planner 详细介绍

## 一、简介

Hierarchical Planner 是分层规划架构。它把复杂任务拆成不同层级：高层 Planner 负责目标拆解和全局策略，低层 Planner 或 Executor 负责具体步骤执行。

一句话理解：

```text
Hierarchical Planner = 高层管方向，低层管执行
```

这种架构非常适合长周期、多子任务、复杂业务流程或多 Agent 系统。

---

## 二、核心流程

```text
用户目标 → 高层任务拆解 → 子任务规划 → 低层执行 → 汇总反馈 → 高层调整
```

示例：

```text
目标：构建企业知识库 Agent

高层计划：
1. 文档处理模块
2. 检索模块
3. 生成模块
4. 评估模块
5. 服务化模块

低层计划：
文档处理模块 → PDF 解析 → Chunk → Metadata → 入库
```

---

## 三、架构图

```text
User Goal
   ↓
High-level Planner
   ↓
Subgoals
   ↓
Low-level Planners
   ↓
Executors / Tools
   ↓
Subtask Results
   ↓
High-level Aggregator
   ↓
Final Answer
```

---

## 四、核心组件

| 组件 | 作用 |
|------|------|
| High-level Planner | 拆解目标、制定全局策略 |
| Subgoal Manager | 管理子目标和依赖关系 |
| Low-level Planner | 为每个子目标生成执行计划 |
| Executor | 执行具体工具调用 |
| State Manager | 管理跨层状态 |
| Aggregator | 汇总子任务结果 |
| Supervisor | 监督整体进展和风险 |

---

## 五、层级设计

### 两层结构

```text
高层 Planner → 低层 Executor
```

适合中等复杂任务。

### 三层结构

```text
战略层 → 任务层 → 执行层
```

适合企业级 Agent。

### 多 Agent 分层结构

```text
Manager Agent
├── Research Agent
├── Coding Agent
├── Review Agent
└── Tool Agent
```

---

## 六、适用场景

### 适合

- 长周期任务
- 企业级 Agent 系统
- 多 Agent 协作
- 自动化研发流程
- 复杂数据分析流程
- 大型报告生成

### 不适合

- 简单单轮问答
- 单工具调用任务
- 对延迟要求极高的任务
- 目标无法拆解的任务

---

## 七、优点

- 适合复杂任务拆解
- 层级清晰
- 可扩展性强
- 便于多 Agent 协作
- 容易做职责隔离
- 便于长期状态管理

---

## 八、缺点

- 架构复杂
- 层级之间通信成本高
- 状态管理困难
- 子任务之间容易不一致
- 调试链路长

---

## 九、数据结构设计

```json
{
  "goal": "完成 AI Agent 技术调研",
  "subgoals": [
    {
      "id": "subgoal_1",
      "name": "调研 Planner 架构",
      "planner": "research_planner",
      "status": "pending"
    },
    {
      "id": "subgoal_2",
      "name": "整理工程实现方案",
      "planner": "engineering_planner",
      "status": "pending"
    }
  ]
}
```

---

## 十、伪代码

```python
def hierarchical_agent(user_goal, llm, tools):
    high_level_plan = generate_subgoals(user_goal, llm)
    subtask_results = {}

    for subgoal in high_level_plan.subgoals:
        low_level_plan = generate_low_level_plan(subgoal, llm)
        result = execute_low_level_plan(low_level_plan, tools)
        subtask_results[subgoal.id] = result

    return aggregate_subtask_results(user_goal, subtask_results, llm)
```

---

## 十一、工程实现关键点

### 1. 明确层级职责

高层不要处理细节，低层不要改变总目标。

```text
高层：做什么、为什么做
低层：怎么做、调用什么工具
```

### 2. 子任务接口要统一

每个子任务应包含：

- 输入
- 输出
- 完成标准
- 依赖关系
- 状态

### 3. 汇总器要处理冲突

不同子任务结果可能冲突，需要 Aggregator 统一判断。

### 4. 支持高层重规划

当多个子任务失败时，高层 Planner 应重新拆解目标。

---

## 十二、与其它 Planner 的区别

| 架构 | 区别 |
|------|------|
| Plan-and-Execute | Plan-and-Execute 通常单层，Hierarchical 多层规划 |
| Multi-Agent | Multi-Agent 强调角色协作，Hierarchical 强调层级拆解 |
| ReAct | ReAct 是单 Agent 动态循环，Hierarchical 是多层任务组织 |
| Workflow-based | Workflow-based 流程固定，Hierarchical 可动态拆解 |
| LLMCompiler | LLMCompiler 强调任务图，Hierarchical 强调抽象层级 |

---

## 十三、总结

Hierarchical Planner 适合复杂长任务和企业级 Agent 系统。

它的核心价值是：

```text
通过分层降低复杂度，让不同层级处理不同粒度的问题
```

当单个 Planner 难以管理任务复杂度时，就应该考虑分层规划。
