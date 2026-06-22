# 后端开发转 AI 算法工程师学习路线

## 一、目标定位

你当前的背景是后端开发，目标是转向 AI 算法工程师。这个转型不是从零开始，因为后端开发已经具备以下优势：

- 编程能力较强，理解工程结构、模块拆分、服务部署
- 熟悉 API、数据库、缓存、消息队列、系统设计等工程化能力
- 更容易理解模型服务化、RAG 系统、推理部署、训练平台和 MLOps
- 对线上稳定性、性能优化、日志监控、接口设计更敏感

AI 算法工程师需要在工程能力基础上补齐：

```text
数学基础 + 机器学习 + 深度学习 + 大模型原理 + 训练/微调 + 推理部署 + 算法项目经验
```

最终目标不是只会调用模型 API，而是能够理解模型原理、训练模型、评估模型、优化模型，并把模型能力落地到真实业务系统中。

---

## 二、当前已有基础评估

根据当前仓库内容，假设以下模块已经有一定程度掌握：

| 已有模块 | 对应能力 | 当前评估 |
|----------|----------|----------|
| `MLP` | 神经网络基础、前向传播、反向传播、分类任务 | 已入门 |
| `CNN` | 卷积神经网络、图像分类、CIFAR10 | 已入门 |
| `Framework/PyTorch` | PyTorch 基础、张量、模型定义、训练流程 | 已入门 |
| `RAG` | 数据切分、向量化、向量库、检索、重排 | 已入门到进阶 |
| `FineTuning` | 全量微调、LoRA、冻结微调、指令微调 | 已入门 |
| `InferenceEngine` | AirLLM、vLLM、Ollama、llama.cpp、MLX 等推理引擎 | 已具备部署认知 |
| `docs/transformer` | QKV、Transformer 相关资料 | 已有基础材料 |

### 当前综合完成度估计

| 能力方向 | 完成度 | 说明 |
|----------|--------|------|
| Python / 工程基础 | 75% | 后端背景具备优势，但需进一步熟悉 AI 工程工具链 |
| PyTorch 基础 | 45% | 已有基础代码，需要系统化训练循环、Dataset、评估、调参 |
| 传统机器学习 | 20% | 仓库中较少体现，需要补齐 sklearn、特征工程和经典算法 |
| 数学基础 | 25% | 需要系统补齐线代、概率统计、优化方法 |
| 深度学习基础 | 40% | 已有 MLP/CNN，需补齐正则化、优化器、归一化、序列模型 |
| Transformer / LLM 原理 | 35% | 已有 QKV/推理/微调资料，需要系统化理解架构和训练流程 |
| RAG 应用 | 60% | 已有较完整模块，可继续加强评估和工程化 |
| 微调能力 | 45% | 已有文档基础，需要完成可复现实验和评估 |
| 推理部署 | 55% | 已有推理引擎文档，需要补齐实际服务化部署项目 |
| 算法项目作品 | 30% | 需要形成可展示的端到端项目 |
| 面试准备 | 20% | 需要整理算法题、ML/DL/LLM 高频问题 |

### 整体转型完成度

```text
当前估计：40% 左右
目标水平：能够胜任初中级 AI 算法工程师 / 大模型应用算法工程师
```

---

## 三、AI 算法工程师能力模型

### 1. 基础能力

| 能力 | 要求 |
|------|------|
| Python | 熟练使用 Python 做数据处理、模型训练、实验脚本 |
| 数学 | 理解线性代数、概率统计、微积分、优化方法 |
| 数据处理 | 熟悉 NumPy、Pandas、数据清洗、特征处理 |
| 实验能力 | 会设计实验、记录指标、分析误差、复现实验 |

### 2. 机器学习能力

| 能力 | 要求 |
|------|------|
| 经典算法 | 线性回归、逻辑回归、SVM、KNN、决策树、随机森林、GBDT、XGBoost |
| 特征工程 | 类别特征、数值特征、文本特征、归一化、标准化、缺失值处理 |
| 模型评估 | Accuracy、Precision、Recall、F1、AUC、PR 曲线、混淆矩阵 |
| 调参与验证 | 交叉验证、网格搜索、过拟合/欠拟合分析 |

