# Codechef比赛数据爬取

实现了完全增量式的数据爬取

## 运行须知

1. `apis.py`文件中的函数每次使用时，`cookies`和`headers`需要更新
2. 每次运行时，需要更新`.env`中的`START_TIME`和`END_TIME`，留空视为不做限制

## 数据表含义
- `contest_brief` 比赛简要信息（主键为`contest_code`）
- `contest_metadata` 详细的比赛元数据
- `division_metadata` 详细的分区元数据
- `problem_metadata` 题目元数据
- `explained_solution` 有题解的solution的列表
- `correct_solution` AC的solution的列表
- `solution` solution的内容（包括annotation）

## 脚本文件用途
- `process.py` 运行爬虫程序，并将数据保存到mongodb中（反复运行直到不报错为止）
- `dump.py` 导出数据为jsonl格式
