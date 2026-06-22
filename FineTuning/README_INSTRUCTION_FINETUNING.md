## Instruction Fine-Tuning（指令微调）

### 一、核心概念

指令微调是使用指令形式的数据对模型进行微调，使模型理解并遵循人类指令的过程。

原理：
```
预训练模型 + 指令数据（指令+输入+输出）→ 学会理解和执行指令 → 指令遵循模型
```

核心目标：
- 让模型理解自然语言指令
- 让模型生成符合指令要求的输出
- 对齐人类意图和偏好

在微调家族中的位置：
```
微调方法
├── 全量微调
├── 冻结微调
├── 参数高效微调（PEFT）
└── 指令微调（通常结合以上方法）
    ├── SFT（监督微调）
    └── RLHF（强化学习人类反馈）
```

---

### 二、指令微调 vs 传统微调

| 维度 | 传统微调 | 指令微调 |
|------|----------|----------|
| 数据格式 | 任务特定格式 | 指令+输入+输出 |
| 训练目标 | 适应特定任务 | 理解和执行指令 |
| 泛化能力 | 单一任务 | 多任务泛化 |
| 交互方式 | 固定输入格式 | 自然语言交互 |
| 典型应用 | 文本分类、命名实体识别 | 对话系统、AI助手 |

---

### 三、数据格式

#### 标准格式

```json
{
  "instruction": "请总结以下文章的主要内容",
  "input": "文章内容...",
  "output": "总结内容..."
}
```

#### 无输入格式

```json
{
  "instruction": "什么是机器学习？",
  "output": "机器学习是..."
}
```

#### 多轮对话格式

```json
{
  "conversations": [
    {"from": "human", "value": "你好"},
    {"from": "gpt", "value": "你好！我是AI助手。"},
    {"from": "human", "value": "什么是RAG？"},
    {"from": "gpt", "value": "RAG是检索增强生成..."}
  ]
}
```

#### ShareGPT格式

```json
{
  "id": "conv_001",
  "conversations": [
    {"role": "user", "content": "什么是LoRA？"},
    {"role": "assistant", "content": "LoRA是低秩适应..."}
  ]
}
```

---

### 四、指令模板

#### 基础模板

```
指令：{instruction}
输入：{input}
输出：{output}
```

#### Alpaca模板

```
### Instruction:
{instruction}

### Input:
{input}

### Response:
{output}
```

#### ChatML模板

```
<|im_start|>user
{instruction}
{input}
<|im_end|>
<|im_start|>assistant
{output}
<|im_end|>
```

#### 自定义模板

```
你是一个专业的AI助手，请根据以下指令完成任务。

指令：{instruction}

输入：{input}

回答：{output}
```

---

### 五、特点与优缺点

#### 特点

| 维度 | 描述 |
|------|------|
| 数据格式 | 指令+输入+输出 |
| 训练目标 | 理解和执行指令 |
| 泛化能力 | 强（多任务） |
| 交互方式 | 自然语言 |
| 效果 | 对齐人类意图 |

#### 优点

| 优点 | 说明 |
|------|------|
| 泛化能力强 | 一个模型可处理多种任务 |
| 交互友好 | 自然语言指令，无需学习特定格式 |
| 易于扩展 | 新增任务只需添加指令数据 |
| 对齐人类偏好 | 生成符合人类期望的输出 |

#### 缺点

| 缺点 | 说明 |
|------|------|
| 数据需求高 | 需要大量高质量指令数据 |
| 数据标注成本 | 指令数据标注比传统任务更复杂 |
| 训练难度大 | 需要更大的训练数据量和更长的训练时间 |

---

### 六、适用场景

| 场景 | 是否适用 | 理由 |
|------|----------|------|
| 对话系统 | 是 | 需要理解自然语言指令 |
| AI助手 | 是 | 需要多任务处理能力 |
| 通用能力对齐 | 是 | 需要对齐人类意图 |
| 垂直领域助手 | 是 | 需要领域知识+指令理解 |
| 单一任务（如文本分类） | 否 | 传统微调更高效 |
| 数据量极少（<100） | 否 | 建议使用提示工程 |

---

### 七、实现步骤

#### 1. 环境准备

```bash
pip install torch transformers datasets accelerate peft
```

#### 2. 数据准备

数据集要求：
- 高质量指令数据
- 多样化任务覆盖
- 格式统一规范

开源数据集：
- Alpaca
- ShareGPT
- Instruction Tuning with GPT-4
- FLAN

数据预处理：

```python
def format_instruction(examples):
    instructions = examples["instruction"]
    inputs = examples.get("input", "")
    outputs = examples["output"]
    
    formatted_texts = []
    for inst, inp, out in zip(instructions, inputs, outputs):
        if inp:
            text = f"### Instruction:\n{inst}\n\n### Input:\n{inp}\n\n### Response:\n{out}"
        else:
            text = f"### Instruction:\n{inst}\n\n### Response:\n{out}"
        formatted_texts.append(text)
    
    return {"text": formatted_texts}

dataset = dataset.map(format_instruction)
```

#### 3. 加载模型

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "meta-llama/Llama-2-7b-hf"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
```

#### 4. 选择微调方法

##### 方法A：全量微调

```python
for param in model.parameters():
    param.requires_grad = True
```

##### 方法B：LoRA微调（推荐）

```python
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
```

##### 方法C：冻结微调

```python
for i, layer in enumerate(model.model.layers):
    if i < 20:
        for param in layer.parameters():
            param.requires_grad = False
```

#### 5. 数据编码

```python
def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=512
    )

tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=dataset.column_names
)

tokenized_dataset.set_format("torch", columns=["input_ids", "attention_mask"])
```

#### 6. 配置训练参数

```python
from transformers import TrainingArguments, Trainer, DataCollatorForLanguageModeling