### 3. 深度学习能力

| 能力 | 要求 |
|------|------|
| 神经网络基础 | MLP、激活函数、损失函数、反向传播 |
| 训练技巧 | BatchNorm、Dropout、学习率调度、权重初始化、梯度裁剪 |
| CNN | 卷积、池化、ResNet、图像分类和迁移学习 |
| 序列模型 | RNN、LSTM、GRU、Attention 基础 |
| Transformer | Self-Attention、Multi-Head Attention、LayerNorm、FFN、位置编码 |

### 4. 大模型能力

| 能力 | 要求 |
|------|------|
| LLM 架构 | GPT、BERT、T5、LLaMA、Qwen、DeepSeek 等基本差异 |
| Tokenizer | BPE、WordPiece、SentencePiece、特殊 token、上下文长度 |
| 训练流程 | 预训练、SFT、RLHF、DPO、偏好优化 |
| 微调 | Full Fine-Tuning、LoRA、QLoRA、Freeze Fine-Tuning、Instruction Tuning |
| 推理 | KV Cache、量化、连续批处理、PagedAttention、Speculative Decoding |
| 评估 | Perplexity、BLEU、ROUGE、准确率、人工评估、LLM-as-a-Judge |

### 5. AI 工程化能力

| 能力 | 要求 |
|------|------|
| 模型服务化 | FastAPI、OpenAI API 兼容接口、流式输出、并发控制 |
| 推理引擎 | vLLM、Ollama、llama.cpp、SGLang、LMDeploy、MLX、TensorRT-LLM |
| RAG 工程 | 文档解析、切分、向量化、召回、重排、生成、评估 |
| MLOps | 实验管理、模型版本、数据版本、监控、灰度发布 |
| 性能优化 | 显存优化、batch、量化、缓存、异步队列、GPU 利用率 |

---

## 四、学习路线总览

```text
阶段 0：明确方向和补齐环境
阶段 1：数学与数据基础
阶段 2：传统机器学习
阶段 3：深度学习系统化
阶段 4：Transformer 与 NLP
阶段 5：大模型训练、微调与评估
阶段 6：RAG 与大模型应用算法
阶段 7：推理部署与 AI 工程化
阶段 8：项目作品与面试准备
```

---

## 五、阶段学习路线

## 阶段 0：方向确认与环境准备

### 目标

明确自己要转向哪类 AI 算法岗位，并建立稳定实验环境。

### 岗位方向分类

| 方向 | 重点能力 | 适合后端转型程度 |
|------|----------|------------------|
| 传统算法工程师 | 机器学习、特征工程、业务建模 | 中 |
| 深度学习算法工程师 | PyTorch、CV/NLP、模型训练 | 中 |
| 大模型算法工程师 | Transformer、微调、评估、推理优化 | 高 |
| 大模型应用算法工程师 | RAG、Agent、微调、模型服务化 | 很高 |
| AI 平台 / 推理工程师 | 推理引擎、GPU、服务化、MLOps | 很高 |

### 推荐主线

结合后端背景，推荐优先路线：

```text
大模型应用算法工程师 → 大模型算法工程师 → AI 推理 / 平台工程能力增强
```

### 需要完成

- 熟悉 Conda / uv / pip / Python 虚拟环境
- 熟悉 JupyterLab / VSCode / PyCharm
- 熟悉 PyTorch GPU 环境
- 熟悉 Hugging Face 模型下载和加载
- 建立实验记录习惯

### 完成标准

- 能独立创建 Python AI 项目环境
- 能运行 PyTorch 训练脚本
- 能下载并运行 Hugging Face 模型
- 能记录实验参数和结果

### 当前完成度

```text
预计完成度：60%
```

---

## 阶段 1：数学与数据基础

### 目标

补齐算法工程师必须理解的数学基础，不要求推导所有公式，但要能理解模型背后的含义。

### 线性代数

必须掌握：

