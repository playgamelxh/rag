from airllm import AutoModel

# 加载模型（自动分层、自动适配）
model = AutoModel.from_pretrained("lmsys/vicuna-70b-v1.5")

# 生成文本
prompt = "写一段关于AI的介绍"
output = model.generate(prompt, max_length=200)
print(output)