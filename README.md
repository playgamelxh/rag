## Project Description
RAG learn

## RAG step
* Data Chunking(数据分片)
* Chunk Vectorisation(分片数据向量化)
* Vector Data Store(向量数据存储)
* Data Retrieval(数据检索召回)
* Reranking of Retrieval Data(召回数据重排)
* LLM Query Generation(大模型查询生成)

## Data Chunking
- 基于大模型的语义感知LlamaIndex SemanticSplitter

## Chunk Vectorisation
- 中小规模文本、实时性要求高：Sentence-BERT（如 all-MiniLM-L6-v2）、USE 轻量版。
- 长文本（如论文、报告）：gte-large、Longformer、Cohere Command。
- 多语言场景：mMiniLM-L12-v2（多语言版）、USE 多语言版。
- 低资源环境：FastText、MiniLM 等轻量模型。

## Vector Data Store
1. Pinecone，云原生托管向量数据库（无需自建维护，按使用付费）。
2. Milvus，开源分布式向量数据库，支持本地部署和云原生。
3. FAISS（Facebook AI Similarity Search）开源向量检索库（严格来说是 “检索工具包”，非完整数据库）。
4. Weaviate，Pinecone 的替代者，开源向量数据库，支持本地部署和云服务。
5. Qdrant，轻量级开源向量数据库，主打简单易用。
6. Elasticsearch（向量检索增强版），传统搜索引擎，7.0 + 版本支持向量字段，可作为向量数据库使用。
7. Chroma，轻量级开源向量数据库，专为 AI 应用设计。

选择建议 
   - 快速上线，无运维：优先 Pinecone、Weaviate 云服务。
   - 私有化部署，大规模数据：Milvus。
   - 轻量、简单、开源：Qdrant、Chroma。
   - 极致性能，嵌入到代码：FAISS。
   - 已有 ES 集群，需混合检索：Elasticsearch。
## Data Retrieval
#### bge-M3

## Reranking of Retrieval Data 

## LLM Query Generation

## Open Code
1. Python
    - https://github.com/run-llama/llama_index
    - https://github.com/openai/openai-python
    - https://github.com/langchain-ai/langchain
    - https://github.com/chonkie-inc/chonkie
    - https://github.com/volcengine/ai-app-lab
2. Go
   - https://github.com/sashabaranov/go-openai