- 向量、矩阵、张量
- 矩阵乘法
- 转置、逆矩阵
- 特征值、特征向量
- 向量空间、基、维度
- 点积、余弦相似度
- SVD 和 PCA 的基本思想

重点理解：

```text
Embedding 本质上是向量表示
Attention 本质上大量使用矩阵乘法和相似度计算
推荐、检索、聚类都依赖向量空间
```

### 概率统计

必须掌握：

- 随机变量
- 条件概率
- 贝叶斯公式
- 期望、方差
- 常见分布：伯努利、二项、正态、泊松
- 最大似然估计
- 交叉熵
- KL 散度
- 置信区间和假设检验

重点理解：

```text
分类模型输出的是概率分布
交叉熵是分类任务最常见损失函数
LLM 本质上是在预测下一个 token 的概率分布
```

### 微积分与优化

必须掌握：

- 导数、偏导数
- 梯度
- 链式法则
- 梯度下降
- 随机梯度下降 SGD
- Momentum、Adam、AdamW
- 学习率和收敛

重点理解：

```text
反向传播 = 链式法则 + 梯度下降
训练模型 = 最小化损失函数
优化器决定参数如何更新
```

### 数据处理

必须掌握：

- NumPy 数组操作
- Pandas DataFrame
- 数据清洗
- 缺失值处理
- 异常值处理
- 数据分布分析
- 可视化：Matplotlib / Seaborn

### 建议产出

- `math/linear_algebra.md`
- `math/probability_statistics.md`
- `math/optimization.md`
- `data/numpy_pandas_demo.ipynb`

### 当前完成度

```text
预计完成度：25%
```

---

## 阶段 2：传统机器学习

### 目标

掌握经典机器学习算法，建立“特征 → 模型 → 评估 → 调参”的完整思维。

### 必学算法

#### 1. 监督学习

- 线性回归
- 逻辑回归
- KNN
- 朴素贝叶斯
- 决策树
- 随机森林
- GBDT
- XGBoost / LightGBM / CatBoost
- SVM

#### 2. 无监督学习

- K-Means
- DBSCAN
- 层次聚类
- PCA
- t-SNE / UMAP 基本理解

#### 3. 推荐与排序基础

- 协同过滤
- 矩阵分解
- Learning to Rank 基础
- 召回、粗排、精排基本架构

### 评估指标

| 任务 | 指标 |
|------|------|
| 分类 | Accuracy、Precision、Recall、F1、AUC |
| 回归 | MAE、MSE、RMSE、R² |
| 排序 | NDCG、MRR、MAP |
| 聚类 | Silhouette Score、ARI |
| 检索 | Recall@K、Precision@K、HitRate |

### 实战项目

1. Titanic 生存预测
2. 房价预测
3. 用户流失预测
4. 文本分类 baseline
5. 商品推荐 baseline

### 完成标准

- 能用 sklearn 完成分类、回归、聚类任务
- 能解释模型为什么过拟合或欠拟合
- 能做特征工程和调参
- 能写出完整实验报告

### 当前完成度

```text
预计完成度：20%
```

---

## 阶段 3：深度学习系统化

### 目标

在已有 MLP、CNN、PyTorch 基础上，系统掌握深度学习训练流程。

### PyTorch 必备能力

- Tensor 操作
- Autograd 自动求导
- Dataset / DataLoader
- nn.Module
- 损失函数
- 优化器
- 训练循环
- 验证循环
- 模型保存和加载
- GPU / MPS / CPU 设备管理
- mixed precision 混合精度训练

### 神经网络基础

- MLP
- 激活函数：Sigmoid、Tanh、ReLU、GELU、SiLU
- 损失函数：MSE、CrossEntropy、BCE
- 反向传播
- 梯度消失和梯度爆炸
- 权重初始化
- 正则化
- Dropout
- BatchNorm / LayerNorm

### CNN

- 卷积核
- padding / stride
- pooling
- LeNet、AlexNet、VGG、ResNet
- 图像增强
- 迁移学习

### 序列模型

