# Agent Planner（规划引擎）主流架构全分类

## 一、简介

Agent Planner（规划引擎）是 AI Agent 系统中的核心模块，负责把用户目标拆解为可执行步骤，并决定每一步应该调用什么工具、查询什么信息、如何判断结果是否完成。

在一个完整 Agent 系统中，Planner 通常处于“大脑”的位置：

```text
用户目标 → Planner 任务规划 → Tool / Memory / LLM 执行 → 观察结果 → 调整计划 → 输出结果
```

如果说 LLM 负责语言理解和推理，Tool 负责执行外部动作，Memory 负责保存上下文，那么 Planner 负责解决的问题就是：

```text
下一步该做什么？为什么做？做完后如何判断是否继续？
```

---

## 二、Agent Planner 要解决的核心问题

| 问题 | 说明 |
|------|------|
| 任务拆解 | 把复杂目标拆成多个子任务 |
| 执行顺序 | 判断子任务之间的依赖关系 |
| 工具选择 | 决定调用搜索、数据库、代码、浏览器、文件等工具 |
| 状态跟踪 | 记录当前完成了什么、还缺什么 |
| 失败恢复 | 工具失败、信息不足、结果错误时重新规划 |
| 目标对齐 | 判断最终结果是否满足用户目标 |
| 成本控制 | 控制 token、工具调用次数、执行时间 |

---

## 详细文档索引

| 架构 | 详细文档 |
|------|----------|
| Prompt-based Planner | [prompt_based_planner/README.md](prompt_based_planner/README.md) |
| ReAct Planner | [react_planner/README.md](react_planner/README.md) |
| Plan-and-Execute Planner | [plan_and_execute_planner/README.md](plan_and_execute_planner/README.md) |
| ReWOO Planner | [rewoo_planner/README.md](rewoo_planner/README.md) |
| LLMCompiler Planner | [llmcompiler_planner/README.md](llmcompiler_planner/README.md) |
| Reflexion Planner | [reflexion_planner/README.md](reflexion_planner/README.md) |
| Tree / Graph Search Planner | [tree_graph_search_planner/README.md](tree_graph_search_planner/README.md) |
| Hierarchical Planner | [hierarchical_planner/README.md](hierarchical_planner/README.md) |
| Workflow-based Planner | [workflow_based_planner/README.md](workflow_based_planner/README.md) |
| Multi-Agent Planner | [multi_agent_planner/README.md](multi_agent_planner/README.md) |

---

## 三、Agent Planner 主流架构分类

### 1. Prompt-based Planner（提示词规划架构）

#### 核心思想

直接通过 Prompt 让 LLM 输出计划步骤。

```text
用户目标 + 规划提示词 → LLM 生成步骤列表 → Executor 执行
```

#### 典型形式

```text
请将以下目标拆解为可执行步骤：
目标：为某个主题写一份研究报告
输出：
1. 搜集资料
2. 提取关键信息
3. 组织大纲
4. 生成报告
```

#### 优点

- 实现简单
- 适合原型验证
- 不依赖复杂框架
- 易于理解和调试

#### 缺点

- 计划容易过于粗糙
- 缺少执行反馈
- 不能很好处理失败恢复
- 对复杂任务稳定性不足

#### 适用场景

- 简单任务拆解
- 工作流辅助
- 文档生成
- 低风险自动化

---

### 2. ReAct Planner（Reasoning + Acting 架构）

#### 核心思想

让 LLM 在“思考”和“行动”之间循环：先推理下一步，再调用工具，再根据观察结果继续推理。

```text
Thought → Action → Observation → Thought → Action → Observation → Final Answer
```

#### 优点

- 能根据执行结果动态调整计划
- 适合工具调用和信息检索任务
- 过程可解释性较强
- 是很多 Agent 框架的基础模式

#### 缺点

- 容易陷入循环
- 工具调用成本较高
- 对 Prompt 和停止条件依赖较强
- 长任务中上下文容易膨胀

#### 适用场景

- 搜索问答
- 数据查询
- RAG Agent
- 工具调用 Agent
- 代码辅助 Agent

