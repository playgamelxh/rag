# LoRA 微调
LoRA（Low-Rank Adaptation，低秩适应）是一种高效的大模型微调技术，通过冻结预训练模型的大部分参数，仅训练少量新增的低秩矩阵参数，在大幅降低显存消耗的同时保持良好的微调效果。以下是其核心原理、实现步骤和关键要点：
## 一、LoRA 的核心原理
1. 低秩分解思想
   模型微调本质是对预训练权重进行微小更新（ΔW ）。LoRA 假设这些更新矩阵具有低秩性，可分解为两个低秩矩阵的乘积：
   $\Delta W = W_A \cdot W_B$ 其中 $W_A \in \mathbb{R}^{d \times r}, \quad W_B \in \mathbb{R}^{r \times d}$（ r 是秩，远小于模型维度 d 通常取 8~32）。
2. 训练与推理机制
    * 训练时：冻结原模型权重$W_0$，仅优化$(W_A)$和$(W_B)$，计算量和显存需求降低至全量微调的 1%~10%。
    * 推理时：将$(\Delta W)$与原权重合并$(W_0 + W_A \cdot W_B)$，不增加推理延迟，与原生模型使用方式一致。
## 二、LoRA 的优势
1. 显存高效：7B 模型微调仅需 10GB + 显存（全量微调需 24GB+），适合中小团队。
2. 保留预训练知识：冻结原模型参数，避免破坏通用能力。
3. 多任务灵活切换：不同任务的 LoRA 权重可单独保存，切换任务时只需加载对应低秩矩阵。
4. 推理无额外开销：合并权重后与原模型结构一致，不影响部署效率。
## 三、LoRA 微调步骤（以 LLaMA 为例）
1. 环境准备
    * 核心库：
        + transformers：加载预训练模型和 tokenizer
        + peft（Hugging Face）：实现 LoRA 微调
        + accelerate/deepspeed：支持分布式训练。
        + bitsandbytes（可选）：4/8 位量化加载模型，进一步降低显存占用。
    * 安装命令
        ```
        pip install transformers datasets peft accelerate bitsandbytes
      ```
2. 数据准备
   与常规微调一致，需按任务格式化数据，例如： 
   * 对话任务：
   ```
   [
    {"conversations": [
        {"from": "human", "value": "什么是LoRA？"},
        {"from": "gpt", "value": "LoRA是一种参数高效微调技术..."}
    ]}]
   ```
   
   * 文本分类
    ```
   [{"text": "这篇文章很棒", "label": "positive"}, ...]
   ```
3. 配置 LoRA 参数

    使用peft.LoraConfig定义关键参数
```azure
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=8,  # 秩，控制低秩矩阵维度，通常8~32
    lora_alpha=32,  # 缩放因子，alpha/r 影响更新幅度
    target_modules=["q_proj", "v_proj"],  # 目标模块（需根据模型结构调整）
    lora_dropout=0.05,
    bias="none",  # 不训练偏置参数
    task_type="CAUSAL_LM"  # 因果语言模型（生成任务）
)
```
目标模块选择：
需针对模型结构指定待适配的模块，例如：
* LLaMA 系列：q_proj、v_proj（注意力的查询和值投影层）。
* BERT 系列：query、value（注意力层）。
* 通常选择注意力模块，对模型输出影响最大。
4. 加载模型并应用 LoRA
```azure
from transformers import AutoModelForCausalLM, AutoTokenizer

# 加载模型（可选4位量化）
model = AutoModelForCausalLM.from_pretrained(
    "decapoda-research/llama-7b-hf",
    load_in_4bit=True,  # 4位量化，节省显存
    device_map="auto",
    torch_dtype=torch.float16
)
tokenizer = AutoTokenizer.from_pretrained("decapoda-research/llama-7b-hf")

# 应用LoRA适配器
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()  # 查看可训练参数比例（通常<1%）
```
5. 训练模型
   
    使用transformers.Trainer或自定义训练循环：
 ```
from transformers import TrainingArguments, Trainer, DataCollatorForLanguageModeling

training_args = TrainingArguments(
    output_dir="./lora_results",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,  # 累积梯度模拟大batch
    learning_rate=2e-4,  # LoRA学习率可高于全量微调（通常1e-4~3e-4）
    num_train_epochs=3,
    logging_steps=10,
    save_strategy="epoch",
    fp16=True  # 混合精度训练，加速且省显存
)

# 数据整理器（生成任务用）
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    data_collator=data_collator
)

trainer.train()
```   
关键超参数:
* 学习率：LoRA 更新幅度小，学习率可设为全量微调的 5~10 倍（如 2e-4）。
* 秩（r）：增大 r 可提升表达能力，但会增加参数和计算量，需平衡（默认 8~16）。
6. 保存与加载 LoRA 权重
```azure
# 保存LoRA权重（仅几MB，远小于全量模型）
model.save_pretrained("lora_weights")

# 加载LoRA权重
from peft import PeftModel
base_model = AutoModelForCausalLM.from_pretrained("decapoda-research/llama-7b-hf")
lora_model = PeftModel.from_pretrained(base_model, "lora_weights")

# 推理时合并权重（可选，优化速度）
merged_model = lora_model.merge_and_unload()
```
## 四、LoRA 的适用场景与局限
* 适用场景：
  + 资源有限但需微调大模型（如 7B/13B 参数模型）。
  + 多任务场景（可快速切换不同 LoRA 权重）。
  + 生成类任务（如对话、摘要），效果接近全量微调。
* 局限：
    + 部分任务（如需要大幅调整模型行为的场景）效果可能略差于全量微调。
    + 目标模块选择依赖经验，选不好可能影响效果。
## 五、实践建议
1. 模块选择：优先微调注意力层（如 Q、V 投影），对语言模型效果最显著。
2. 秩的设置：从小秩（如 8）开始尝试，效果不足再增大（如 16/32）。
3. 数据质量：LoRA 对数据质量更敏感，需严格清洗（避免噪声样本）。
4. 量化训练：结合 4/8 位量化（bitsandbytes），在消费级 GPU（如 RTX 3090/4090）上即可微调 7B 模型。

## 总结
LoRA 凭借高效性已成为大模型微调的主流技术，尤其适合中小团队落地。实际应用中，可结合具体任务调整参数，或尝试其变体（如 LoRA+Adapter 混合策略）进一步优化效果。