- RNN
- LSTM
- GRU
- Seq2Seq
- Attention

### 实战项目

1. MNIST MLP 分类重构
2. CIFAR10 CNN 分类优化
3. ResNet 图像分类
4. 文本情感分类
5. 使用 TensorBoard 记录训练过程

### 完成标准

- 能独立写完整 PyTorch 训练框架
- 能处理训练不收敛、过拟合、显存不足等问题
- 能解释常见网络结构和训练技巧

### 当前完成度

```text
预计完成度：40%
```

---

## 阶段 4：Transformer 与 NLP

### 目标

系统理解 Transformer，这是进入大模型算法方向的核心基础。

### NLP 基础

- 分词
- 词袋模型
- TF-IDF
- Word2Vec
- GloVe
- FastText
- 文本分类
- 序列标注
- 文本匹配
- 文本生成

### Transformer 必须掌握

- Token Embedding
- Position Embedding
- Self-Attention
- Multi-Head Attention
- Q / K / V
- Masked Attention
- Feed Forward Network
- Residual Connection
- LayerNorm
- Encoder / Decoder
- GPT / BERT / T5 架构差异

### 重点理解

```text
BERT：Encoder-only，适合理解类任务
GPT：Decoder-only，适合生成类任务
T5：Encoder-Decoder，适合文本到文本任务
LLM 主流架构多为 Decoder-only
```

### 实战项目

1. 手写简化 Self-Attention
2. 用 PyTorch 实现 Mini Transformer
3. 使用 BERT 做文本分类
4. 使用 GPT 类模型做文本生成
5. 对比不同 Tokenizer 的编码结果

### 完成标准

- 能画出 Transformer 架构图并解释每个模块
- 能解释 QKV 和 Attention 计算过程
- 能说明 BERT、GPT、T5 的区别
- 能使用 Hugging Face 完成 NLP 任务

### 当前完成度

```text
预计完成度：35%
```

---

## 阶段 5：大模型训练、微调与评估

### 目标

从“会用大模型”进阶到“理解大模型如何训练、如何微调、如何评估”。

### 预训练基础

- Causal Language Modeling
- Masked Language Modeling
- Next Token Prediction
- 数据清洗
- 数据去重
- 语料质量控制
- Token 数估算
- Scaling Law 基本概念

### 指令微调

- Instruction 数据格式
- Alpaca 格式
- ShareGPT 格式
- ChatML 格式
- 多轮对话构造
- 数据质量评估

### 微调方法

- Full Fine-Tuning
- Freeze Fine-Tuning
- LoRA
- QLoRA
- Prefix Tuning
- Prompt Tuning
- Adapter
- SFT
- DPO

### 训练工具

- Transformers Trainer
- PEFT
- TRL
- Accelerate
- DeepSpeed 基础
- LLaMA-Factory
- Axolotl

### 评估方法

| 类型 | 指标 / 方法 |
|------|-------------|
| 语言建模 | Perplexity |
| 摘要 | ROUGE |
| 翻译 | BLEU |
| 分类 | Accuracy / F1 |
| 检索增强 | Answer Correctness、Faithfulness |
| 对话 | 人工评估、LLM-as-a-Judge |

### 实战项目

1. 使用 LoRA 微调 Qwen 小模型
2. 构造一份领域指令数据集
3. 对比微调前后效果
4. 使用不同 rank 的 LoRA 做实验
5. 输出完整微调报告

### 完成标准

- 能说明各种微调方法的区别
- 能完成一次 LoRA / QLoRA 微调
- 能设计训练数据格式
- 能评估微调结果是否有效

### 当前完成度

```text
预计完成度：45%
```

---

## 阶段 6：RAG 与大模型应用算法

### 目标

基于已有 RAG 内容，进一步提升到可落地的企业级 RAG 算法能力。

### RAG 核心流程

```text
文档解析 → 数据清洗 → 文本切分 → 向量化 → 向量库 → 检索召回 → 重排 → Prompt 构造 → LLM 生成 → 评估
```

### 需要加强的知识点

#### 文档解析