#### 详细文档

[ReAct Planner 详细介绍](react_planner/README.md)

---

### 3. Plan-and-Execute Planner（先规划后执行架构）

#### 核心思想

先由 Planner 生成完整计划，再由 Executor 按步骤执行。执行过程中可选地进行局部修正。

```text
用户目标 → 生成完整计划 → 逐步执行 → 汇总结果
```

#### 优点

- 结构清晰
- 适合长任务
- 便于用户审核计划
- 便于拆分执行和并行处理

#### 缺点

- 初始计划可能不准确
- 对动态环境适应性较弱
- 如果中间结果变化大，需要重新规划

#### 适用场景

- 报告生成
- 数据分析流程
- 复杂文档处理
- 多步骤业务流程

---

### 4. ReWOO Planner（Reasoning Without Observation 架构）

#### 核心思想

先规划完整推理链和工具调用占位符，再统一执行工具，最后根据工具结果生成答案。

```text
Plan: 设计推理路径和工具调用
Worker: 执行工具调用
Solver: 汇总结果生成答案
```

#### 示例结构

```text
Plan: 我需要查询 A 的信息，再查询 B 的信息，最后比较两者
E1: Search[A]
E2: Search[B]
Solver: 根据 E1 和 E2 生成最终答案
```

#### 优点

- 减少多轮 LLM 调用
- 计划结构更稳定
- 工具调用可以并行
- 成本可控性较好

#### 缺点

- 执行过程中缺少动态反馈
- 初始计划错误会影响后续结果
- 对复杂异常处理不如 ReAct 灵活

#### 适用场景

- 多信息源查询
- 可并行工具调用
- 成本敏感任务
- 结构化研究任务

---

### 5. LLMCompiler Planner（编译式规划架构）

#### 核心思想

把用户任务编译成一个任务图或执行图，然后按照依赖关系调度执行。

```text
用户目标 → 任务图 DAG → 调度器执行 → 汇总输出
```

#### 优点

- 支持并行执行
- 适合复杂任务依赖
- 任务结构清晰
- 便于优化执行效率

#### 缺点

- 实现复杂
- 需要任务图解析和调度机制
- 对 Planner 输出格式要求高

#### 适用场景

- 多工具复杂 Agent
- 数据分析 Agent
- 自动化工作流
- 可并行执行的研究任务

---

### 6. Reflexion Planner（反思式规划架构）

#### 核心思想

Agent 执行任务后，对结果进行自我反思，总结错误经验，并在下一轮任务中改进。

```text
执行 → 失败 / 不理想 → 反思 → 记录经验 → 重新规划
```

#### 优点

- 能从失败中改进
- 适合需要多轮尝试的任务
- 可以结合长期记忆
- 对复杂任务更稳健

#### 缺点

- 成本较高
- 反思质量依赖 LLM
- 可能产生错误反思
- 需要记忆管理机制

#### 适用场景

- 代码生成与调试
- 自动任务修复
- 长期学习型 Agent
- 多轮优化任务

---

### 7. Tree / Graph Search Planner（树搜索 / 图搜索规划架构）

#### 核心思想

把可能的行动路径展开成树或图，通过搜索、评分、回溯选择最优路径。

```text
目标 → 多个候选动作 → 展开路径 → 评分 → 选择最优路径
```

#### 常见方法

- Tree of Thoughts
- Graph of Thoughts
- Monte Carlo Tree Search
- Beam Search Planning

#### 优点

- 适合复杂推理
- 可以比较多条候选路径
- 能提升复杂问题求解质量
- 支持回溯和搜索

#### 缺点

- Token 成本高
- 搜索空间容易爆炸
- 工程实现复杂
- 响应延迟较高

#### 适用场景

- 数学推理
- 复杂决策
- 多路径任务求解
- 需要高正确率的规划任务

---

### 8. Hierarchical Planner（分层规划架构）

#### 核心思想

把规划拆成高层规划和低层执行规划。高层负责目标拆解，低层负责具体工具调用和执行细节。

```text
高层目标规划 → 子任务规划 → 工具执行 → 结果汇总
```

#### 优点

