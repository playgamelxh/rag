from llama_index.core import SimpleDirectoryReader
from llama_index.core.text_splitter import SemanticSplitterNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding
import os

# 1. 加载文档（以本地文本文件为例）
documents = SimpleDirectoryReader(input_files=["example_document.txt"]).load_data()
print(f"加载文档：{len(documents)} 个文档")

# 2. 初始化嵌入模型（用于计算语义向量）
# 可选：OpenAI Embedding（需API密钥）、Sentence-BERT（开源本地模型）等
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
embed_model = OpenAIEmbedding(model_name="text-embedding-3-small")

# 3. 配置 SemanticSplitter
semantic_splitter = SemanticSplitterNodeParser(
    embedding_model=embed_model,
    chunk_size=512,  # 目标分片长度（字符数）
    chunk_overlap=50,  # 分片重叠字符数
    similarity_threshold=0.7  # 语义相似度阈值（低于此值则分割）
)

# 4. 执行语义分片
nodes = semantic_splitter.get_nodes_from_documents(documents)
print(f"语义分片完成：{len(nodes)} 个分片")

# 5. 查看分片结果
for i, node in enumerate(nodes[:3]):  # 打印前3个分片
    print(f"\n分片 {i+1}（长度：{len(node.text)}）：")
    print(node.text[:200] + "...")  # 预览前200字符