- PDF 解析
- Word / HTML / Markdown 解析
- 表格解析
- OCR 基础
- 文档结构保留

#### Chunk 策略

- 固定长度切分
- 递归切分
- 语义切分
- Parent-Child Chunk
- Sliding Window
- 按标题层级切分

#### Embedding

- Sentence-BERT
- BGE
- E5
- GTE
- OpenAI Embedding
- 多语言 Embedding
- 向量维度和归一化

#### Retrieval

- 向量检索
- BM25
- Hybrid Search
- Multi-Query Retrieval
- Query Rewrite
- Metadata Filter

#### Rerank

- CrossEncoder
- BGE-Reranker
- Cohere Rerank
- LLM Rerank

#### 生成

- Prompt Template
- 引用来源
- 防幻觉
- 上下文压缩
- 多轮对话记忆

#### 评估

- Recall@K
- MRR
- NDCG
- Faithfulness
- Answer Relevance
- Context Precision
- Context Recall

### 实战项目

1. 企业知识库问答系统
2. PDF 文档问答系统
3. 混合检索 RAG
4. 带重排的 RAG
5. 带评估报告的 RAG Benchmark

### 完成标准

- 能独立实现完整 RAG Pipeline
- 能解释召回差、回答错、幻觉产生的原因
- 能通过评估指标优化 RAG 效果
- 能把 RAG 服务化成 API

### 当前完成度

```text
预计完成度：60%
```

---

## 阶段 7：推理部署与 AI 工程化

### 目标

发挥后端优势，把模型能力部署为稳定、可扩展、可监控的服务。

### 推理基础

- Token 生成流程
- KV Cache
- Prefill / Decode
- Batch Size
- Throughput / Latency
- TTFT
- TPOT
- 上下文长度

### 推理优化

- FP16 / BF16
- INT8 / INT4
- GPTQ / AWQ / GGUF
- PagedAttention
- Continuous Batching
- Speculative Decoding
- Tensor Parallel
- Pipeline Parallel

### 推理引擎

当前仓库已有以下内容，需要继续通过实践掌握：

- AirLLM
- vLLM
- Ollama
- LM Studio
- llama.cpp
- TensorRT-LLM
- SGLang
- LMDeploy
- Transformers
- MLX

### 服务化能力

- FastAPI
- OpenAI API 协议
- SSE 流式输出
- 请求队列
- 并发控制
- 超时控制
- 限流
- 鉴权
- 日志
- Prometheus 监控
- Docker 部署

### 实战项目

1. 使用 vLLM 部署 OpenAI 兼容 API
2. 使用 FastAPI 封装 RAG 服务
3. 使用 Ollama / LM Studio 做本地模型服务
4. 使用 llama.cpp 部署 GGUF 模型
5. 搭建模型服务监控面板

### 完成标准

- 能部署至少一种本地模型服务
- 能部署至少一种 GPU 推理服务
- 能实现流式输出接口
- 能监控模型服务延迟、吞吐和错误率

### 当前完成度

```text
预计完成度：55%
```

---

## 阶段 8：项目作品与面试准备

### 目标

形成可以展示的项目、简历亮点和面试知识体系。

### 推荐项目组合

#### 项目 1：传统机器学习项目

```text
用户流失预测 / 房价预测 / 风控评分
```

需要体现：

- 数据清洗
- 特征工程
- 模型训练
- 指标评估
- 模型解释

#### 项目 2：深度学习项目

```text
图像分类 / 文本分类 / 情感分析
```

需要体现：

- PyTorch 训练流程
- 模型结构设计
- 训练优化
- 过拟合分析
- 实验记录

#### 项目 3：RAG 知识库项目

```text
企业文档知识库问答系统
```

需要体现：

- 文档解析
- Chunk 策略
- Embedding
- 向量检索
- Rerank
- Prompt 优化
- RAG 评估

#### 项目 4：大模型微调项目

```text
基于 Qwen / Llama 的领域指令微调
```

需要体现：

- 数据构造
- LoRA / QLoRA
- 训练参数
- 效果对比
- 评估报告

