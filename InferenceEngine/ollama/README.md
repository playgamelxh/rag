## 简介

Ollama 是一个面向本地大模型运行和管理的工具，特点是安装简单、模型管理方便、命令行体验友好。它适合个人电脑、本地开发、教学实验和轻量级应用集成。

## 一、核心原理（一句话懂）

Ollama 把模型下载、量化格式、运行时、服务接口封装成统一体验，用户可以像运行应用一样在本地启动和调用大模型。

```
ollama pull 模型 → ollama run 模型 → 本地 API / 命令行调用
```

## 二、核心优势

- 极简安装：适合快速体验本地 LLM
- 模型管理方便：支持 pull、run、list、rm 等命令
- 本地隐私：数据默认在本机处理
- API 友好：提供本地 HTTP 接口
- 多平台：支持 macOS、Linux、Windows

## 三、快速上手

1. 安装后拉取模型

```bash
ollama pull llama3.1
```

2. 运行模型

```bash
ollama run llama3.1
```

3. 调用本地 API

```bash
curl http://localhost:11434/api/generate \
  -d '{
    "model": "llama3.1",
    "prompt": "介绍一下 Ollama"
  }'
```

## 四、常用命令

| 命令 | 作用 |
|------|------|
| `ollama pull <model>` | 下载模型 |
| `ollama run <model>` | 运行模型 |
| `ollama list` | 查看本地模型 |
| `ollama rm <model>` | 删除模型 |
| `ollama serve` | 启动服务 |
| `ollama create` | 基于 Modelfile 创建自定义模型 |

## 五、适用场景

- 个人电脑本地运行大模型
- 快速测试不同开源模型效果
- 本地 RAG 应用开发
- 教学演示和原型验证
- 对数据隐私有要求的轻量应用

## 六、与其他引擎对比

| 方案 | 定位 | 特点 |
|------|------|------|
| Ollama | 本地模型管理和运行 | 简单易用，适合个人开发 |
| vLLM | 高吞吐服务化推理 | 更适合生产 API 服务 |
| llama.cpp | 底层低资源推理 | 更灵活，配置更细 |
| Transformers | 通用研究框架 | 适合学习模型内部流程 |

## 七、注意事项

- Ollama 更强调易用性，不一定是最高吞吐方案。
- 模型大小仍然受内存、显存和磁盘空间限制。
- 生产高并发服务通常更推荐 vLLM、SGLang 或 LMDeploy。
- 自定义模型可通过 Modelfile 管理系统提示词、参数和基础模型。
