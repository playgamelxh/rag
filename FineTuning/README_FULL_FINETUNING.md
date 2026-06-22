## Full Fine-Tuning（全量微调）

### 一、核心概念

全量微调是更新模型所有参数的微调方式，是最传统的微调方法。

原理：
```
预训练模型(W_0) + 任务数据 → 更新所有参数 → 适配任务的模型(W_final)
```

在微调家族中的位置：
```
微调方法
├── 全量微调（更新100%参数）
└── 参数高效微调（PEFT，更新<1%参数）
    ├── LoRA
    ├── Adapter
    ├── Prefix Tuning
    └── Prompt Tuning
```

---

### 二、特点与优缺点

#### 特点

| 维度 | 描述 |
|------|------|
| 参数更新 | 100% 所有参数 |
| 显存需求 | 高（7B模型约需24GB+，13B模型约需48GB+） |
| 数据需求 | 大量标注数据（数万级） |
| 效果 | 理论上最优 |
| 训练时间 | 长（数天至数周） |
| 模型文件大小 | 完整模型大小 |

#### 优点

| 优点 | 说明 |
|------|------|
| 效果最优 | 更新所有参数，能够最大程度适配任务 |
| 无需特殊技术 | 实现简单，无需PEFT库 |
| 模型独立 | 微调后的模型可独立使用，无需原模型 |

#### 缺点

| 缺点 | 说明 |
|------|------|
| 显存需求高 | 需要高端GPU集群 |
| 数据需求大 | 需要大量标注数据，否则容易过拟合 |
| 训练时间长 | 计算成本高 |
| 模型文件大 | 每个任务都需要存储完整模型 |
| 容易遗忘 | 可能破坏预训练知识 |

---

### 三、适用场景

| 场景 | 是否适用 | 理由 |
|------|----------|------|
| 数据充足（数万级标注样本） | 是 | 全量微调需要大量数据避免过拟合 |
| 计算资源充裕（多GPU集群） | 是 | 需要高端硬件支持 |
| 需要最大化模型性能 | 是 | 全量微调效果理论最优 |
| 中小团队/个人开发者 | 否 | 资源受限 |
| 消费级GPU（单卡24GB） | 否 | 仅能训练较小模型（如7B） |
| 多任务场景 | 否 | 每个任务需要单独存储完整模型 |

---

### 四、实现步骤

#### 1. 环境准备

核心依赖：
```bash
pip install torch transformers datasets accelerate
```

可选依赖：
```bash
pip install deepspeed
pip install tensorboard
pip install evaluate
```

#### 2. 数据准备

数据格式要求：
- 高质量标注数据
- 多样化任务覆盖
- 格式统一规范

示例数据格式：

##### 文本分类
```json
{"text": "这篇文章很棒", "label": "positive"}
```

##### 文本生成
```json
{"input": "问题：什么是机器学习？", "output": "机器学习是..."}
```

##### 对话数据
```json
{
  "conversations": [
    {"from": "human", "value": "你好"},
    {"from": "gpt", "value": "你好！我是AI助手。"}
  ]
}
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

#### 4. 配置训练参数

```python
from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    output_dir="./full_finetune_results",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    gradient_accumulation_steps=4,
    learning_rate=2e-5,
    num_train_epochs=5,
    logging_steps=10,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    fp16=True,
    bf16=False,
    weight_decay=1e-4,
    warmup_steps=1000,
    lr_scheduler_type="cosine",
    report_to="tensorboard"
)
```

关键参数说明：

| 参数 | 作用 | 推荐值 |
|------|------|--------|
| learning_rate | 学习率 | 1e-5 ~ 5e-5 |
| per_device_train_batch_size | 每设备batch大小 | 8 ~ 32（根据显存） |
| gradient_accumulation_steps | 梯度累积步数 | 4 ~ 16 |
| num_train_epochs | 训练轮数 | 3 ~ 10 |
| weight_decay | 权重衰减（正则化） | 1e-4 |
| warmup_steps | 预热步数 | 1000 ~ 5000 |
| fp16 | 混合精度训练 | True |

#### 5. 数据预处理

```python
def preprocess_function(examples):
    inputs = examples["input"]
    targets = examples["output"]
    
    model_inputs = tokenizer(inputs, padding="max_length", truncation=True, max_length=512)
    labels = tokenizer(targets, padding="max_length", truncation=True, max_length=512)
    
    labels["input_ids"] = [
        [(l if l != tokenizer.pad_token_id else -100) for l in label]
        for label in labels["input_ids"]
    ]
    
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_dataset = dataset.map(
    preprocess_function,
    batched=True,
    remove_columns=dataset.column_names
)
```

#### 6. 执行训练

```python
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["eval"]
)

