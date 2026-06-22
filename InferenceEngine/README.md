## LLM Inference Engine（大模型推理引擎）

### 一、简介

LLM 推理引擎是负责把大语言模型从“训练好的权重”变成“可对外提供文本生成能力”的核心运行系统。它连接模型、显存、CPU、磁盘、请求队列和服务接口，决定模型在真实环境中的推理速度、吞吐能力、显存占用、并发能力和部署复杂度。

简单理解：

```
模型权重 + Tokenizer + 推理引擎 + 硬件资源 → 可调用的大模型服务
```

推理引擎不仅仅是执行 `model.generate()`，还会处理 KV Cache、批处理、显存管理、量化、模型并行、请求调度、流式输出和 OpenAI API 兼容服务等能力。

### 二、为什么需要推理引擎

大模型推理与普通深度学习模型推理不同，主要难点在于：

| 难点 | 说明 |
|------|------|
| 模型参数巨大 | 7B、13B、70B 模型会占用大量显存和磁盘 |
| 自回归生成慢 | 每次生成一个 token，都要基于已有上下文继续计算 |
| KV Cache 占用高 | 长上下文和高并发会快速消耗显存 |
| 并发调度复杂 | 多用户请求长度不同，需要高效调度 |
| 部署形态多样 | 本地运行、API 服务、边缘设备、GPU 集群需求不同 |

因此，不同推理引擎会围绕不同目标做优化：有的追求高吞吐，有的追求低显存，有的追求本地易用，有的适合生产服务化部署。

### 三、核心技术点

#### 1. KV Cache

Transformer 解码阶段会重复使用历史 token 的 Key / Value。KV Cache 可以避免重复计算历史上下文，是 LLM 推理性能的关键。

```
Prompt 计算 → 保存 KV Cache → 每生成一个新 token 复用历史 KV
```

#### 2. Continuous Batching（连续批处理）

传统 batch 要等一批请求全部结束后才能处理下一批。连续批处理允许新请求动态加入、已完成请求动态退出，提升 GPU 利用率。

#### 3. PagedAttention

PagedAttention 将 KV Cache 像操作系统分页内存一样管理，减少显存碎片，提高长上下文和高并发下的显存利用率。vLLM 是该技术的代表。

#### 4. 量化

通过 INT8、INT4、GPTQ、AWQ、GGUF 等方式降低模型权重占用，让消费级显卡或 CPU 也能运行更大的模型。

#### 5. 模型并行

当单张 GPU 放不下模型时，可以通过 Tensor Parallel、Pipeline Parallel 等方式把模型切分到多张 GPU 上。

#### 6. Speculative Decoding（投机解码）

使用小模型先生成候选 token，再由大模型验证，从而加速生成过程。

### 四、常见推理引擎与工具

| 名称 | 核心定位 | 适合场景 | 目录 |
|------|----------|----------|------|
| AirLLM | 极低显存运行超大模型 | 本地低显存、研究验证 | [airllm](airllm/README.md) |
| vLLM | 高吞吐在线推理服务 | 生产 API、高并发服务 | [vllm](vllm/README.md) |
| Ollama | 本地大模型运行与管理 | 个人电脑、本地开发 | [ollama](ollama/README.md) |
| LM Studio | 本地大模型桌面应用 | 图形界面、本地体验、模型管理 | [lmstudio](lmstudio/README.md) |
| llama.cpp | CPU / 边缘设备推理 | 低资源环境、GGUF 模型 | [llama_cpp](llama_cpp/README.md) |
| TensorRT-LLM | NVIDIA GPU 极致性能 | 企业级 GPU 部署 | [tensorrt_llm](tensorrt_llm/README.md) |
| SGLang | 结构化生成与服务化推理 | Agent、多轮对话、复杂推理 | [sglang](sglang/README.md) |
| LMDeploy | 国产模型部署优化 | 通义、InternLM、Qwen 等部署 | [lmdeploy](lmdeploy/README.md) |
| Transformers | 通用模型加载与推理 | 学习、实验、原型验证 | [transformers](transformers/README.md) |
| MLX | Apple Silicon 机器学习框架 | Mac 本地推理、微调、研究 | [mlx](mlx/README.md) |

### 五、按类型分类

#### 1. 本地易用型

| 名称 | 特点 |
|------|------|
| LM Studio | 图形界面，适合快速下载、管理和运行本地模型 |
| Ollama | 命令行和 API 体验好，适合开发者集成本地模型 |

#### 2. 低资源 / 量化型

| 名称 | 特点 |
|------|------|
| llama.cpp | GGUF 生态成熟，适合 CPU、Mac、边缘设备 |
| AirLLM | 通过分层加载降低显存门槛，适合低显存跑超大模型 |

#### 3. 服务化高吞吐型

| 名称 | 特点 |
|------|------|
| vLLM | PagedAttention 和连续批处理，适合高并发 API 服务 |
| SGLang | 兼顾高性能推理和复杂生成流程，适合 Agent 场景 |
| LMDeploy | 部署链路完整，对 Qwen、InternLM 等模型友好 |

