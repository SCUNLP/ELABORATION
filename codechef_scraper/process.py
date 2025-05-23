from scraper.utils import (
    get_all_contests,
    get_all_contest_metadata_by_time,
    get_all_division_metadata,
    get_all_problem_related_metadata,
    get_all_solutions,
)

# 获取比赛列表
get_all_contests()

# 获取范围内比赛信息（需要先更新.env文件）
get_all_contest_metadata_by_time()

# 根据比赛信息，获取所有的division元信息
get_all_division_metadata()

# 根据题目信息，获取1. problem_metadata 2. explained_solusions 3. correct_solutions
get_all_problem_related_metadata()

# 获取solutions，某些solution会包含annotation
get_all_solutions()
