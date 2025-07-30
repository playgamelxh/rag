from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SemanticSplitterNodeParser, SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os


# 1. 预处理文档（确保段落分隔）
with open("example_document.txt", "r", encoding="utf-8") as f:
    content = f.read()
# 增强段落分割（根据文档实际标点调整）
content = content.replace("。", "。\n").replace("！", "！\n").replace("？", "？\n").replace("中新网", "\n中新网")
with open("example_document.txt", "w", encoding="utf-8") as f:
    f.write(content)

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
# print(embed_model)

# 测试嵌入模型是否正常 结果：模型正常，生成向量维度：1024
test_text = "测试嵌入模型是否工作"
try:
    embedding = embed_model.get_text_embedding(test_text)
    print(f"模型正常，生成向量维度：{len(embedding)}")  # 正常应为768维（bge-m3输出）
except Exception as e:
    print(f"嵌入模型异常：{e}")  # 若报错，需检查模型下载/环境

# 4. 规则预分块（确保多分片）
rule_splitter = SentenceSplitter(
    chunk_size=300,
    chunk_overlap=30,
    separator="\n"  # 按换行分割
)
pre_nodes = rule_splitter.get_nodes_from_documents(documents)
print(f"规则预分块：{len(pre_nodes)} 个分片")

semantic_splitter = SemanticSplitterNodeParser(
    embed_model=embed_model,
    chunk_size=200,  # 目标分片长度（字符数），核心参数
    chunk_overlap=30,  # 分片重叠长度，帮助保持上下文连贯性
    max_chunk_size=300,      # 强制最大长度（超过则无论语义如何都分割）
    min_chunk_size=30,       # 防止过短分片
    similarity_threshold=0.85  # 根据需求调整阈值
)

# 4. 执行语义分片
nodes = semantic_splitter.get_nodes_from_documents(pre_nodes)
print(f"语义分片完成：{len(nodes)} 个分片")

# 5. 查看分片结果
# for i, node in enumerate(nodes[:3]):  # 打印前3个分片
for i, node in enumerate(nodes):  # 打印前3个分片
    print(f"\n分片 {i+1}（长度：{len(node.text)}）：")
    print(node.text[:200] + "...")  # 预览前200字符
#     print(node.text)  # 预览全部字符

