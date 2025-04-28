# Lua 代码分析工具

这是一个用于分析 Lua 代码中 table 重复 key 的工具。

## 功能特点

- 递归扫描指定目录下的所有 Lua 文件
- 使用 AI 模型分析 Lua 代码中的 table 重复 key 问题
- 输出 JSONL 格式的重复 key 信息，每行一个 JSON 对象

## 环境要求

- Python 3.x
- OpenAI API 访问权限

## 配置说明

在使用前，需要在项目根目录创建 `.env` 文件，并配置以下环境变量：

```env
BASE_URL=你的 API base_url
API_KEY=你的 API 密钥
```

## 使用方法

1. 安装依赖：
```bash
uv venv llm_check
uv pip install -r requirements.txt
```

2. 配置 `.env` 文件

3. 运行程序：
```bash
python main.py <lua文件目录>
```

## 输出格式

程序会输出 JSONL 格式的分析结果，每行一个 JSON 对象，格式如下：

```json
{"table_name": "表名", "key": "重复的key", "lines": [行号1, 行号2, ...]}
```

示例输出：
```json
{"table_name": "example_table", "key": "duplicate_key", "lines": [10, 15]}
```

如果没有发现重复的 key，将不会输出任何 JSON 对象。

## 注意事项

- 确保 `.env` 文件中的 API 配置正确
- 程序需要网络连接以访问 OpenAI API
- 建议在分析大型代码库时注意 API 调用限制 