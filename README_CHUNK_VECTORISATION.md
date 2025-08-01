## Chunk_Vectorisation

#### 定义
Chunk Vectorisation（分片向量化） 是将文本分片（Chunks）转换为数值向量（Vectors）的关键步骤，目的是让计算机能够理解文本的语义，并通过向量之间的相似性进行高效检索。

#### 常用算法
常用的向量化算法（模型）主要分为传统文本嵌入算法和基于预训练语言模型（LLM）的嵌入算法

#### 一、传统文本嵌入算法
1. 词袋模型（Bag of Words, BoW）及衍生 
   - 原理：将文本视为词语的无序集合，统计词语出现频率作为向量特征（如独热编码、词频 TF 向量）
   - 局限：忽略词语顺序和语义关联，向量维度高（等于词汇表大小）。
   - 衍生：TF-IDF（词频 - 逆文档频率），通过权衡词语在文档和语料库中的重要性优化向量，是信息检索领域的经典方法。
2. Word2Vec
    - 原理：通过浅层神经网络（CBOW 或 Skip-gram 模型）学习词语的分布式表示，将词语映射到低维向量空间，向量相似度可反映语义相关性（如 “国王 - 男人 + 女人≈女王”）。
    - 局限：仅支持词语级向量，需通过拼接 / 平均等方式生成句子 / 文档向量，无法处理多义词和上下文变化。
3. GloVe（Global Vectors for Word Representation）
    - 原理：结合全局词频统计和局部上下文信息，通过最小化词向量与共现概率的误差学习表示，兼顾 Word2Vec 的局部语境和全局统计特性。
    - 应用：适合生成静态词向量，需进一步处理为长文本向量。
4. FastText
    - 原理：在 Word2Vec 基础上引入 “子词（n-gram）”，将词语拆分为字符级子词（如 “apple” 拆分为 “app”“ple”），支持未登录词（OOV）的向量生成，适合多语言或拼写不规则的场景。

#### 二、基于预训练语言模型（LLM）的嵌入算法
这类算法基于深层 Transformer 架构，通过大规模语料预训练学习上下文语义，能生成高质量的句子 / 文档级向量，是当前 RAG 系统的主流选择。
1. BERT 及衍生模型（句子级嵌入）
    - 原理：BERT（双向编码器表示）通过双向 Transformer 学习上下文依赖的词语表示，可通过 “[CLS]” 标记的隐藏状态或句子向量平均生成句子嵌入。
    - 衍生模型
        + Sentence-BERT（SBERT）：针对句子嵌入优化的 BERT 变体，通过对比学习（如孪生网络）使相似句子的向量更接近，支持高效的句子级相似度计算，速度比原生 BERT 快 100 倍以上，是 RAG 中最常用的模型之一。
        + MiniLM：轻量级 BERT 变体，参数更小（如 MiniLM-L6-H384 仅 660 万参数），适合资源受限场景，性能接近 SBERT。
2. 通用句子嵌入模型
    - Sentence Transformers 库中的模型：除 SBERT 外，还包括：
        + all-MiniLM-L6-v2：轻量高效，适合实时检索，支持多语言。
        + all-mpnet-base-v2：性能更强，向量维度 768，语义捕捉更精准，但计算成本较高。
    - USE（Universal Sentence Encoder）：谷歌推出的通用句子编码器，支持多种输入（句子、短语），有轻量版（Transformer 架构）和高效版（DAN 架构），适合跨语言场景。
3. 长文本专用嵌入模型
    - 原理：传统 LLM 对长文本（如超过 512 tokens）处理能力有限，长文本嵌入模型通过优化注意力机制或分段聚合支持更长输入。
    - 代表模型：
        + Cohere Command：支持长文本（最高 2048 tokens），语义理解能力强，适合文档级嵌入。
        + Longformer：通过稀疏注意力机制支持超长文本（如 4096 tokens），可直接对长文档生成嵌入向量。
        + gte-large：针对长文本优化的开源模型，支持 8192 tokens，适合 RAG 中长文档分片的向量化。
4. 多模态嵌入模型（支持文本 + 其他模态）
    - 若 RAG 系统涉及图片、表格等多模态数据，可使用多模态嵌入模型，如：
        + CLIP（Contrastive Language-Image Pretraining）：将文本和图片映射到同一向量空间，支持 “文本检索图片” 或 “图片检索文本”。
        + BLIP-2：通过桥接模型连接视觉编码器和语言模型，生成多模态嵌入向量，适合图文混合文档的向量化。

#### 三、算法选择建议
1. 优先选择场景：
   - 中小规模文本、实时性要求高：Sentence-BERT（如 all-MiniLM-L6-v2）、USE 轻量版。
   - 长文本（如论文、报告）：gte-large、Longformer、Cohere Command。
   - 多语言场景：mMiniLM-L12-v2（多语言版）、USE 多语言版。
   - 低资源环境：FastText、MiniLM 等轻量模型。
2. 工具库推荐：
   - 开源实现：sentence-transformers 库（集成多数主流模型）、huggingface-transformers。
   - 商业 API：OpenAI Embeddings（如 text-embedding-ada-002）、Cohere API，优点是无需本地部署，适合快速搭建。

#### 总结
RAG 系统中，向量化算法的核心目标是最大化向量对语义的表征能力，从而提升检索精度。实际应用中，需根据文本长度、资源限制、多模态需求等选择合适模型，其中 Sentence-BERT 系列 和 OpenAI Embeddings 因平衡性能和易用性，是目前 RAG 中最常用的向量化方案。


#### 开源项目
- https://github.com/run-llama/llama_index
