# Tree / Graph Search Planner 详细介绍

## 一、简介

Tree / Graph Search Planner 是一种基于搜索的 Agent 规划架构。它不会只生成一条执行路径，而是展开多个可能的推理或行动路径，通过评分、比较、回溯选择更优方案。

典型代表包括：

- Tree of Thoughts
- Graph of Thoughts
- Beam Search Planning
- Monte Carlo Tree Search

一句话理解：

```text
Tree / Graph Search Planner = 同时探索多条候选路径，再选择最优路径
```

---

## 二、核心流程

```text
用户目标 → 生成多个候选思路 → 展开搜索树 / 图 → 评分 → 选择路径 → 输出答案
```

示例：

```text
问题
├── 思路 A
│   ├── 子思路 A1
│   └── 子思路 A2
├── 思路 B
│   ├── 子思路 B1
│   └── 子思路 B2
└── 思路 C
    └── 子思路 C1
```

---

## 三、架构图

```text
User Goal
   ↓
Candidate Generator
   ↓
Search Tree / Graph
   ↓
Evaluator / Scorer
   ↓
Path Selector
   ↓
Executor / Solver
   ↓
Final Answer
```

---

## 四、核心组件

| 组件 | 作用 |
|------|------|
| Candidate Generator | 生成多个候选思路或动作 |
| Search State | 表示当前推理状态或任务状态 |
| Expander | 扩展下一层候选节点 |
| Evaluator | 给候选节点打分 |
| Search Strategy | 决定如何搜索，如 BFS、DFS、Beam Search、MCTS |
| Path Selector | 选择最优路径 |
| Solver | 根据最优路径生成最终结果 |

---

## 五、常见搜索策略

### 1. Tree of Thoughts

让 LLM 生成多个中间思路，再逐步展开和评分。

```text
Thought 1 → Thought 1.1 → Answer
Thought 2 → Thought 2.1 → Answer
Thought 3 → Pruned
```

### 2. Graph of Thoughts

不局限于树结构，允许多个思路合并、引用和重组。

```text
A → C
B → C
C → D
```

### 3. Beam Search Planning

每一层只保留得分最高的 K 个候选。

```text
每轮生成 N 个候选 → 打分 → 保留 Top-K
```

### 4. Monte Carlo Tree Search

通过模拟多条路径，逐渐把搜索资源集中到更有希望的路径上。

---

## 六、适用场景

### 适合

- 数学推理
- 逻辑推理
- 复杂决策
- 多方案比较
- 高正确率要求任务
- 策略规划和路径选择

### 不适合

- 简单任务
- 成本敏感任务
- 低延迟在线服务
- 搜索空间巨大且无法评分的任务
- 评分标准模糊的开放任务

---

## 七、优点

- 可以探索多个解法
- 支持回溯
- 能提升复杂问题正确率
- 可结合评分器优化输出
- 适合难题求解和方案比较

---

## 八、缺点

- Token 成本高
- 延迟高
- 搜索空间容易爆炸
- 评分器设计困难
- 工程实现复杂

---

## 九、评分方法

常见评分维度：

| 维度 | 说明 |
|------|------|
| Correctness | 是否正确 |
| Completeness | 是否完整 |
| Feasibility | 是否可执行 |
| Cost | 执行成本是否合理 |
| Risk | 是否存在风险 |
| Evidence | 是否有证据支持 |

评分可以由：

- LLM 自评
- 规则函数
- 外部验证器
- 单元测试
- 人工反馈

---

## 十、伪代码

```python
def tree_search_planner(user_goal, llm, max_depth=3, beam_size=3):
    frontier = [create_root_state(user_goal)]

    for depth in range(max_depth):
        candidates = []
        for state in frontier:
            next_states = expand_state(state, llm)
            candidates.extend(next_states)

        scored = [(state, evaluate_state(state, llm)) for state in candidates]
        frontier = select_top_k(scored, k=beam_size)

    best_state = select_best(frontier)
    return generate_answer_from_path(best_state, llm)
```

---

## 十一、工程实现关键点

### 1. 控制搜索宽度和深度

必须限制：

- 最大深度
- 每层候选数量
- 最大 token 成本
- 最大执行时间

### 2. 评分器要稳定

评分器不稳定会导致选错路径。复杂任务可以使用多评分器投票。

### 3. 支持剪枝

低分路径应尽早剪掉，避免搜索爆炸。

### 4. 保存搜索轨迹

搜索过程很重要，便于调试和解释：

```text
候选路径 → 分数 → 被保留 / 被剪枝原因
```

---

## 十二、与其它 Planner 的区别

| 架构 | 区别 |
|------|------|
| ReAct | ReAct 通常走单一路径，Tree Search 同时探索多路径 |
| Plan-and-Execute | Plan-and-Execute 生成一个计划，Tree Search 生成多个候选计划 |
| Reflexion | Reflexion 多轮改进，Tree Search 同轮探索多路径 |
| LLMCompiler | LLMCompiler 编译任务图，Tree Search 搜索候选路径 |
| Multi-Agent | Multi-Agent 强调角色分工，Tree Search 强调搜索空间探索 |

---

## 十三、总结

Tree / Graph Search Planner 适合复杂推理和高正确率任务。它的核心价值是：

```text
不把希望寄托在单次生成上，而是生成多个候选、比较后选择更优解
```

如果任务简单或成本敏感，不建议使用该架构；如果任务复杂且允许较高成本，它可以显著提升结果质量。
