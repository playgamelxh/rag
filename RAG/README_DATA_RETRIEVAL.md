## Data Retrieval（数据检索）

### 一、核心概念与定位

**数据检索**是 RAG 系统中根据用户查询从向量数据库中找到最相关文本分片的过程，是连接用户需求和知识库的关键环节。

**在 RAG 流程中的位置**：
```
Data Chunking → Chunk Vectorisation → Vector Data Store → Data Retrieval → Reranking → LLM Query Generation
```

**核心目标**：
- **高召回率**：尽可能多地找到与查询相关的文档
- **高精度**：返回的文档与查询真正相关
- **低延迟**：在毫秒级完成检索
- **可解释性**：能够解释检索结果的来源和相关性

---

### 二、检索流程详解

#### 标准检索流程

```
用户查询 → 查询向量化 → 向量相似度搜索 → 元数据过滤 → Top-K 结果返回 → 结果处理
```

#### 各阶段说明

##### 1. 用户查询

用户输入自然语言查询，例如：
- "如何配置 RAG 的向量数据库？"
- "什么是数据分块策略？"
- "BGE 模型和 E5 模型有什么区别？"

##### 2. 查询向量化

使用与文档分片相同的嵌入模型将查询转换为向量：

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('BAAI/bge-large-zh')
query = "如何配置 RAG 的向量数据库？"
query_vector = model.encode(query)
```

**关键要点**：
- 必须使用与文档向量化相同的模型
- 向量维度必须与数据库中存储的向量一致
- 建议对向量进行归一化处理（特别是使用余弦相似度时）

##### 3. 向量相似度搜索

通过向量数据库的 API 执行相似度搜索：

```python
# Milvus 示例
results = collection.search(
    data=[query_vector],
    anns_field="vector",
    param={"metric_type": "COSINE", "params": {"efSearch": 50}},
    limit=10
)
```

**常用相似度算法**：

| 算法 | 特点 | 适用场景 |
|------|------|----------|
| **余弦相似度** | 衡量方向相似度，不考虑长度 | 文本语义匹配（最常用） |
| **欧氏距离** | 衡量空间距离 | 图像识别、语音识别 |
| **内积** | 衡量投影重叠度 | 推荐系统、文本分类 |

##### 4. 元数据过滤

结合分片的元数据做前置或后置过滤：

```python
# 前置过滤（缩小检索范围）
results = collection.search(
    data=[query_vector],
    anns_field="vector",
    param={"metric_type": "COSINE"},
    limit=10,
    expr="source == '技术文档' && category == 'RAG'"
)
```

**常用元数据字段**：

| 字段 | 示例值 | 用途 |
|------|--------|------|
| `source` | "文档A.pdf" | 过滤特定来源的文档 |
| `category` | "技术文档" | 过滤特定类别的文档 |
| `timestamp` | "2024-01-01" | 过滤特定时间范围的文档 |
| `section` | "第3章" | 过滤特定章节 |

##### 5. Top-K 结果返回

返回相似度最高的前 K 个结果（通常 K=3~20）：

```python
for hit in results[0]:
    print(f"相似度: {hit.score:.4f}")
    print(f"文本: {hit.entity.get('text')}")
    print(f"来源: {hit.entity.get('source')}")
```

##### 6. 结果处理

对返回的结果进行后处理：

- **去重**：移除重复或高度相似的结果
- **排序**：按相似度分数排序
- **拼接**：将多个结果拼接为上下文文本

---

### 三、检索策略详解

#### 1. 单向量检索（Single Vector Retrieval）

**原理**：将用户查询转换为单个向量，与数据库中的所有向量进行相似度比较。

**特点**：
- **优点**：简单直接，计算效率高
- **缺点**：可能无法捕捉查询的多义性

**适用场景**：简单查询、明确意图的查询

#### 2. 多查询检索（Multi-Query Retrieval）

**原理**：使用 LLM 将单个查询扩展为多个相关查询，分别检索后合并结果。

**流程**：
```
用户查询 → LLM 生成多个变体查询 → 分别向量化 → 分别检索 → 合并去重 → 返回结果
```

**示例**：
```python
from langchain.retrievers import MultiQueryRetriever
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(temperature=0)
retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=llm
)
```

**优点**：
- 提升召回率
- 处理多义性查询
- 覆盖不同角度的语义

**缺点**：
- 增加计算成本（多次检索）
- 需要额外的 LLM 调用

**适用场景**：复杂查询、模糊查询、多义性查询

#### 3. 混合检索（Hybrid Search）

**原理**：结合向量语义检索和关键词检索（如 BM25）。

**策略**：

##### 策略 A：并行检索后合并

```
用户查询 → 向量检索 → Top-K 结果
        → BM25 检索 → Top-K 结果
        → 合并去重 → 重排序 → 返回结果
