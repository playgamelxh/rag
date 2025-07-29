from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os

# 1. 加载文档（以本地文本文件为例）
documents = SimpleDirectoryReader(input_files=["example_document.txt"]).load_data()
print(f"加载文档：{len(documents)} 个文档")

# # 2. 初始化嵌入模型（用于计算语义向量）
# # 可选：OpenAI Embedding（需API密钥）、Sentence-BERT（开源本地模型）等
# # os.environ["OPENAI_API_KEY"] = ""
# # embed_model = OpenAIEmbedding(model_name="text-embedding-3-small")
# embed_model = OpenAIEmbedding(model_name="text-embedding-ada-002")
#
# # 3. 配置 SemanticSplitter
# semantic_splitter = SemanticSplitterNodeParser(
#     embedding_model=embed_model,
#     chunk_size=50,  # 目标分片长度（字符数）
#     chunk_overlap=15,  # 分片重叠字符数
#     similarity_threshold=0.7  # 语义相似度阈值（低于此值则分割）
# )

# 初始化开源嵌入模型（如 BGE-M3）
embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-m3",
    device="cpu"  # 可选：指定设备，如 "cuda" 用于GPU加速
)
semantic_splitter = SemanticSplitterNodeParser(
    embed_model=embed_model,
    chunk_size=300,  # 目标分片长度（字符数），核心参数
    chunk_overlap=30,  # 分片重叠长度，帮助保持上下文连贯性
    max_chunk_size=500,      # 强制最大长度（超过则无论语义如何都分割）
    min_chunk_size=50,       # 防止过短分片
    similarity_threshold=0.65  # 根据需求调整阈值
)

# 4. 执行语义分片
nodes = semantic_splitter.get_nodes_from_documents(documents)
print(f"语义分片完成：{len(nodes)} 个分片")

# 5. 查看分片结果
for i, node in enumerate(nodes[:3]):  # 打印前3个分片
    print(f"\n分片 {i+1}（长度：{len(node.text)}）：")
    print(node.text[:200] + "...")  # 预览前200字符
#     print(node.text)  # 预览前200字符