training_args = TrainingArguments(
    output_dir="./instruction_finetune_results",
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    num_train_epochs=3,
    logging_steps=10,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    fp16=True,
    weight_decay=0.01,
    warmup_steps=1000
)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)
```

#### 7. 执行训练

```python
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["eval"],
    data_collator=data_collator
)

trainer.train()
```

#### 8. 保存模型

```python
model.save_pretrained("./instruction_lora_model")

merged_model = model.merge_and_unload()
merged_model.save_pretrained("./instruction_full_model")
```

---

### 八、数据构建指南

#### 1. 数据来源

| 来源 | 说明 | 质量 |
|------|------|------|
| 人工标注 | 专业标注人员编写 | 高 |
| 自动化生成 | 使用GPT-4等模型生成 | 中-高 |
| 开源数据集 | Alpaca、ShareGPT等 | 中 |
| 用户日志 | 真实用户交互数据 | 中-高 |

#### 2. 数据质量要求

| 维度 | 要求 |
|------|------|
| 指令清晰 | 指令描述明确，无歧义 |
| 输出准确 | 输出符合指令要求，正确无误 |
| 格式统一 | 所有样本格式一致 |
| 多样性 | 覆盖多种任务类型和场景 |
| 无偏见 | 避免性别、种族等偏见 |

#### 3. 数据量建议

| 模型大小 | 推荐数据量 | 理由 |
|----------|------------|------|
| 7B | 10K~100K | 平衡效果与训练成本 |
| 13B | 10K~200K | 更大模型需要更多数据 |
| 70B | 100K~1M | 超大模型需要大量数据 |

#### 4. 任务覆盖

建议覆盖以下任务类型：

| 任务类别 | 示例任务 |
|----------|----------|
| 问答 | 事实问答、常识问答 |
| 摘要 | 文本摘要、文档摘要 |
| 翻译 | 多语言翻译 |
| 推理 | 数学推理、逻辑推理 |
| 创作 | 故事创作、诗歌创作 |
| 代码 | 代码生成、代码解释 |
| 分类 | 文本分类、情感分析 |
| 提取 | 关键词提取、实体识别 |

---

### 九、评估方法

#### 自动评估

| 评估指标 | 适用任务 | 说明 |
|----------|----------|------|
| BLEU | 翻译、摘要 | 衡量生成文本与参考的相似度 |
| ROUGE | 摘要 | 衡量召回率 |
| BERTScore | 通用 | 使用BERT计算语义相似度 |
| MMLU | 知识问答 | 衡量模型知识水平 |
| BBH | 推理 | 衡量推理能力 |
| MT-Bench | 对话 | 衡量对话质量 |

#### 人工评估

| 评估维度 | 评分标准 |
|----------|----------|
| 指令遵循 | 是否理解并执行指令 |
| 回答准确性 | 回答是否正确 |
| 语言流畅性 | 表达是否自然流畅 |
| 完整性 | 是否完整回答问题 |
| 安全性 | 是否包含有害内容 |

---

### 十、高级技巧

#### 1. 多阶段训练

```
阶段1：通用指令微调（100K样本，3个epoch）
    └── 目的：学习通用指令理解能力

阶段2：领域指令微调（10K领域样本，2个epoch）
    └── 目的：学习领域特定知识

阶段3：RLHF（可选）
    └── 目的：对齐人类偏好
```

#### 2. 指令多样性增强

```python
def augment_instruction(instruction):
    variations = [
        instruction,
        f"请{instruction}",
        f"你能{instruction}吗？",
        f"如何{instruction}？",
        f"帮我{instruction}"
    ]
    return variations
```

#### 3. 数据筛选

```python
def filter_high_quality_data(dataset):
    filtered = []
    for sample in dataset:
        if len(sample["instruction"]) < 5:
            continue
        if len(sample["output"]) < 10:
            continue
        if contains_toxic_content(sample["output"]):
            continue
        filtered.append(sample)
    return filtered
```

---

### 十一、实践建议

#### 1. 数据策略

- 数据质量优先：宁可少而精，不可多而滥
- 多样性覆盖：覆盖尽可能多的任务类型
- 领域适配：通用指令微调后进行领域微调
- 持续迭代：根据评估结果不断优化数据

#### 2. 训练策略

- 学习率：LoRA使用2e-4~3e-4，全量微调使用1e-5~5e-5
- 训练轮数：3~5轮通常足够
- Batch Size：根据显存调整，建议使用梯度累积
- 混合精度：使用fp16加速训练

#### 3. 评估策略

- 自动评估：作为快速反馈
- 人工评估：作为最终判断标准
- 对比测试：与基线模型对比
- 持续监控：定期评估模型效果

#### 4. 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 指令遵循差 | 数据量不足 | 增加指令数据量 |
| 输出质量低 | 数据质量差 | 筛选高质量数据 |
| 过拟合 | 数据量不足 | 增加数据、使用正则化 |
| 训练不稳定 | 学习率过高 | 降低学习率 |
| 领域知识不足 | 缺少领域数据 | 添加领域指令数据 |

---

### 十二、总结

指令微调是构建对话系统和AI助手的关键技术。

核心要点：
1. 数据格式：指令+输入+输出
2. 训练目标：理解和执行指令
3. 泛化能力：一个模型处理多种任务
4. 对齐人类偏好：生成符合期望的输出

推荐实践：
- 数据：高质量+多样化+领域适配
- 方法：LoRA微调（资源有限）或全量微调（资源充足）
- 评估：自动评估+人工评估结合
- 迭代：持续优化数据和模型

未来趋势：
- 更大规模的指令数据
- 更高效的指令微调方法
- 自动指令生成和筛选
- 多模态指令微调
