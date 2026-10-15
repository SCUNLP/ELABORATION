import os
import json
from pathlib import Path

# 设置文件路径
input_file = "atcoder.jsonl"
output_files = ["atcoder1.jsonl", "atcoder2.jsonl", "atcoder3.jsonl"]

# 读取原始 jsonl 数据
with open(input_file, "r", encoding="utf-8") as f:
    lines = [json.loads(line) for line in f]

# 按 id 排序（确保分组有序）
lines.sort(key=lambda x: x["id"])

# 平均分成三组
total = len(lines)
chunk_size = (total + 2) // 3  # ceil(total/3)

chunks = [lines[i * chunk_size: (i + 1) * chunk_size] for i in range(3)]

# 写入新文件
for i in range(3):
    with open(output_files[i], "w", encoding="utf-8") as f:
        for item in chunks[i]:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"已将 {input_file} 平均分割为：{', '.join(output_files)}")
