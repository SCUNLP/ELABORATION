from dateutil import parser
from datetime import datetime

import os

# 每次请求后等待的时间
sleep_time = 1

# 定义默认的时间范围（非常宽泛）
DEFAULT_START_TIME = datetime(1970, 1, 1)  # Unix 纪元起始
DEFAULT_END_TIME = datetime(2099, 12, 31)  # 遥远的未来

start_time_str = os.environ.get("START_TIME")
end_time_str = os.environ.get("END_TIME")

start_time = DEFAULT_START_TIME
if start_time_str:
    try:
        start_time = parser.parse(start_time_str)
    except (ValueError, TypeError):
        print(f"Invalid START_TIME format: {start_time_str}. Using default start time.")

end_time = DEFAULT_END_TIME
if end_time_str:
    try:
        end_time = parser.parse(end_time_str)
    except (ValueError, TypeError):
        print(f"Invalid END_TIME format: {end_time_str}. Using default end time.")

__all__ = ["start_time", "end_time", "sleep_time"]
