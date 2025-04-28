import os
import sys
import re
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

def load_env():
    load_dotenv()
    base_url = os.getenv('BASE_URL')
    api_key = os.getenv('API_KEY')
    
    if not base_url or not api_key:
        print("错误：请在.env文件中设置BASE_URL和API_KEY")
        sys.exit(1)
    
    return base_url, api_key
base_url, api_key = load_env()
client = OpenAI(api_key=api_key, base_url=base_url)

def find_duplicate_keys(name, content):
    # 给内容添加行号
    lines = content.split('\n')
    numbered_content = '\n'.join(f"{i+1}: {line}" for i, line in enumerate(lines))
    
    response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                            {"role": "system", "content": "你是一个专业的Lua代码分析助手。你的任务是找出Lua文件中table里重复定义的key。请严格按照以下JSONL格式输出结果，每行一个JSON对象：\n\n{\"filename\": \"文件名\", \"table_name\": \"表名\", \"key\": \"重复的key\", \"lines\": [行号1, 行号2, ...]}\n\n如果文件中没有重复的key，请输出空行。\n不要输出任何其他无关信息。key只要字面值\n\n注意：输入的文件内容已经带有行号，格式为'行号: 内容'，请使用这些行号来标识重复key的位置。"},
                            {"role": "user", "content": f"请分析以下Lua文件中的table重复key问题。文件名: {name}"},
                            {"role": "user", "content": numbered_content},
                        ],
                stream=False
                )
    print(f"开始分析文件: {name}")
    result = response.choices[0].message.content.strip()
    
    # 创建对应的jsonl文件
    jsonl_filename = str(name) + '.jsonl'
    with open(jsonl_filename, 'w', encoding='utf-8') as jsonl_file:
        if result:
            for line in result.split('\n'):
                if line.strip():
                    try:
                        json_obj = json.loads(line)
                        jsonl_file.write(line + '\n')  # 写入jsonl文件
                        print(json.dumps(json_obj, ensure_ascii=False))
                    except json.JSONDecodeError:
                        print(f"警告：无法解析JSON行: {line}")
        else:
            jsonl_file.write('\n')  # 如果没有结果，写入空行

def analyze_lua_files(directory):
    directory_path = Path(directory)
    
    if not directory_path.exists():
        print(f"错误：目录 {directory} 不存在")
        return
    
    for file_path in directory_path.rglob('*.lua'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                duplicates = find_duplicate_keys(file_path, content)
                
                if duplicates:
                    print(f"\n在文件 {file_path} 中发现重复的key：")
                    for key, line in duplicates:
                        print(f"  Key: {key}, 行号: {line}")
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python main.py <lua文件目录>")
        sys.exit(1)
    
    analyze_lua_files(sys.argv[1]) 
