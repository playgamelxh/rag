# coding:utf-8
from __future__ import print_function
from ast import While
import re
from time import sleep

from volcengine import visual
from volcengine.visual.VisualService import VisualService

import json
import sys
import os
import base64
import datetime
import hashlib
import hmac
import requests

AK = os.getenv("VOLC_ACCESSKEY")
SK = os.getenv("VOLC_SECRETKEY")

def create_role_task(req_key:str, image_url:str):
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak(AK)
    visual_service.set_sk(SK)

    # 请求Body(查看接口文档请求参数-请求示例，将请求参数内容复制到此)
    form = {
        # "req_key": "realman_avatar_picture_create_role",# 普通模式
        # "image_url": "https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_cf48da49ad4749c72a532e39e8ec140d.jpg",
        "req_key": req_key,
        "image_url": image_url,
    }
    resp = visual_service.cv_submit_task( form)
    print(resp)
    return resp


def create_video_task(req_key:str,  audio_url:str, resource_id:str):
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak(AK)
    visual_service.set_sk(SK)

    # 请求Body(查看接口文档请求参数-请求示例，将请求参数内容复制到此)
    form = {
        "req_key": req_key,
        "audio_url": audio_url,
        "resource_id": resource_id,
    }
    resp = visual_service.cv_submit_task( form)
    print(resp)
    return resp


def check_task(req_key:str, task_id:str):
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak(AK)
    visual_service.set_sk(SK)

    # 请求Body(查看接口文档请求参数-请求示例，将请求参数内容复制到此)
    form = {
        "req_key": req_key,
        "task_id": task_id
    }
    resp = visual_service.cv_get_result(form)
    print(resp)
    return resp

def create_video(query:str, filename:str, audio_filename:str):
    # create role task
    req_key = "realman_avatar_picture_create_role"
    image_url = "https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_cf48da49ad4749c72a532e39e8ec140d.jpg"
    task_info = create_role_task(req_key, image_url)

    # check task
    resource_id = ""
    while True:
        task_result = check_task(req_key, task_info["data"]["task_id"])
        resp_data = json.loads(task_result["data"]["resp_data"])
        # 判断resp_data dict 是否包含  resource_id 字端
        if "resource_id" in resp_data:
            resource_id = resp_data["resource_id"]
            print(resource_id)
            break
        sleep(3)

    # create video task
    req_key = "realman_avatar_picture_v2"
    audio_url = audio_filename
    task_info = create_video_task(req_key, audio_url, resource_id)

    # check task
    preview_url = ""
    while True:
        task_result = check_task(req_key, task_info["data"]["task_id"])
        # {'code': 10000, 'data': {'binary_data_base64': [], 'image_urls': None, 'resp_data': '{"progress": 100, "received_at": 1754292527, "processed_at": 1754292527, "finished_at": 1754292606, "binary_data_url_list": [], "binary_data_info_list": [], "code": 0, "msg": "success", "video": {"Vid": "v034e3g10004d2862v7og65lqgmr3kn0", "VideoMeta": {"Uri": "tos-cn-v-70bec6/oICGBiQ2E10AxnnXEAQA0hiACSu4YgPD1vIwCf", "Height": 2048, "Width": 1152, "OriginHeight": 2048, "OriginWidth": 1152, "Duration": 16.555, "Bitrate": 1866392, "Md5": "2a7fc1e70ac89036b5614248c0d439aa", "Format": "MP4", "Size": 3862267, "FileType": "video", "Codec": "h264"}, "GetPosterMode": "sync"}, "alpha": null, "url": null, "algorithm_status_code": 0, "preview_url": ["https://v26-default.365yg.com/105a32a20120b9f2f451dc0bb718b211/68906f9d/video/tos/cn/tos-cn-v-70bec6/oICGBiQ2E10AxnnXEAQA0hiACSu4YgPD1vIwCf/?a=5667&ch=0&cr=0&dr=0&er=0&lr=unwatermarked&cd=0%7C0%7C0%7C0&br=1822&bt=1822&cs=0&ft=Oi.pi77JWH6BMIfVC_r0PD1IN&mime_type=video_mp4&qs=13&rc=M251am85cnk5NTczNDY3M0BpM251am85cnk5NTczNDY3M0BrMGpuMmQ0LzVhLS1kYjBzYSNrMGpuMmQ0LzVhLS1kYjBzcw%3D%3D&btag=c0000e00010000&dy_q=1754292605&l=02175429260566700000000000000000000ffff0a9fd718d25305"]}', 'status': 'done'}, 'message': 'Success', 'request_id': '202508041532067F19A9512D81856858B2', 'status': 10000, 'time_elapsed': '10.63823ms'}
        resp_data = json.loads(task_result["data"]["resp_data"])
        # 判断resp_data dict 是否包含  resource_id 字端
        if "preview_url" in resp_data:
            preview_url = resp_data["preview_url"][0]
            print(preview_url)
            # return preview_url
            break
        sleep(3)



    # download file
    response = requests.get(preview_url)
    with open(filename, 'wb') as f:
        f.write(response.content)

    return preview_url


if __name__ == "__main__":

    # create role task
    req_key = "realman_avatar_picture_create_role"
    image_url = "https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_cf48da49ad4749c72a532e39e8ec140d.jpg"
    task_info = create_role_task(req_key, image_url)
    # {'code': 10000, 'data': {'task_id': '10776474864155912247'}, 'message': 'Success', 'request_id': '2025080410104688C375C2121F3D4322B6', 'status': 10000, 'time_elapsed': '537.758857ms'}

    # # check task
    resource_id = "745cc915-ab49-4c2c-950b-9359623c185c"
    # {'code': 10000, 'data': {'binary_data_base64': [], 'image_urls': None, 'resp_data': '{"progress": 100, "received_at": 1754273919, "processed_at": 1754273919, "finished_at": 1754273926, "gpu_type": "unknown", "binary_data_url_list": [], "binary_data_info_list": [], "code": 0, "msg": "success", "resource_id": "fa91b383-b636-4207-b8bb-3808e8a12468", "status": 0, "message": "", "refuse_code": [], "face_position": [327, 490, 781, 963], "body_position": null, "role_type": "realman", "face_position_norm": null}', 'status': 'done'}, 'message': 'Success', 'request_id': '20250804101901364856A2673CA04497FA', 'status': 10000, 'time_elapsed': '10.614087ms'}
    while True:
        task_result = check_task(req_key, task_info["data"]["task_id"])
        resp_data = json.loads(task_result["data"]["resp_data"])
        # 判断resp_data dict 是否包含  resource_id 字端
        if "resource_id" in resp_data:
            resource_id = resp_data["resource_id"]
            print(resource_id)
            break
        sleep(3)

    # create video task
    req_key = "realman_avatar_picture_v2"
    audio_url = ""
    task_info = create_video_task(req_key, audio_url, resource_id)

    # check task
    while True:
        task_result = check_task(req_key, task_info["data"]["task_id"])
        resp_data = json.loads(task_result["data"]["resp_data"])
        # 判断resp_data dict 是否包含  resource_id 字端
        if "preview_url" in resp_data:
            preview_url = resp_data["preview_url"]
            print(preview_url)
            break
        sleep(3)