```

**示例**：
```python
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.vectorstores import Chroma

vector_retriever = Chroma.as_retriever(search_kwargs={"k": 10})
bm25_retriever = BM25Retriever.from_documents(documents)

ensemble_retriever = EnsembleRetriever(
    retrievers=[vector_retriever, bm25_retriever],
    weights=[0.7, 0.3]
)
```

##### 策略 B：向量 + 关键词融合

```
用户查询 → 向量化 + 关键词提取 → 向量检索（带关键词过滤） → 返回结果
```

**优点**：
- 避免纯向量检索漏掉关键词匹配的重要内容
- 提升召回率和精度
- 结合语义理解和精确匹配

**缺点**：
- 实现复杂
- 需要维护两套检索系统

**适用场景**：需要精确关键词匹配的场景、混合文档类型

#### 4. 上下文感知检索（Context-Aware Retrieval）

**原理**：结合对话历史或上下文信息进行检索。

**策略**：

##### 策略 A：拼接历史上下文

```
对话历史 + 当前查询 → 合并向量化 → 检索 → 返回结果
```

##### 策略 B：独立编码上下文

```
对话历史 → 编码为上下文向量
当前查询 → 编码为查询向量
上下文向量 + 查询向量 → 融合检索 → 返回结果
```

**优点**：
- 处理多轮对话
- 理解上下文依赖的查询
- 提升对话连贯性

**缺点**：
- 增加计算复杂度
- 需要处理长上下文

**适用场景**：对话式 AI、多轮问答系统

#### 5. 密集-稀疏混合检索（Dense-Sparse Retrieval）

**原理**：结合稠密向量（来自深度学习模型）和稀疏向量（来自传统方法）。

**策略**：
```
稠密向量检索 → Top-K 结果
稀疏向量检索 → Top-K 结果
合并重排序 → 返回结果
```

**优点**：
- 兼顾语义理解和精确匹配
- 提升检索精度

**缺点**：
- 需要存储两种类型的向量
- 实现复杂

**适用场景**：对检索精度要求极高的场景

---

### 四、检索优化技巧

#### 1. 查询扩展（Query Expansion）

**原理**：对用户查询进行扩展，增加相关词汇。

**方法**：

##### 同义词扩展
```python
from nltk.corpus import wordnet

def expand_query(query):
    expanded = [query]
    for word in query.split():
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                expanded.append(lemma.name())
    return list(set(expanded))
```

##### LLM 生成扩展
```python
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(temperature=0)
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个查询扩展助手。请为以下查询生成3-5个相关的查询变体。"),
    ("human", "{query}")
])
chain = prompt | llm
variants = chain.invoke({"query": query})
```

#### 2. 动态 Top-K 调整

**原理**：根据查询复杂度动态调整返回结果数量。

**策略**：
- 简单查询（短、明确）：K=3~5
- 中等查询（中等长度）：K=5~10
- 复杂查询（长、模糊）：K=10~20

#### 3. 结果去重

**原理**：移除重复或高度相似的检索结果。

**方法**：
- 基于文本内容去重
- 基于向量相似度去重（阈值 > 0.95）
- 基于来源和位置去重

#### 4. 渐进式检索（Progressive Retrieval）

**原理**：先进行快速粗检索，再进行精细检索。

**策略**：
```
快速粗检索（K=50）→ 精细重排序 → 返回 Top-K（K=10）
```

**优点**：
- 平衡速度和精度
- 减少精细检索的计算量

---

### 五、检索评估指标

#### 常用评估指标

| 指标 | 定义 | 计算方式 | 优化目标 |
|------|------|----------|----------|
| **Recall@K** | 前 K 个结果中包含相关文档的比例 | 相关文档数 / 总相关文档数 | 最大化 |
| **Precision@K** | 前 K 个结果中相关文档的比例 | 相关文档数 / K | 最大化 |
| **F1@K** | Recall 和 Precision 的调和平均 | 2 × Recall × Precision / (Recall + Precision) | 最大化 |
| **NDCG@K** | 归一化折损累积增益 | 考虑结果排序的质量 | 最大化 |
| **MRR** | 平均倒数排名 | 1 / 第一个相关结果的排名 | 最大化 |

#### 评估流程

```
准备测试集（查询 + 相关文档）→ 执行检索 → 计算指标 → 分析结果 → 优化策略
```

**示例**：
```python
from langchain.evaluation import load_evaluator

