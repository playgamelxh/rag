# Workflow-based Planner 详细介绍

## 一、简介

Workflow-based Planner 是一种基于预定义工作流的规划架构。它不是让 LLM 完全自由规划，而是把 Agent 限制在可控流程中，LLM 只负责判断分支、填充参数或选择下一节点。

一句话理解：

```text
Workflow-based Planner = 固定流程 + LLM 辅助决策
```

这是最适合生产环境的一类 Agent Planner 架构之一。

---

## 二、核心流程

```text
用户输入 → 工作流入口 → LLM 判断参数 / 分支 → 节点执行 → 状态流转 → 输出结果
```

示例：

```text
客服 Agent：
识别问题类型 → 查询订单 → 判断是否需要退款 → 生成回复 → 人工确认
```

---

## 三、架构图

```text
User Input
   ↓
Workflow Engine
   ↓
Node Router
   ↓
Task Node / Tool Node / LLM Node
   ↓
State Update
   ↓
Next Node
   ↓
Final Output
```

---

## 四、核心组件

| 组件 | 作用 |
|------|------|
| Workflow Definition | 预定义流程图 |
| Node Router | 判断下一步节点 |
| LLM Node | 使用 LLM 做理解、生成、判断 |
| Tool Node | 调用外部工具或 API |
| Condition Node | 分支判断 |
| State Store | 保存工作流状态 |
| Guardrails | 权限、安全和审计 |

---

## 五、工作流结构

```json
{
  "workflow": "rag_qa_flow",
  "nodes": [
    {
      "id": "classify_query",
      "type": "llm",
      "next": "retrieve_docs"
    },
    {
      "id": "retrieve_docs",
      "type": "tool",
      "tool": "vector_search",
      "next": "rerank_docs"
    },
    {
      "id": "rerank_docs",
      "type": "tool",
      "tool": "reranker",
      "next": "generate_answer"
    },
    {
      "id": "generate_answer",
      "type": "llm",
      "next": "final"
    }
  ]
}
```

---

## 六、适用场景

### 适合

- 企业生产系统
- 客服 Agent
- 审批流 Agent
- RAG 问答流程
- 数据处理流水线
- 合规和安全要求高的任务

### 不适合

- 完全开放式探索任务
- 需要自由创造计划的任务
- 临时性很强的复杂问题求解
- 流程无法提前定义的任务

---

## 七、优点

- 稳定性高
- 可控性强
- 易于审计
- 安全边界明确
- 适合生产环境
- 易于接入权限和日志系统

---

## 八、缺点

- 灵活性不足
- 需要提前设计流程
- 流程变更需要维护
- 对开放式任务适应性较弱
- 过多节点会增加复杂度

---

## 九、节点类型

| 节点类型 | 说明 |
|----------|------|
| LLM Node | 文本理解、摘要、生成、判断 |
| Tool Node | 调用数据库、搜索、API、代码执行 |
| Condition Node | 根据状态判断分支 |
| Human Node | 人工审核或确认 |
| Memory Node | 读取或写入记忆 |
| End Node | 输出最终结果 |

---

## 十、伪代码

```python
def workflow_agent(user_input, workflow, state):
    current_node = workflow.entry
    state["user_input"] = user_input

    while current_node != "final":
        node = workflow.get_node(current_node)
        result = execute_node(node, state)
        state.update(result)
        current_node = route_next_node(node, state)

    return state["final_answer"]
```

---

## 十一、工程实现关键点

### 1. 状态驱动

工作流应该由状态驱动，而不是纯文本上下文驱动。

```json
{
  "query": "用户问题",
  "intent": "refund",
  "order_id": "123",
  "risk_level": "low"
}
```

### 2. 节点职责单一

每个节点只做一件事，便于调试和复用。

### 3. 高风险节点加人工确认

例如：

- 删除数据
- 退款
- 发送外部邮件
- 执行代码
- 修改生产配置

### 4. 可观测性

记录：

- 节点输入
- 节点输出
- 执行时间
- 错误信息
- LLM token 成本

---

## 十二、与其它 Planner 的区别

| 架构 | 区别 |
|------|------|
| ReAct | ReAct 灵活但不可控，Workflow 更稳定可控 |
| Plan-and-Execute | Plan 动态生成，Workflow 预先定义 |
| LLMCompiler | LLMCompiler 动态编译任务图，Workflow 使用固定任务图 |
| Multi-Agent | Multi-Agent 多角色协作，Workflow 强调流程约束 |
| Prompt-based | Prompt-based 自由规划，Workflow 限定流程 |

---

## 十三、总结

Workflow-based Planner 是最适合生产落地的 Agent Planner 架构之一。

它的核心价值是：

```text
用固定流程保证稳定性，用 LLM 增强理解和决策能力
```

如果任务面向真实业务、高风险操作或企业系统，优先考虑 Workflow-based Planner。