#### 项目 5：模型服务化项目

```text
OpenAI API 兼容的大模型推理服务
```

需要体现：

- vLLM / SGLang / Ollama 部署
- FastAPI 封装
- 流式输出
- 并发控制
- 监控和日志

### 面试知识清单

#### 机器学习

- 逻辑回归原理
- 决策树如何分裂
- GBDT 和 XGBoost 区别
- 过拟合如何解决
- AUC 如何理解
- L1 / L2 正则区别

#### 深度学习

- 反向传播原理
- BatchNorm 和 LayerNorm 区别
- Dropout 作用
- Adam 和 SGD 区别
- 梯度消失 / 梯度爆炸
- ResNet 为什么有效

#### Transformer / LLM

- Attention 计算公式
- QKV 分别是什么
- BERT 和 GPT 区别
- 为什么 LLM 使用 Decoder-only
- KV Cache 是什么
- LoRA 原理
- SFT 和 DPO 区别

#### RAG

- RAG 为什么能降低幻觉
- Chunk 太大或太小有什么问题
- 向量检索和 BM25 区别
- Rerank 为什么有效
- 如何评估 RAG 系统
- 如何优化召回率

#### 工程化

- 如何部署大模型 API
- 如何实现流式输出
- 如何做限流和超时控制
- 如何降低推理延迟
- 如何监控模型服务
- 如何进行模型版本管理

### 当前完成度

```text
预计完成度：30%
```

---

## 六、总体进度评估

| 阶段 | 内容 | 当前完成度 | 优先级 |
|------|------|------------|--------|
| 阶段 0 | 方向确认与环境准备 | 60% | 高 |
| 阶段 1 | 数学与数据基础 | 25% | 高 |
| 阶段 2 | 传统机器学习 | 20% | 高 |
| 阶段 3 | 深度学习系统化 | 40% | 高 |
| 阶段 4 | Transformer 与 NLP | 35% | 高 |
| 阶段 5 | 大模型训练、微调与评估 | 45% | 高 |
| 阶段 6 | RAG 与大模型应用算法 | 60% | 高 |
| 阶段 7 | 推理部署与 AI 工程化 | 55% | 中高 |
| 阶段 8 | 项目作品与面试准备 | 30% | 高 |

### 当前整体完成度

```text
综合完成度：约 40%
```

### 近期最应该补齐的短板

```text
1. 数学基础
2. 传统机器学习
3. PyTorch 系统化训练流程
4. Transformer 原理
5. 可展示的端到端项目
```

---

## 七、优先级路线

如果目标是尽快转到 AI 算法工程师，建议优先顺序如下：

```text
1. 传统机器学习 + sklearn
2. PyTorch 系统训练能力
3. Transformer / LLM 原理
4. RAG 项目工程化
5. LoRA 微调项目
6. vLLM / Ollama / FastAPI 模型服务化
7. 面试题和项目复盘
```

如果目标是大模型应用算法工程师，建议优先顺序如下：

```text
1. Transformer / LLM 原理
2. RAG 系统优化
3. Embedding / Rerank / Prompt Engineering
4. LoRA / QLoRA 微调
5. LLM 评估
6. 推理部署和服务化
7. Agent 和工具调用
```

如果目标是 AI 推理 / 平台方向，建议优先顺序如下：

```text
1. PyTorch 模型加载与推理
2. KV Cache / Batch / 量化
3. vLLM / SGLang / llama.cpp
4. FastAPI / OpenAI API 协议
5. Docker / GPU 环境 / 监控
6. 性能压测和优化
```

---

## 八、后续 todo 清单

### 高优先级

- [ ] 系统学习线性代数、概率统计和优化方法
- [ ] 使用 sklearn 完成 3 个传统机器学习项目
- [ ] 重构 PyTorch 训练模板，形成通用训练框架
- [ ] 手写 Self-Attention 和 Mini Transformer
- [ ] 使用 Hugging Face 完成文本分类和文本生成任务
- [ ] 完成一个 LoRA 微调实验并输出报告
- [ ] 完成一个带评估的 RAG 项目
- [ ] 使用 vLLM 或 Ollama 部署模型 API
- [ ] 整理 50 个 AI 算法面试高频问题

