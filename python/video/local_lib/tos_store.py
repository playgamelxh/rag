import os
import tos
from tos import HttpMethodType

def upload_to_cloud(filename):
    # 上传文件到云存储
    # 上传到 tos
    ak = os.getenv("VOLC_ACCESSKEY")
    sk = os.getenv("VOLC_SECRETKEY")
    # your endpoint 和 your region 填写Bucket 所在区域对应的Endpoint。# 以华北2(北京)为例，your endpoint 填写 tos-cn-beijing.volces.com，your region 填写 cn-beijing。
    endpoint = "tos-cn-beijing.volces.com"
    region = "cn-beijing"
    bucket_name = "lvxh-first"
    # 根据 本地文件filename ，获取key 和 data
    object_key = filename.replace('./', '')
    data = open(filename, 'rb').read()
    try:
        client = tos.TosClientV2(ak, sk, endpoint, region)
        # 通过字符串方式添加 Object
        client.put_object(bucket_name, object_key, content=data)
    except tos.exceptions.TosClientError as e:
        # 操作失败，捕获客户端异常，一般情况为非法请求参数或网络异常
        print('fail with client error, message:{}, cause: {}'.format(e.message, e.cause))
    except tos.exceptions.TosServerError as e:
        # 操作失败，捕获服务端异常，可从返回信息中获取详细错误信息
        print('fail with server error, code: {}'.format(e.code))
        # request id 可定位具体问题，强烈建议日志中保存
        print('error with request id: {}'.format(e.request_id))
        print('error with message: {}'.format(e.message))
        print('error with http code: {}'.format(e.status_code))
        print('error with ec: {}'.format(e.ec))
        print('error with request url: {}'.format(e.request_url))
    except Exception as e:
        print('fail with unknown error: {}'.format(e))

    try:
        # 生成带签名的 url
        pre_signed_url_output = client.pre_signed_url(HttpMethodType.Http_Method_Get, bucket_name, object_key)
        return pre_signed_url_output.signed_url
    except Exception as e:
        print('fail with unknown error: {}'.format(e))

def get_link(filename):
    # 上传到 tos
    ak = os.getenv("VOLC_ACCESSKEY")
    sk = os.getenv("VOLC_SECRETKEY")
    # your endpoint 和 your region 填写Bucket 所在区域对应的Endpoint。# 以华北2(北京)为例，your endpoint 填写 tos-cn-beijing.volces.com，your region 填写 cn-beijing。
    endpoint = "tos-cn-beijing.volces.com"
    region = "cn-beijing"
    bucket_name = "lvxh-first"
    # 根据 本地文件filename ，获取key 和 data
    object_key = filename.replace('./', '')
    data = open(filename, 'rb').read()
    try:
        client = tos.TosClientV2(ak, sk, endpoint, region)
        # 生成带签名的 url
        pre_signed_url_output = client.pre_signed_url(HttpMethodType.Http_Method_Get, bucket_name, object_key)
        return pre_signed_url_output.signed_url
    except Exception as e:
        print('fail with unknown error: {}'.format(e))

if __name__ == '__main__':
    filename = './static/audios/audio_82dfd691-a413-4b27-8d57-73d6e0a521cb.mp3'
    link = upload_to_cloud(filename)
    print(link)
    # link = get_link(filename)
    # print(link)
