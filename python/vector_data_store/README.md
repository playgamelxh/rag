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
