## 简介

LMDeploy 是 OpenMMLab 推出的面向大语言模型和多模态模型的部署工具链，重点优化模型推理、量化和服务化部署。它对 InternLM、Qwen、Llama 等模型生态支持较好，适合中文和国产模型部署实践。

## 一、核心原理（一句话懂）

LMDeploy 通过 TurboMind 推理引擎、模型量化、KV Cache 优化和服务接口封装，把开源大模型高效部署为可调用的本地或在线服务。

```
模型权重 → LMDeploy 转换/量化 → TurboMind 推理 → API 服务
```

## 二、核心优势

- 部署链路完整：支持聊天、量化、服务化、压测等流程
- 中文模型友好：对 InternLM、Qwen 等模型支持较好
- 推理性能强：TurboMind 引擎面向高效服务化推理
- 支持量化：降低显存占用，提升部署灵活性
- API 兼容：可提供 OpenAI 风格接口

## 三、快速上手

1. 安装

```bash
pip install lmdeploy
```

2. 本地聊天

```bash
lmdeploy chat Qwen/Qwen2.5-7B-Instruct
```

3. 启动 API 服务

```bash
lmdeploy serve api_server Qwen/Qwen2.5-7B-Instruct \
  --server-name 0.0.0.0 \
  --server-port 23333
```

4. 调用服务

```bash
curl http://localhost:23333/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2.5-7B-Instruct",
    "messages": [{"role": "user", "content": "介绍一下 LMDeploy"}]
  }'
```

## 四、关键能力

| 能力 | 说明 |
|------|------|
| TurboMind | LMDeploy 的高性能推理后端 |
| Quantization | 支持权重量化，降低部署成本 |
| API Server | 提供服务化接口 |
| Pipeline Chat | 支持本地快速对话测试 |
| Benchmark | 可用于推理性能评估 |

## 五、适用场景

- Qwen、InternLM 等模型部署
- 中文大模型服务化
- 企业内部模型 API 服务
- 需要量化降低显存成本的场景
- 模型部署、压测、评估一体化流程

## 六、与其他引擎对比

| 方案 | 定位 | 特点 |
|------|------|------|
| LMDeploy | 模型部署工具链 | 中文模型友好，流程完整 |
| vLLM | 高吞吐通用服务 | 社区生态广，生产常用 |
| SGLang | 复杂生成流程 | 适合 Agent 和结构化输出 |
| TensorRT-LLM | NVIDIA 极致性能 | 性能强但部署复杂 |

## 七、注意事项

- 不同模型架构的支持程度需要查看对应版本文档。
- 量化模型部署前要评估精度损失。
- 生产环境应补充鉴权、限流、监控和日志。
- 如果目标是最通用的 OpenAI API 高并发服务，vLLM 也是常见选择。
