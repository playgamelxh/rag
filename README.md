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
2. Go
   - https://github.com/sashabaranov/go-openai
