import os
import json
import requests
from volcengine.auth.SignerV4 import SignerV4
from volcengine.base.Request import Request
from volcengine.Credentials import Credentials

collection_name = "first"
project_name = "default"
query = ""
ak = os.getenv("VOLC_ACCESSKEY")
sk = os.getenv("VOLC_SECRETKEY")
g_knowledge_base_domain = "api-knowledgebase.mlp.cn-beijing.volces.com"
account_id = "57163232"


def prepare_request(method, path, params=None, data=None, doseq=0):
    if params:
        for key in params:
            if (
                    isinstance(params[key], int)
                    or isinstance(params[key], float)
                    or isinstance(params[key], bool)
            ):
                params[key] = str(params[key])
            elif isinstance(params[key], list):
                if not doseq:
                    params[key] = ",".join(params[key])
    r = Request()
    r.set_shema("http")
    r.set_method(method)
    r.set_connection_timeout(10)
    r.set_socket_timeout(10)
    mheaders = {
        "Accept": "application/json",
        "Content-Type": "application/json; charset=utf-8",
        "Host": g_knowledge_base_domain,
        "V-Account-Id": account_id,
    }
    r.set_headers(mheaders)
    if params:
        r.set_query(params)
    r.set_host(g_knowledge_base_domain)
    r.set_path(path)
    if data is not None:
        r.set_body(json.dumps(data))

    # 生成签名
    credentials = Credentials(ak, sk, "air", "cn-north-1")
    SignerV4.sign(r, credentials)
    return r


def search_knowledge(query):
    method = "POST"
    path = "/api/knowledge/collection/search_knowledge"
    request_params = {
    "project": "default",
    "name": "first",
    "query": query,
    "limit": 10,
    "pre_processing": {
        "need_instruction": True,
        "return_token_usage": True,
        "messages": [
            {
                "role": "system",
                "content": ""
            },
            {
                "role": "user"
            }
        ]
    },
    "dense_weight": 0.68,
    "post_processing": {
        "get_attachment_link": True,
        "rerank_only_chunk": False,
        "rerank_switch": True,
        "rerank_model": "base-multilingual-rerank",
        "retrieve_count": 25
    }
}

    info_req = prepare_request(method=method, path=path, data=request_params)
    rsp = requests.request(
        method=info_req.method,
        url="http://{}{}".format(g_knowledge_base_domain, info_req.path),
        headers=info_req.headers,
        data=info_req.body
    )

    return rsp.json()


if __name__ == "__main__":
    search_knowledge()
