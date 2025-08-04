#coding=utf-8

'''
requires Python 3.6 or later
pip install requests
'''
import base64
import json
import uuid
import requests

# 配置参数可外部传入或修改
DEFAULT_CONFIG = {
    'appid': '1659582763',
    'access_token': '0yHp4VHGHTZ-e_DOwj4GMnbCy3y6kOWy',
    'cluster': 'volcano_tts',
    'voice_type': 'BV705_streaming',
    'host': 'openspeech.bytedance.com',
    'encoding': 'mp3',
    'speed_ratio': 1.0,
    'volume_ratio': 1.0,
    'pitch_ratio': 1.0
}

def text_to_speech(text, output_file, config=None, uid='388808087185088'):
    """
    文本转语音合成方法
    :param text: 待合成文本
    :param output_file: 音频输出文件路径
    :param config: 合成配置字典，可选，默认使用DEFAULT_CONFIG
    :param uid: 用户唯一标识
    :return: 成功返回True，失败返回False
    """
    # 合并配置（用户传入配置覆盖默认配置）
    cfg = {**DEFAULT_CONFIG,** (config or {})}
    api_url = f"https://{cfg['host']}/api/v1/tts"
    headers = {'Authorization': f'Bearer;{cfg['access_token']}'}

    try:
        # 构建请求参数
        request_json = {
            'app': {
                'appid': cfg['appid'],
                'token': cfg['access_token'],
                'cluster': cfg['cluster']
            },
            'user': {'uid': uid},
            'audio': {
                'voice_type': cfg['voice_type'],
                'encoding': cfg['encoding'],
                'speed_ratio': cfg['speed_ratio'],
                'volume_ratio': cfg['volume_ratio'],
                'pitch_ratio': cfg['pitch_ratio'],
            },
            'request': {
                'reqid': str(uuid.uuid4()),
                'text': text,
                'text_type': 'plain',
                'operation': 'query',
                'with_frontend': 1,
                'frontend_type': 'unitTson'
            }
        }

        # 发送请求
        response = requests.post(
            api_url,
            data=json.dumps(request_json),
            headers=headers
        )
        response.raise_for_status()  # 检查HTTP错误状态
        resp_data = response.json()

        # 处理响应
        if 'data' in resp_data:
            with open(output_file, 'wb') as f:
                f.write(base64.b64decode(resp_data['data']))
            print(f'音频已保存至: {output_file}')
            return True
        else:
            print(f'合成失败: {resp_data.get('message', '未知错误')}')
            return False

    except requests.exceptions.RequestException as e:
        print(f'网络请求异常: {str(e)}')
    except Exception as e:
        print(f'处理异常: {str(e)}')
    return False

# 示例调用
if __name__ == '__main__':
    # 默认配置调用
    text_to_speech(
        text='你好，我是字节跳动语音合成',
        output_file='test_submit.mp3'
    )