### 中优先级

- [ ] 学习 XGBoost / LightGBM 并完成表格数据建模
- [ ] 学习 BGE / E5 / GTE 等 Embedding 模型
- [ ] 学习 BGE-Reranker 和 CrossEncoder
- [ ] 学习 DPO 和偏好优化基础
- [ ] 学习模型量化：INT8、INT4、GPTQ、AWQ、GGUF
- [ ] 学习 MLX 在 Mac 上的推理和微调流程
- [ ] 学习 SGLang 的结构化生成和 Agent 场景

### 低优先级

- [ ] 学习 TensorRT-LLM 深度优化
- [ ] 学习 DeepSpeed 分布式训练
- [ ] 学习 Kubernetes 上的模型服务部署
- [ ] 学习多模态模型基础
- [ ] 学习强化学习基础

---

## 九、建议新增仓库目录

后续可以逐步补充以下目录，让学习体系更完整：

```text
Math/
├── linear_algebra.md
├── probability_statistics.md
└── optimization.md

MachineLearning/
├── README.md
├── sklearn_basics.py
├── linear_regression.py
├── logistic_regression.py
├── decision_tree.py
├── random_forest.py
├── xgboost_lightgbm.md
└── model_evaluation.md

DeepLearning/
├── README.md
├── pytorch_training_template.py
├── optimizers.md
├── regularization.md
└── tensorboard.md

Transformer/
├── README.md
├── self_attention.py
├── mini_transformer.py
└── tokenizer.md

LLM/
├── README.md
├── pretraining.md
├── sft.md
├── dpo.md
├── evaluation.md
└── prompt_engineering.md

Projects/
├── ml_user_churn_prediction/
├── dl_text_classification/
├── rag_knowledge_base/
├── lora_finetuning_qwen/
└── llm_api_server/
```

---

## 十、阶段性验收标准

### 入门算法工程师标准

达到以下能力可以认为具备入门 AI 算法工程师能力：

- 能使用 sklearn 完成传统机器学习任务
- 能使用 PyTorch 训练简单神经网络
- 能解释 MLP、CNN、Transformer 基本原理
- 能完成文本分类、图像分类等基础任务
- 能独立评估模型效果

### 大模型应用算法工程师标准

达到以下能力可以认为具备大模型应用算法工程师能力：

- 能搭建完整 RAG 系统
- 能优化 Chunk、Embedding、Retrieval、Rerank、Prompt
- 能完成 LoRA 微调实验
- 能评估大模型应用效果
- 能部署本地或 GPU 大模型服务
- 能结合业务场景设计大模型解决方案

### 中级 AI 算法工程师标准

达到以下能力可以向中级水平靠近：

- 能根据业务问题选择合适模型方案
- 能设计训练数据和评估方案
- 能系统分析模型误差来源
- 能优化训练和推理性能
- 能完成从数据到模型服务的端到端项目
- 能指导初级同学完成模型实验和工程落地

---

## 十一、最终建议

从后端转 AI 算法工程师，不建议完全放弃后端优势，而是把后端能力变成差异化竞争力。

推荐定位：

```text
懂算法原理 + 懂大模型应用 + 懂模型部署 + 懂工程落地的 AI 算法工程师
```

这类能力组合非常适合当前大模型应用落地场景，尤其适合：

- 企业知识库 RAG
- 大模型应用平台
- 模型推理服务
- AI Agent 后端
- 领域模型微调
- AI 工程化和算法落地

下一阶段最重要的不是继续只看文档，而是形成 3 到 5 个可展示项目：

```text
1. 一个传统机器学习项目
2. 一个 PyTorch 深度学习项目
3. 一个完整 RAG 项目
4. 一个 LoRA 微调项目
5. 一个模型服务化部署项目
```

当这些项目完成后，整体转型完成度可以从当前约 40% 提升到 75% 以上。
