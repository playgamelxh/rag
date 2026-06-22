## Freeze Fine-Tuning（冻结微调）

### 一、核心概念

冻结微调是指冻结模型的部分参数（通常是底层参数），仅训练剩余参数（通常是顶层参数）的微调方式。

原理：
```
预训练模型(W_0)
├── 底层参数（冻结，不更新）→ 保留通用语言知识
└── 顶层参数（训练，更新）→ 适应特定任务
```

在微调家族中的位置：
```
微调方法
├── 全量微调（更新100%参数）
├── 冻结微调（更新部分参数，如顶层）
└── 参数高效微调（PEFT，更新<1%参数）
    ├── LoRA
    ├── Adapter
    └── ...
```

---

### 二、冻结策略

#### 按层级冻结

| 冻结策略 | 冻结范围 | 更新范围 | 特点 |
|----------|----------|----------|------|
| 冻结底层 | 第1~N层Transformer | 顶层分类/生成层 | 保留通用知识，适配任务 |
| 冻结中间层 | 中间几层Transformer | 底层+顶层 | 适合领域适配 |
| 冻结除最后一层 | 所有层除最后一层 | 仅最后一层 | 参数最少，效果有限 |
| 逐步解冻 | 初始冻结所有层 | 逐步解冻训练 | 平衡效果与稳定性 |

#### 按模块冻结

| 冻结策略 | 冻结范围 | 更新范围 | 特点 |
|----------|----------|----------|------|
| 冻结编码器 | Transformer编码器 | 仅解码器 | 适合翻译任务 |
| 冻结注意力层 | 注意力模块 | FFN模块 | 保持注意力机制 |
| 冻结FFN层 | FFN模块 | 注意力模块 | 调整信息流动 |

---

### 三、特点与优缺点

#### 特点

| 维度 | 描述 |
|------|------|
| 参数更新 | 部分参数（通常10%~50%） |
| 显存需求 | 中（7B模型约需16GB+） |
| 数据需求 | 中等（数千至数万级） |
| 效果 | 介于全量微调与PEFT之间 |
| 训练时间 | 中等 |
| 模型文件大小 | 完整模型大小 |

#### 优点

| 优点 | 说明 |
|------|------|
| 保留预训练知识 | 冻结底层参数，保留通用能力 |
| 显存需求降低 | 比全量微调减少约30%~50% |
| 训练更快 | 更新参数少，训练时间缩短 |
| 不易过拟合 | 自由度降低，泛化能力更好 |

#### 缺点

| 缺点 | 说明 |
|------|------|
| 效果受限 | 更新参数少，可能无法充分适配任务 |
| 策略选择复杂 | 需要确定冻结哪些层 |
| 模型文件大 | 仍需存储完整模型 |
| 不适合多任务 | 每个任务需要单独存储模型 |

---

### 四、适用场景

| 场景 | 是否适用 | 理由 |
|------|----------|------|
| 数据量中等（数千至数万） | 是 | 平衡效果与数据需求 |
| 显存有限（16GB+） | 是 | 比全量微调节省显存 |
| 需要保留通用能力 | 是 | 冻结底层参数 |
| 领域适配 | 是 | 适合逐步解冻策略 |
| 中小团队 | 是 | 资源需求适中 |
| 数据量极少（<100） | 否 | 建议使用PEFT或提示工程 |
| 需要最大化性能 | 否 | 建议使用全量微调 |
| 多任务场景 | 否 | 建议使用PEFT |

---

### 五、实现步骤

#### 1. 环境准备

```bash
pip install torch transformers datasets accelerate
```

#### 2. 加载模型

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

#### 3. 冻结参数

##### 策略A：冻结底层Transformer层

```python
transformer_layers = model.model.layers

num_layers_to_freeze = 20
for i, layer in enumerate(transformer_layers):
    if i < num_layers_to_freeze:
        for param in layer.parameters():
            param.requires_grad = False
    else:
        for param in layer.parameters():
            param.requires_grad = True
```

##### 策略B：仅训练分类/生成头

```python
for param in model.model.parameters():
    param.requires_grad = False

for param in model.lm_head.parameters():
    param.requires_grad = True
```

##### 策略C：逐步解冻（推荐）

```python
def freeze_model(model, freeze_layers):
    for i, layer in enumerate(model.model.layers):
        if i < freeze_layers:
            for param in layer.parameters():
                param.requires_grad = False

freeze_model(model, len(model.model.layers))
```

#### 4. 查看可训练参数

```python
def print_trainable_parameters(model):
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"可训练参数: {trainable_params:,} ({trainable_params/total_params*100:.2f}%)")
    print(f"总参数: {total_params:,}")

print_trainable_parameters(model)
```

#### 5. 配置训练参数

```python
from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    output_dir="./freeze_finetune_results",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    gradient_accumulation_steps=4,
    learning_rate=3e-5,
    num_train_epochs=5,
    logging_steps=10,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    fp16=True,
    weight_decay=1e-4,
    warmup_steps=500
)
```