trainer.train()
```

#### 7. 保存与加载模型

```python
model.save_pretrained("./full_finetune_model")
tokenizer.save_pretrained("./full_finetune_model")

from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("./full_finetune_model")
tokenizer = AutoTokenizer.from_pretrained("./full_finetune_model")
```

---

### 五、分布式训练配置

#### 使用 DeepSpeed（推荐）

配置文件 deepspeed_config.json：
```json
{
  "train_batch_size": 32,
  "train_micro_batch_size_per_gpu": 8,
  "gradient_accumulation_steps": 4,
  "optimizer": {
    "type": "AdamW",
    "params": {
      "lr": 2e-5,
      "weight_decay": 1e-4
    }
  },
  "scheduler": {
    "type": "WarmupCosine",
    "params": {
      "warmup_min_lr": 0,
      "warmup_max_lr": 2e-5,
      "warmup_num_steps": 1000,
      "total_num_steps": 100000
    }
  },
  "zero_optimization": {
    "stage": 2,
    "offload_optimizer": {
      "device": "cpu",
      "pin_memory": true
    },
    "allgather_partitions": true,
    "allgather_bucket_size": 2e8,
    "overlap_comm": true,
    "reduce_scatter": true,
    "reduce_bucket_size": 2e8,
    "contiguous_gradients": true
  },
  "fp16": {
    "enabled": true
  }
}
```

启动命令：
```bash
deepspeed --num_gpus=4 train.py --deepspeed_config deepspeed_config.json
```

---

### 六、评估与调优

#### 常用评估指标

| 任务类型 | 评估指标 | 说明 |
|----------|----------|------|
| 文本分类 | Accuracy, F1, Precision, Recall | 分类任务标准指标 |
| 文本生成 | BLEU, ROUGE, METEOR | 生成任务标准指标 |
| 问答任务 | EM, F1 | 问答任务标准指标 |
| 语言模型 | Perplexity | 困惑度，越低越好 |

#### 评估代码示例

```python
import evaluate

metric = evaluate.load("accuracy")

predictions = trainer.predict(eval_dataset)
results = metric.compute(
    predictions=predictions.predictions.argmax(-1),
    references=predictions.label_ids
)
print(f"Accuracy: {results['accuracy']}")
```

#### 调优策略

| 问题 | 解决方案 |
|------|----------|
| 训练loss不下降 | 降低学习率、检查数据格式、增加epoch |
| 过拟合 | 增加数据、增加weight_decay、使用Dropout |
| 显存不足 | 减小batch_size、使用梯度累积、使用DeepSpeed ZeRO |
| 训练不稳定 | 降低学习率、增加warmup_steps |

---

### 七、实践建议

#### 1. 硬件配置建议

| 模型大小 | 推荐显存 | 推荐GPU数量 |
|----------|----------|-------------|
| 7B | 24GB+ | 1 |
| 13B | 48GB+ | 2 |
| 70B | 200GB+ | 8+ |

#### 2. 数据策略

- 数据量：至少需要数万级标注样本
- 数据质量：优先保证数据质量而非数量
- 数据多样性：覆盖多种场景和任务类型
- 数据清洗：去除噪声、重复和低质量数据

#### 3. 训练策略

- 学习率：从1e-5开始，效果不佳可尝试增大至5e-5
- 训练轮数：3~5轮通常足够，过多容易过拟合
- 混合精度：使用fp16加速训练
- 正则化：适当使用weight_decay防止过拟合

#### 4. 监控与日志

- 使用TensorBoard监控训练过程
- 记录train/eval loss、评估指标
- 设置checkpoint保存策略
- 定期验证模型效果

---

### 八、总结

全量微调是效果最优但资源需求最大的微调方式。

适用条件：
- 充足的标注数据（数万级）
- 充裕的计算资源（高端GPU集群）
- 需要最大化模型性能

不适用条件：
- 资源受限的中小团队或个人开发者
- 数据量有限的场景
- 多任务场景（每个任务需要存储完整模型）

替代方案：
- 资源有限时选择LoRA等PEFT方法
- 数据有限时考虑少样本学习或提示工程
- 多任务场景使用Adapter或LoRA等参数高效方法
