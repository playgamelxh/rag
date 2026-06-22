## 简介

llama.cpp 是一个高性能、轻量级的大模型推理项目，最初用于在 CPU 上运行 LLaMA 模型，后来扩展支持多种模型架构、GPU 加速和 GGUF 量化格式。它是低资源设备和本地离线推理的重要方案。

## 一、核心原理（一句话懂）

llama.cpp 使用 C/C++ 实现高效推理内核，并通过 GGUF 量化模型降低内存占用，让大模型可以在 CPU、笔记本、边缘设备甚至移动设备上运行。

```
Hugging Face 模型 → 转换 GGUF → 量化 → llama.cpp 本地推理
```

## 二、核心优势

- 低资源友好：CPU 也能运行量化大模型
- 部署轻量：依赖少，适合嵌入式和边缘设备
- GGUF 生态成熟：大量模型提供 GGUF 版本
- 支持多后端：CPU、CUDA、Metal、Vulkan 等
- 离线可用：适合本地隐私场景

## 三、快速上手

1. 编译项目

```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
cmake -B build
cmake --build build --config Release
```

2. 运行 GGUF 模型

```bash
./build/bin/llama-cli \
  -m models/qwen2.5-7b-instruct-q4_k_m.gguf \
  -p "介绍一下 llama.cpp" \
  -n 256
```

3. 启动本地服务

```bash
./build/bin/llama-server \
  -m models/qwen2.5-7b-instruct-q4_k_m.gguf \
  --host 0.0.0.0 \
  --port 8080
```

## 四、关键概念

| 概念 | 说明 |
|------|------|
| GGUF | llama.cpp 常用模型文件格式 |
| Q4 / Q5 / Q8 | 不同量化等级，数字越小越省内存 |
| Metal | macOS GPU 加速后端 |
| CUDA | NVIDIA GPU 加速后端 |
| Context Size | 上下文长度，越大内存占用越高 |

## 五、适用场景

- CPU 或低显存设备运行大模型
- macOS 本地模型推理
- 边缘设备、离线设备部署
- 对依赖和服务体积敏感的应用
- 学习量化模型推理原理

## 六、与其他引擎对比

| 方案 | 定位 | 特点 |
|------|------|------|
| llama.cpp | 低资源本地推理 | CPU、GGUF、边缘部署友好 |
| Ollama | 本地模型封装 | 更易用，底层常依赖类似量化生态 |
| vLLM | 高吞吐服务化 | 更适合 GPU 高并发 |
| AirLLM | 极低显存超大模型 | 通过分层加载降低显存 |

## 七、注意事项

- 量化越激进，占用越低，但效果可能略有下降。
- CPU 推理可用但速度受内存带宽影响明显。
- 上下文越长，KV Cache 占用越高。
- 如果追求生产高并发服务，通常不是首选方案。
