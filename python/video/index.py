from flask import Flask, render_template, request, jsonify, redirect, session
import uuid
import threading
from datetime import datetime
import os
import time
from local_lib.knowledage import search_knowledge
from local_lib.doubao import call_doubao_model
from local_lib.tts_http_demo import text_to_speech
from local_lib.qimeila import create_video
from local_lib.tos_store import upload_to_cloud

app = Flask(__name__)
VIDEO_FOLDER = os.path.join('static', 'videos')
app.config['VIDEO_FOLDER'] = VIDEO_FOLDER

# 存储对话历史和请求状态
conversation_history = []
processing_requests = {}


@app.route('/')
def index():
    # 获取视频列表
    videos = [f for f in os.listdir(app.config['VIDEO_FOLDER']) if os.path.isfile(os.path.join(app.config['VIDEO_FOLDER'], f))]
    return render_template('index.html', videos=videos)


@app.route('/generate-video', methods=['POST'])    
def generate_video():

    text = request.form['text']
    # 创建随机音频文件名称
    audio_filename = f"./static/audios/audio_{uuid.uuid4()}.mp3"
    # 调用文本转语音接口
    text_to_speech(text, audio_filename)
    print(audio_filename)
    
    # 将音频文件上传到tos中
    audio_filename_url = upload_to_cloud(audio_filename)
    
    # 启动异步视频生成
    video_filename = f"video_{uuid.uuid4()}.mp4"
    # 生成视频链接
    video_url = os.path.join(app.config['VIDEO_FOLDER'], video_filename)
    thread = threading.Thread(target=create_video, args=(text, video_url, audio_filename_url))
    thread.start()

    # 等待视频生成完成, 最多等待1分钟
    for _ in range(60):
        if os.path.exists(video_url):
            break
        time.sleep(1)
        print("等待视频生成完成")

    return redirect('/')

@app.route('/generate-text', methods=['POST'])
def generate_text():
    text = request.form['text']
    request_id = str(uuid.uuid4())
    
    # get knowledage
    res = search_knowledge(text)
    knowledges = res.get('data', {}).get('result_list', [])
    
    # 提取有用的文本信息（如caption）
    knowledge_texts = []
    for item in knowledges:
        attachments = item.get('chunk_attachment', [])
        for attachment in attachments:
            caption = attachment.get('caption', '').strip()
            if caption:
                knowledge_texts.append(caption)
    
    # 构建查询参数
    query = text
    if knowledge_texts:
        knowledge_str = '; '.join(knowledge_texts)
        query = f"{text}。参考知识库：{knowledge_str}"

    # 调用豆包大模型
    global conversation_history
    response = call_doubao_model(query, conversation_history)
    generated_text = response.message.content

    # 存储对话历史
    conversation_history.append({
        'role': 'user',
        'content': text
    })
    conversation_history.append({
        'role': 'assistant',
        'content': generated_text
    })
    # 限制对话历史长度
    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]
    
    return jsonify({'generated_text': generated_text, 'request_id': request_id})


@app.route('/api/get_video_files')
def get_video_files():
    video_dir = VIDEO_FOLDER
    # 确保目录存在
    if not os.path.exists(video_dir):
        return jsonify([])
    # 获取所有视频文件（排除目录）
    files = [f for f in os.listdir(video_dir) if os.path.isfile(os.path.join(video_dir, f))]
    # 按修改时间排序（最新的在前）
    files.sort(key=lambda x: os.path.getmtime(os.path.join(video_dir, x)), reverse=True)
    return jsonify(files)


if __name__ == '__main__':
    app.run(debug=True)