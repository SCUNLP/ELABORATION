# Codeforces比赛数据爬取

实现了完全增量式的数据爬取

## 运行须知

1. `apis.py`文件中的函数每次使用时，`cookies`和`headers`需要更新
2. 每次运行时，需要更新`.env`中的`START_TIME`和`END_TIME`，留空视为不做限制

## 数据表含义


## 脚本文件用途
- `process.py` 运行爬虫程序，并将数据保存到mongodb中（反复运行直到不报错为止）
- `dump.py` 导出数据为jsonl格式