#### 6. 数据预处理

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

#### 7. 执行训练

```python
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["eval"]
)

trainer.train()
```

---

### 六、冻结层数选择指南

#### 按模型大小选择

| 模型大小 | 总层数 | 推荐冻结层数 | 可训练参数比例 |
|----------|--------|--------------|----------------|
| 7B | 32 | 20~24 | 20%~40% |
| 13B | 40 | 28~32 | 20%~30% |
| 70B | 80 | 60~64 | 20%~25% |

#### 按任务类型选择

| 任务类型 | 推荐冻结层数 | 理由 |
|----------|--------------|------|
| 文本分类 | 多冻结（2/3以上） | 任务简单，只需微调顶层 |
| 文本生成 | 适度冻结（1/2~2/3） | 需要更多参数适配生成风格 |
| 对话系统 | 适度冻结（1/2~2/3） | 需要理解和生成能力 |
| 领域适配 | 少冻结（1/3以下）或逐步解冻 | 需要学习领域知识 |

#### 按数据量选择

| 数据量 | 推荐冻结层数 | 理由 |
|--------|--------------|------|
| 少量（<1000） | 多冻结（2/3以上） | 防止过拟合 |
| 中等（1000~10000） | 适度冻结（1/2~2/3） | 平衡效果与泛化 |
| 大量（>10000） | 少冻结（1/3以下） | 充分利用数据 |

---

### 七、逐步解冻策略

#### 三阶段解冻

```
阶段1（Epoch 1-2）：冻结所有Transformer层，仅训练输出层
    └── 目的：让输出层适应任务格式

阶段2（Epoch 3-4）：解冻最后N层（如4层）
    └── 目的：让顶层Transformer学习任务特征

阶段3（Epoch 5-6）：解冻全部层，降低学习率继续训练
    └── 目的：微调所有参数，提升整体效果
```

#### 实现代码

```python
from transformers import TrainerCallback

class UnfreezeCallback(TrainerCallback):
    def __init__(self, model, unfreeze_epochs=[3, 5], unfreeze_layers=[4, None]):
        self.model = model
        self.unfreeze_epochs = unfreeze_epochs
        self.unfreeze_layers = unfreeze_layers
        self.current_epoch = 0
    
    def on_epoch_begin(self, args, state, control, **kwargs):
        self.current_epoch = state.epoch
        for epoch, layers in zip(self.unfreeze_epochs, self.unfreeze_layers):
            if self.current_epoch == epoch:
                self.unfreeze_layers_func(layers)
    
    def unfreeze_layers_func(self, num_layers):
        if num_layers is None:
            for param in self.model.parameters():
                param.requires_grad = True
        else:
            total_layers = len(self.model.model.layers)
            start_idx = total_layers - num_layers
            for i, layer in enumerate(self.model.model.layers):
                if i >= start_idx:
                    for param in layer.parameters():
                        param.requires_grad = True
```

---

### 八、评估与调优

#### 常用评估指标

| 任务类型 | 评估指标 |
|----------|----------|
| 文本分类 | Accuracy, F1, Precision, Recall |
| 文本生成 | BLEU, ROUGE, METEOR |
| 问答任务 | EM, F1 |
| 语言模型 | Perplexity |

#### 调优策略

| 问题 | 解决方案 |
|------|----------|
| 效果不佳 | 减少冻结层数、增加训练轮数 |
| 过拟合 | 增加冻结层数、使用weight_decay |
| 训练不稳定 | 降低学习率、增加warmup_steps |
| 显存不足 | 增加冻结层数、减小batch_size |

---

### 九、实践建议

#### 1. 冻结层数选择

- 从保守开始：先冻结2/3层，效果不佳再减少冻结层数
- 参考表：根据模型大小、任务类型、数据量选择
- 实验验证：尝试不同冻结层数，选择效果最好的

#### 2. 学习率调整

| 训练阶段 | 学习率 |
|----------|--------|
| 仅训练输出层 | 5e-5 ~ 1e-4 |
| 解冻部分层 | 3e-5 ~ 5e-5 |
| 解冻全部层 | 1e-5 ~ 3e-5 |

#### 3. 数据策略

- 数据量：至少需要数千级标注样本
- 数据质量：优先保证数据质量
- 数据多样性：覆盖多种场景

#### 4. 监控与日志

- 使用TensorBoard监控训练过程
- 记录可训练参数比例
- 观察train/eval loss曲线
- 定期验证模型效果

---

### 十、总结

冻结微调是平衡效果与资源的折中方案。

适用条件：
- 数据量中等（数千至数万）
- 显存有限（16GB+）
- 需要保留模型通用能力

不适用条件：
- 数据量极少（<1000）→ 建议使用PEFT
- 需要最大化性能 → 建议使用全量微调
- 多任务场景 → 建议使用PEFT

推荐策略：
- 逐步解冻策略：分阶段解冻，平衡效果与稳定性
- 从保守开始：先冻结更多层，再根据效果调整
- 结合正则化：使用weight_decay防止过拟合