evaluator = load_evaluator("retrieval")
results = evaluator.evaluate(
    queries=queries,
    retriever=retriever,
    relevant_documents=relevant_docs
)
```

---

### 六、实践最佳实践

#### 1. 检索链路设计

**推荐架构**：
```
用户查询
    ↓
查询预处理（分词、扩展）
    ↓
多查询生成（可选）
    ↓
向量检索 + BM25 检索（混合检索）
    ↓
元数据过滤
    ↓
结果去重
    ↓
重排序（Reranking）
    ↓
Top-K 结果返回
```

#### 2. 参数调优指南

| 参数 | 推荐范围 | 调优建议 |
|------|----------|----------|
| **Top-K** | 3~20 | 根据查询复杂度调整 |
| **向量维度** | 768~1024 | BGE/E5 系列默认值 |
| **相似度算法** | 余弦相似度 | 文本检索首选 |
| **索引类型** | HNSW | 平衡精度与速度 |
| **efSearch** | 50~200 | 值越大精度越高但速度越慢 |

#### 3. 故障排查

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| **召回率低** | 查询表达不清晰 | 使用多查询检索或查询扩展 |
| **精度低** | 向量模型不合适 | 更换更合适的嵌入模型 |
| **延迟高** | 索引配置不当 | 优化索引参数或增加硬件资源 |
| **结果重复** | 分块策略问题 | 调整分块重叠率或增加去重逻辑 |

#### 4. 监控与日志

**建议监控指标**：
- 查询延迟（P50、P95、P99）
- 检索吞吐量（QPS）
- Recall@K、Precision@K
- 缓存命中率

**建议日志内容**：
- 查询文本
- 检索结果及相似度分数
- 元数据过滤条件
- 检索耗时

---

### 七、示例代码

#### 完整检索流程示例

```python
from sentence_transformers import SentenceTransformer
from pymilvus import connections, Collection

# 1. 连接向量数据库
connections.connect(host="localhost", port="19530")
collection = Collection("rag_chunks")

# 2. 加载嵌入模型
model = SentenceTransformer('BAAI/bge-large-zh')

# 3. 用户查询
query = "如何配置 RAG 的向量数据库？"

# 4. 查询向量化
query_vector = model.encode(query)

# 5. 向量相似度搜索
search_params = {
    "metric_type": "COSINE",
    "params": {"efSearch": 50}
}
results = collection.search(
    data=[query_vector],
    anns_field="vector",
    param=search_params,
    limit=10,
    expr="category == '技术文档'"
)

# 6. 结果处理
retrieved_docs = []
for hit in results[0]:
    doc = {
        "text": hit.entity.get("text"),
        "source": hit.entity.get("source"),
        "score": hit.score
    }
    retrieved_docs.append(doc)

# 7. 去重（基于文本相似度）
unique_docs = []
seen_texts = set()
for doc in retrieved_docs:
    text_hash = hash(doc["text"])
    if text_hash not in seen_texts:
        seen_texts.add(text_hash)
        unique_docs.append(doc)

# 8. 按分数排序
unique_docs.sort(key=lambda x: x["score"], reverse=True)

# 9. 返回 Top-5 结果
final_results = unique_docs[:5]
```

---

### 八、总结

**核心要点**：
1. **检索流程**：查询向量化 → 向量相似度搜索 → 元数据过滤 → Top-K 返回
2. **检索策略**：单向量检索是基础，混合检索和多查询检索能提升效果
3. **优化技巧**：查询扩展、动态 Top-K、结果去重、渐进式检索
4. **评估指标**：Recall@K、Precision@K、NDCG@K 是核心评估指标
5. **最佳实践**：设计完整的检索链路，合理调优参数，做好监控

**推荐组合**：
- **通用场景**：BGE 嵌入模型 + Milvus 向量数据库 + 余弦相似度 + Top-K=10
- **复杂查询**：多查询检索 + 混合检索 + 重排序
- **高精度要求**：密集-稀疏混合检索 + 精细重排序
