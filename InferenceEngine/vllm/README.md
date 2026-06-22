## 简介

vLLM 是一个面向大语言模型高吞吐在线推理的开源引擎，核心目标是让 GPU 在多用户、多请求场景下保持高利用率。它常用于把 Llama、Qwen、Mistral、ChatGLM 等模型部署成 OpenAI API 兼容服务。

## 一、核心原理（一句话懂）

vLLM 通过 PagedAttention 高效管理 KV Cache，并结合连续批处理（Continuous Batching）动态调度请求，从而在高并发场景下显著提升吞吐量。

```
请求队列 → 连续批处理 → PagedAttention 管理 KV Cache → GPU 高效生成 token
```

## 二、核心优势

- 高吞吐：适合多用户并发访问的大模型 API 服务
- 显存利用率高：PagedAttention 减少 KV Cache 显存碎片
- OpenAI API 兼容：业务系统接入成本低
- 模型支持广：支持 Hugging Face 上大量主流模型
- 服务化友好：适合容器化、网关、监控和生产部署

## 三、快速上手

1. 安装

```bash
pip install vllm
```

2. 启动 OpenAI API 兼容服务

```bash
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-7B-Instruct \
  --host 0.0.0.0 \
  --port 8000
```

3. 调用接口

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2.5-7B-Instruct",
    "messages": [{"role": "user", "content": "介绍一下 vLLM"}],
    "temperature": 0.7
  }'
```

## 四、关键参数

| 参数 | 作用 | 说明 |
|------|------|------|
| `--model` | 模型路径或 Hugging Face 模型名 | 必填 |
| `--tensor-parallel-size` | Tensor Parallel GPU 数量 | 多卡部署常用 |
| `--gpu-memory-utilization` | GPU 显存使用比例 | 默认会预留部分显存 |
| `--max-model-len` | 最大上下文长度 | 影响 KV Cache 显存 |
| `--dtype` | 权重精度 | auto、float16、bfloat16 等 |
| `--quantization` | 量化方式 | awq、gptq 等 |

## 五、适用场景

- 高并发大模型 API 服务
- OpenAI API 兼容部署
- RAG 系统中的 LLM 生成服务
- 企业内部模型服务平台
- 多用户共享 GPU 推理资源

## 六、与其他引擎对比

| 方案 | 定位 | 特点 |
|------|------|------|
| vLLM | 高吞吐服务化推理 | PagedAttention、连续批处理 |
| Ollama | 本地模型运行 | 易用，适合个人电脑 |
| llama.cpp | 低资源推理 | CPU、GGUF、边缘设备友好 |
| TensorRT-LLM | 极致 GPU 性能 | NVIDIA 深度优化，部署复杂度高 |

## 七、注意事项

- 更适合 NVIDIA GPU 服务化部署，不是低资源 CPU 推理首选。
- 上下文长度越大，KV Cache 显存占用越高。
- 并发能力与 GPU 显存、模型大小、输出长度强相关。
- 生产环境建议配合网关、限流、日志、监控和鉴权使用。
