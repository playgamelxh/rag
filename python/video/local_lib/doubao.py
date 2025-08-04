import os
from openai import OpenAI

# 封装豆包模型调用函数
def call_doubao_model(query, history=None):
    # 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
    # 初始化Ark客户端，从环境变量中读取您的API Key
    client = OpenAI(
        # 此为默认路径，您可根据业务所在地域进行配置
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
        api_key=os.environ.get("DOUBAO_API_KEY"),
#         api_key="",
    )

    # 初始化历史消息列表
    if history is None:
        history = []

    # 构建消息列表（历史消息 + 当前查询）
    messages = history + [{
        "role": "user",
        "content": query
    }]

    response = client.chat.completions.create(
        # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
        model="doubao-seed-1-6-250615",
        messages=messages,
        max_tokens=50,
    )
    return response.choices[0]
