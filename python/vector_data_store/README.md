## Docs
https://milvus.io/docs/zh/schema.md

## SDK
```azure

 
```



## Windows 
```azure
# Install
# https://milvus.io/docs/zh/install_standalone-windows.md
wget https://raw.githubusercontent.com/milvus-io/milvus/refs/heads/master/scripts/standalone_embed.bat -OutFile standalone.bat
standalone.bat start
standalone.bat stop

# python 
#  创建虚拟环境
python -m venv venv
# 在命令提示符（CMD）中激活：
venv\Scripts\activate.bat
# 在 PowerShell 中激活：
venv\Scripts\Activate.ps1
# install package
python -m pip install pymilvus==2.6.0b0
# check
python -c "from pymilvus import Collection"

```

## zilliz/attu
```azure
https://github.com/zilliztech/attu
docker network create milvus-net
docker run -d --name milvus_standalone --network milvus-net -p 19530:19530 -p 9091:9091 milvusdb/milvus:latest 
docker run -d --name zilliz_attu --network milvus-net -p 3000:3000 -e MILVUS_URL=milvus_standalone:19530 zilliz/attu:latest
# http://localhost:3000/#/connect
# 链接方式milvus-standalone:19530
```