#### 4. 硬件厂商优化型

| 名称 | 特点 |
|------|------|
| TensorRT-LLM | NVIDIA GPU 极致优化，适合企业级生产部署 |
| MLX | Apple Silicon 优化，适合 Mac 本地推理、训练和微调 |

#### 5. 研究学习型

| 名称 | 特点 |
|------|------|
| Transformers | 最适合理解模型加载、Tokenizer 和 generate 流程 |
| MLX | 适合在 Apple Silicon 上研究训练、微调和推理 |

### 六、如何选择推理引擎

#### 个人本地使用

- 想用图形界面快速运行模型：优先 LM Studio
- 想用命令行和 API 快速运行本地模型：优先 Ollama
- 想在 CPU 或低显存设备上运行：优先 llama.cpp
- 想用极低显存跑超大模型：优先 AirLLM

#### Mac / Apple Silicon

- 想简单聊天和体验模型：优先 LM Studio 或 Ollama
- 想运行 GGUF 量化模型：优先 llama.cpp、LM Studio 或 Ollama
- 想做模型研究、训练或 LoRA 微调：优先 MLX

#### 服务化部署

- 高并发、OpenAI API 兼容服务：优先 vLLM
- NVIDIA GPU 极致性能：优先 TensorRT-LLM
- 复杂对话、Agent、结构化输出：优先 SGLang
- Qwen、InternLM 等模型部署：可考虑 LMDeploy 或 vLLM

#### 学习与研究

- 想理解模型加载、Tokenizer、generate 流程：优先 Transformers
- 想研究显存优化：AirLLM、vLLM、llama.cpp
- 想研究生产级调度：vLLM、SGLang、TensorRT-LLM
- 想研究 Apple Silicon 上的模型训练和推理：优先 MLX

### 七、对比总结

| 维度 | AirLLM | vLLM | Ollama | LM Studio | llama.cpp | TensorRT-LLM | SGLang | LMDeploy | Transformers | MLX |
|------|--------|------|--------|-----------|-----------|--------------|--------|----------|--------------|-----|
| 易用性 | 高 | 中 | 很高 | 很高 | 中 | 低 | 中 | 中 | 高 | 中 |
| 吞吐能力 | 低 | 很高 | 中 | 中 | 中 | 很高 | 高 | 高 | 低/中 | 中 |
| 显存优化 | 很强 | 很强 | 中 | 中 | 很强 | 强 | 强 | 强 | 一般 | 强 |
| CPU 支持 | 部分 | 弱 | 支持 | 支持 | 很强 | 弱 | 弱 | 弱 | 支持 | 支持 |
| Mac 友好 | 中 | 弱 | 强 | 强 | 强 | 弱 | 中 | 中 | 中 | 很强 |
| 生产部署 | 弱 | 很强 | 中 | 弱 | 中 | 很强 | 强 | 强 | 中 | 弱 |
| 训练 / 微调 | 弱 | 弱 | 弱 | 弱 | 弱 | 弱 | 弱 | 中 | 强 | 强 |
| 学习成本 | 低 | 中 | 低 | 低 | 中 | 高 | 中 | 中 | 低 | 中 |

### 八、学习路线建议

1. 先使用 Transformers 理解 LLM 推理基本流程。
2. 使用 LM Studio 或 Ollama 快速体验本地模型运行。
3. 使用 llama.cpp 理解量化模型和低资源部署。
4. 使用 vLLM 学习高吞吐服务化推理。
5. 如果使用 Mac 并关注训练、微调或研究，可以学习 MLX。
6. 根据硬件和业务场景深入 AirLLM、TensorRT-LLM、SGLang 或 LMDeploy。

### 九、常见部署形态

```
本地图形界面体验：LM Studio
本地命令行 / API：Ollama
本地实验：Transformers / Ollama / LM Studio / llama.cpp
Mac 本地训练与微调：MLX
低显存大模型：AirLLM / llama.cpp
高并发 API：vLLM / SGLang / LMDeploy
NVIDIA 极致优化：TensorRT-LLM
Apple Silicon 优化：MLX
边缘设备：llama.cpp / Ollama
```

### 十、注意事项

- 推理速度不仅取决于模型大小，也取决于上下文长度、batch size、KV Cache、量化方式和硬件带宽。
- 低显存方案通常会牺牲速度，高吞吐方案通常需要更强 GPU。
- 量化可以显著降低显存占用，但可能带来轻微精度损失。
- LM Studio 和 Ollama 更适合本地易用场景，不是高并发生产服务首选。
- MLX 更适合 Apple Silicon 上的研究、微调和本地模型开发，不适合 NVIDIA GPU 服务端部署。
- 生产部署要重点关注并发、限流、监控、日志、安全和模型热更新。
- OpenAI API 兼容接口可以降低业务系统接入成本。
