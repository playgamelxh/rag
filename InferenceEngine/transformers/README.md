## 简介

Transformers 是 Hugging Face 提供的通用深度学习模型库，支持大量 NLP、多模态和大语言模型。它不是专门的高性能推理服务器，但非常适合学习 LLM 推理流程、模型实验、原型开发和研究验证。

## 一、核心原理（一句话懂）

Transformers 提供统一的模型、Tokenizer 和生成接口，让用户可以用少量 Python 代码加载模型并执行文本生成。

```
Tokenizer 编码 → AutoModel 加载权重 → generate 生成 token → Tokenizer 解码
```

## 二、核心优势

- 模型生态丰富：Hugging Face 上大量模型可直接加载
- 学习友好：便于理解 Tokenizer、模型结构和生成参数
- API 统一：AutoTokenizer、AutoModelForCausalLM 等接口通用
- 研究灵活：方便修改模型、调试输出、验证算法
- 与训练生态打通：可结合 Datasets、PEFT、Accelerate 等工具

## 三、快速上手

1. 安装

```bash
pip install transformers torch accelerate
```

2. 文本生成

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen2.5-0.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

messages = [
    {"role": "user", "content": "介绍一下 Transformers 推理"}
]

text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer([text], return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=256, temperature=0.7)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## 四、常用生成参数

| 参数 | 作用 | 说明 |
|------|------|------|
| `max_new_tokens` | 最大生成 token 数 | 控制输出长度 |
| `temperature` | 随机性 | 越高越发散 |
| `top_p` | nucleus sampling | 控制候选 token 范围 |
| `do_sample` | 是否采样 | False 时更偏确定性输出 |
| `repetition_penalty` | 重复惩罚 | 减少重复生成 |
| `eos_token_id` | 结束 token | 控制生成停止 |

## 五、适用场景

- 学习 LLM 推理流程
- 快速验证 Hugging Face 模型
- 研究生成参数对输出的影响
- 自定义模型结构或推理逻辑
- 小规模原型应用

## 六、与其他引擎对比

| 方案 | 定位 | 特点 |
|------|------|------|
| Transformers | 通用模型库 | 灵活易学，性能不是最优 |
| vLLM | 高吞吐推理服务 | 适合生产 API 部署 |
| Ollama | 本地模型运行 | 使用简单，适合个人电脑 |
| llama.cpp | 低资源推理 | 适合 CPU、GGUF、边缘设备 |

## 七、注意事项

- 默认 `generate()` 不适合高并发生产服务。
- 大模型加载需要关注显存、精度和 device_map 配置。
- 如果需要服务化和并发调度，建议使用 vLLM、SGLang 或 LMDeploy。
- Transformers 更适合作为理解和实验 LLM 的基础入口。
