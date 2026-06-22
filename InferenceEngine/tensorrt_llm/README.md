## 简介

TensorRT-LLM 是 NVIDIA 面向大语言模型推理优化的高性能引擎，基于 TensorRT、CUDA 和 NVIDIA GPU 生态进行深度优化。它适合对性能、延迟和吞吐要求极高的企业级部署场景。

## 一、核心原理（一句话懂）

TensorRT-LLM 会把模型转换成经过 TensorRT 优化的推理引擎，通过算子融合、内核优化、并行策略和量化技术最大化 NVIDIA GPU 性能。

```
模型权重 → TensorRT-LLM 构建 Engine → NVIDIA GPU 高性能推理
```

## 二、核心优势

- 极致性能：充分利用 NVIDIA GPU、Tensor Core 和 CUDA 优化
- 低延迟高吞吐：适合严肃生产环境
- 支持多种并行：Tensor Parallel、Pipeline Parallel 等
- 支持量化：FP16、BF16、INT8、INT4 等优化路径
- 企业生态完善：适合与 Triton Inference Server 集成

## 三、基本流程

1. 准备模型权重

```bash
huggingface-cli download meta-llama/Llama-2-7b-hf --local-dir ./models/llama2-7b
```

2. 转换权重

```bash
python convert_checkpoint.py \
  --model_dir ./models/llama2-7b \
  --output_dir ./checkpoints/llama2-7b/trt
```

3. 构建 TensorRT Engine

```bash
trtllm-build \
  --checkpoint_dir ./checkpoints/llama2-7b/trt \
  --output_dir ./engines/llama2-7b
```

4. 启动推理服务

```bash
python3 run.py \
  --engine_dir ./engines/llama2-7b \
  --tokenizer_dir ./models/llama2-7b \
  --input_text "介绍一下 TensorRT-LLM"
```

## 四、关键技术

| 技术 | 说明 |
|------|------|
| Kernel Fusion | 融合多个算子，减少显存读写和调度开销 |
| Tensor Parallel | 将模型张量切分到多张 GPU |
| Pipeline Parallel | 将不同层分布到不同 GPU |
| In-flight Batching | 动态批处理，提高并发效率 |
| Quantization | 通过低精度降低显存并提升速度 |

## 五、适用场景

- NVIDIA GPU 生产部署
- 对延迟和吞吐要求极高的业务
- 大规模在线推理服务
- 与 Triton Inference Server 结合部署
- 企业级模型服务平台

## 六、与其他引擎对比

| 方案 | 定位 | 特点 |
|------|------|------|
| TensorRT-LLM | NVIDIA 极致优化 | 性能强，部署复杂 |
| vLLM | 通用高吞吐服务 | 易用性更好，生态更简单 |
| SGLang | 结构化服务推理 | 更适合复杂生成流程 |
| Transformers | 通用实验框架 | 易学习但性能不是最优 |

## 七、注意事项

- 主要面向 NVIDIA GPU，硬件依赖强。
- 构建和部署流程比 vLLM、Ollama 更复杂。
- 模型转换、Engine 构建和版本兼容需要重点关注。
- 更适合稳定模型的生产部署，不适合频繁切换模型的快速实验。