- 适合复杂长任务
- 结构清晰
- 可扩展性好
- 便于多 Agent 协作

#### 缺点

- 架构复杂
- 高低层之间需要良好通信协议
- 状态管理难度较高

#### 适用场景

- 企业级 Agent 系统
- 多 Agent 协作
- 长周期任务
- 自动化办公和研发流程

---

### 9. Workflow-based Planner（工作流规划架构）

#### 核心思想

把 Agent 任务约束在预定义工作流中，Planner 只负责选择路径、填充参数或判断分支。

```text
预定义流程图 → LLM 判断分支 / 参数 → 节点执行 → 输出结果
```

#### 优点

- 稳定性高
- 可控性强
- 适合生产环境
- 易于权限、安全和审计

#### 缺点

- 灵活性较弱
- 需要提前设计流程
- 不适合完全开放式任务

#### 适用场景

- 企业业务流程
- 客服 Agent
- 审批流 Agent
- 数据处理流水线
- 低风险生产系统

---

### 10. Multi-Agent Planner（多 Agent 协作规划架构）

#### 核心思想

多个 Agent 分别承担不同角色，由一个主 Planner 或协调器分配任务、收集结果并进行决策。

```text
Coordinator → Research Agent / Coding Agent / Review Agent / Tool Agent → 汇总结果
```

#### 常见角色

- Planner Agent
- Research Agent
- Coding Agent
- Reviewer Agent
- Tool Agent
- Memory Agent

#### 优点

- 职责清晰
- 适合复杂任务
- 可以模拟团队协作
- 便于扩展专业能力

#### 缺点

- 成本高
- 通信复杂
- 容易出现重复工作
- 一致性和冲突处理困难

#### 适用场景

- 软件研发 Agent
- 研究报告 Agent
- 自动数据分析 Agent
- 复杂企业流程自动化

---

## 四、主流架构对比

| 架构 | 动态调整 | 工具调用 | 并行能力 | 成本 | 复杂度 | 适合场景 |
|------|----------|----------|----------|------|--------|----------|
| Prompt-based | 弱 | 弱 | 弱 | 低 | 低 | 简单任务拆解 |
| ReAct | 强 | 强 | 弱 | 中高 | 中 | 工具调用、搜索问答 |
| Plan-and-Execute | 中 | 中 | 中 | 中 | 中 | 长任务、报告生成 |
| ReWOO | 弱 | 强 | 强 | 中 | 中 | 多信息源查询 |
| LLMCompiler | 中 | 强 | 强 | 中 | 高 | 复杂任务图执行 |
| Reflexion | 强 | 中 | 弱 | 高 | 中高 | 调试、迭代优化 |
| Tree / Graph Search | 强 | 中 | 中 | 高 | 高 | 复杂推理和决策 |
| Hierarchical | 强 | 强 | 中 | 中高 | 高 | 长周期复杂任务 |
| Workflow-based | 中 | 强 | 中 | 低中 | 中 | 企业生产流程 |
| Multi-Agent | 强 | 强 | 中 | 高 | 高 | 多角色协作任务 |

---

## 五、如何选择 Agent Planner 架构

### 简单任务

```text
Prompt-based Planner
```

适合任务拆解、摘要、大纲生成、简单自动化。

### 需要工具调用和动态反馈

```text
ReAct Planner
```

适合搜索、查询、代码执行、RAG Agent。

### 长任务和报告生成

```text
Plan-and-Execute Planner
```

适合先生成大纲，再分步骤执行。

### 多个工具调用可以并行

```text
ReWOO / LLMCompiler
```

适合多搜索源、多 API 查询、多数据分析任务。

### 生产环境稳定可控

```text
Workflow-based Planner
```

适合企业业务流程、客服、审批、固定链路任务。

### 复杂研发或研究任务

```text
Multi-Agent Planner / Hierarchical Planner
```

适合代码生成、研究报告、复杂系统自动化。

---

## 六、Agent Planner 在完整 Agent 系统中的位置

一个典型 Agent 系统可以拆成：

