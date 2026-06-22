## 简介

SGLang 是一个面向大语言模型和多模态模型的高性能推理与编程框架，既关注服务化推理性能，也关注复杂生成流程的表达能力。它适合 Agent、多轮对话、结构化输出、工具调用和复杂提示词编排场景。

## 一、核心原理（一句话懂）

SGLang 将“推理服务”和“生成程序”结合起来，通过高效运行时、RadixAttention、连续批处理和结构化生成接口，让复杂 LLM 应用更容易写、更高效运行。

```
复杂生成逻辑 → SGLang 编程接口 → 高性能 Runtime → 模型输出
```

## 二、核心优势

- 适合复杂生成流程：多轮对话、分支、约束输出、工具调用
- 高性能服务化：支持高吞吐推理运行时
- 支持结构化输出：适合 JSON、函数调用、Agent 场景
- 多模型支持：覆盖主流语言模型和部分多模态模型
- 应用表达能力强：比单纯推理服务更适合复杂业务逻辑

## 三、快速上手

1. 安装

```bash
pip install sglang
```

2. 启动服务

```bash
python -m sglang.launch_server \
  --model-path Qwen/Qwen2.5-7B-Instruct \
  --host 0.0.0.0 \
  --port 30000
```

3. Python 调用

```python
import sglang as sgl

@sgl.function
def qa(s, question):
    s += "请回答下面的问题：" + question
    s += sgl.gen("answer", max_tokens=256)

state = qa.run(question="介绍一下 SGLang")
print(state["answer"])
```

## 四、关键技术

| 技术 | 说明 |
|------|------|
| RadixAttention | 复用共享前缀的 KV Cache，提高多请求效率 |
| Continuous Batching | 动态批处理，提高 GPU 利用率 |
| Structured Generation | 支持结构化、约束化输出 |
| Runtime Server | 提供服务化推理能力 |
| Programmatic Prompting | 用程序方式组织复杂提示词流程 |

## 五、适用场景

- Agent 应用和工具调用
- 多轮对话系统
- 结构化 JSON 输出
- 复杂 Prompt 编排
- 高并发模型服务
- 多模态推理应用

## 六、与其他引擎对比

| 方案 | 定位 | 特点 |
|------|------|------|
| SGLang | 复杂生成与高性能推理 | 适合 Agent 和结构化流程 |
| vLLM | 高吞吐 API 服务 | 更偏通用推理服务 |
| Transformers | 实验和模型开发 | 灵活但服务性能弱 |
| TensorRT-LLM | NVIDIA 极致性能 | 更底层、更复杂 |

## 七、注意事项

- 如果只是本地简单运行模型，Ollama 更容易上手。
- 如果只需要通用 OpenAI API 服务，vLLM 可能更直接。
- SGLang 的优势在于复杂生成逻辑和服务性能结合。
- 生产部署仍需关注鉴权、限流、日志和监控。
