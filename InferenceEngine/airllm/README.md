## 简介
AirLLM 是一个开源的大模型推理优化库，核心是用极低显存跑超大模型：4GB 显存可跑 70B 模型，8GB 显存可跑 405B 模型（如 Llama 3.1），且无需量化、蒸馏、剪枝。

## 一、核心原理（一句话懂）
LLM 由多层 Transformer 组成，推理时每层只依赖前一层输出。AirLLM 采用分层推理（Layered Inference）：
只把当前需要计算的层加载到 GPU
算完立即释放显存，再加载下一层
配合元设备加载（只读结构、不读参数）+ Flash Attention 优化，把显存占用压到极低。
## 二、核心优势
极低显存门槛：4GB 跑 70B，8GB 跑 405B
原生精度：不做量化 / 蒸馏 / 剪枝，保持模型原始效果
自动适配：支持 Llama、Qwen、Mistral、ChatGLM、Baichuan、InternLM 等主流模型
简单易用：一行代码加载、一行生成
多平台：Linux、macOS、Windows 均可
## 三、快速上手（5 分钟）
1. 安装
```
pip install airllm
```
2. 一行代码跑 70B（4GB 显存即可）
```
from airllm import AutoModel

# 加载模型（自动分层、自动适配）
model = AutoModel.from_pretrained("lmsys/vicuna-70b-v1.5")

# 生成文本
prompt = "写一段关于AI的介绍"
output = model.generate(prompt, max_length=200)
print(output)

```
3. 关键参数（按需调整）
```
model.generate(
    prompt,
    max_length=512,        # 生成长度
    temperature=0.7,        # 随机性
    top_p=0.9,
    use_quantization=True,  # 开启4/8位块量化（提速3倍）
    device="cuda"           # 或 "cpu" / "mps"（Mac）
)
```

## 四、适用场景
* 个人 / 小团队低成本跑大模型（不用买 A100/H100）
* 边缘设备、笔记本、低配服务器部署大模型
* 快速验证大模型效果，无需云服务
* 教学 / 研究：在普通硬件上体验 70B+ 模型
## 五、与 Ollama、vLLM 对比

| 方案 |	显存要求 | 模型大小     | 特点 |
| --- | --- |----------| --- |
| AirLLM | 4GB 跑 70B | 	最大 405B | 分层加载、原生精度、极简代码 |
| Ollama |	70B 需～35GB	| 最大 70B   | 	封装友好、本地部署快 |
| vLLM |	70B 需～80GB	| 最大 70B	| 高吞吐、适合服务化 |
## 六、注意事项
速度较慢：分层加载会有磁盘 I/O，适合单请求、非实时场景
磁盘空间：70B 模型需～130GB 磁盘空间（存放分层权重）
量化可选：开启 use_quantization=True 可提速 2–3 倍，精度几乎无损