```text
User Input
   ↓
Intent Understanding
   ↓
Planner
   ↓
Executor / Tool Caller
   ↓
Memory / State Manager
   ↓
Evaluator / Reflector
   ↓
Final Answer
```

其中 Planner 不是孤立模块，它通常需要和以下组件协同：

| 组件 | 作用 |
|------|------|
| LLM | 生成计划、推理下一步 |
| Tool Registry | 提供可调用工具列表 |
| Executor | 执行工具调用 |
| Memory | 存储历史计划、结果和经验 |
| Evaluator | 判断执行结果是否满足目标 |
| Guardrails | 做权限、安全和输出约束 |
| State Manager | 跟踪任务状态和中间结果 |

---

## 七、工程实现关键点

### 1. 计划格式结构化

不要只依赖自然语言计划，推荐使用 JSON / YAML / DSL 表达计划。

```json
{
  "goal": "生成一份市场分析报告",
  "steps": [
    {
      "id": "step_1",
      "task": "搜索行业资料",
      "tool": "web_search",
      "status": "pending"
    },
    {
      "id": "step_2",
      "task": "整理关键信息",
      "tool": "llm_summarize",
      "status": "pending"
    }
  ]
}
```

### 2. 明确停止条件

Planner 必须知道何时停止，常见停止条件包括：

- 达到最终答案
- 达到最大步骤数
- 达到最大工具调用次数
- 结果置信度足够
- 用户目标已满足
- 出现不可恢复错误

### 3. 工具调用要有 Schema

每个工具都应该描述：

- 工具名称
- 输入参数
- 输出格式
- 错误类型
- 权限限制
- 调用成本

### 4. 规划和执行分离

推荐将 Planner 和 Executor 分开：

```text
Planner：决定做什么
Executor：负责怎么做
Evaluator：判断做得怎么样
```

这样更容易调试、测试和扩展。

### 5. 加入安全边界

生产环境 Planner 必须考虑：

- 不允许执行危险命令
- 不允许访问未授权数据
- 不允许泄露敏感信息
- 工具调用需要权限控制
- 高风险动作需要人工确认

---

## 八、学习路线建议

### 第一阶段：理解基础模式

- Prompt-based Planner
- ReAct
- Plan-and-Execute

### 第二阶段：理解复杂规划

- ReWOO
- LLMCompiler
- Reflexion

### 第三阶段：理解生产架构

- Workflow-based Planner
- Hierarchical Planner
- Multi-Agent Planner

### 第四阶段：动手实现

建议依次实现：

```text
1. 简单 Prompt Planner
2. ReAct 工具调用 Agent
3. Plan-and-Execute 报告生成 Agent
4. Workflow-based RAG Agent
5. Multi-Agent 研究助手
```

---

## 九、推荐深入阅读

| 主题 | 建议 |
|------|------|
| ReAct | 理解 Thought / Action / Observation 循环 |
| Tool Calling | 学习函数调用、工具 Schema、参数校验 |
| LangGraph | 理解状态图和可控 Agent 流程 |
| AutoGen | 理解多 Agent 协作 |
| CrewAI | 理解角色化 Agent 协作 |
| LlamaIndex Agent | 理解 RAG 场景下的 Agent Planner |
| OpenAI Function Calling | 理解生产级工具调用接口 |

---

## 十、总结

Agent Planner 是 Agent 能否真正完成复杂任务的关键。不同架构没有绝对优劣，核心是根据任务复杂度、工具调用需求、稳定性要求和成本约束选择合适方案。

简单总结：

```text
简单任务：Prompt-based
工具调用：ReAct
长任务：Plan-and-Execute
并行任务：ReWOO / LLMCompiler
复杂推理：Tree / Graph Search
生产稳定：Workflow-based
长周期复杂任务：Hierarchical
团队协作模拟：Multi-Agent
```

如果要从工程角度落地，建议优先掌握 ReAct 和 Workflow-based 两类架构：

- ReAct 代表灵活的动态工具调用能力
- Workflow-based 代表生产环境中的稳定可控能力

本目录将先详细展开 ReAct Planner，因为它是理解 Agent 工具调用和动态规划最经典的基础架构。
