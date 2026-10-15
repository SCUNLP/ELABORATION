from pymongo import MongoClient
from dateutil import parser

import os
import time

from .apis import (
    get_contest_list,
    get_contest_metadata,
    get_division_metadata,
    get_problem_metadata,
    get_explained_solution_list,
    get_solution_list,
    get_solution,
    get_annotation,
)
from .config import start_time, end_time, sleep_time

valid_languages = ["PYTH 3", "PYPY3"]


def get_db_client():
    mongo_connection_uri = os.environ.get("ME_CONFIG_MONGODB_URL")
    client = MongoClient(mongo_connection_uri)
    return client["codechef"]


def get_collection_dict():
    """
    获取集合字典
    contest_brief: 比赛简要信息
    contest_metadata: 比赛元数据
    division_metadata: 比赛分区元数据
    """
    db = get_db_client()
    return {
        "contest_brief": db["contest_brief"],
        "contest_metadata": db["contest_metadata"],
        "division_metadata": db["division_metadata"],
        "problem_metadata": db["problem_metadata"],
        "explained_solution": db["explained_solution"],
        "correct_solution": db["correct_solution"],
        "solution": db["solution"],
    }


def prepare_contest_data(contest):
    # 将字符串时间转换为 datetime 对象
    contest["contest_start_date"] = parser.isoparse(contest["contest_start_date_iso"])
    contest["contest_end_date"] = parser.isoparse(contest["contest_end_date_iso"])
    del contest["contest_start_date_iso"]
    del contest["contest_end_date_iso"]
    return contest


def get_all_contests():
    """
    获取所有比赛的列表
    """
    offset = 0

    collections = get_collection_dict()
    contest_brief = collections["contest_brief"]
    existing_contest_code = set(
        contest["contest_code"]
        for contest in contest_brief.find({}, {"contest_code": 1})
    )

    while True:
        print(f"Fetching contests from offset {offset}...")
        current_contests = get_contest_list(offset)
        if not current_contests:
            break
        offset += len(current_contests)
        new_contests = [
            prepare_contest_data(contest)
            for contest in current_contests
            if contest["contest_code"] not in existing_contest_code
        ]
        if new_contests:
            print(f"Found {len(new_contests)} new contests.")
            contest_brief.insert_many(new_contests)
            existing_contest_code.update(
                contest["contest_code"] for contest in new_contests
            )
        else:
            print("No new contests found.")

        time.sleep(sleep_time)


def get_all_contest_metadata_by_time():
    """
    获取比赛元数据
    """
    collections = get_collection_dict()
    contest_metadata = collections["contest_metadata"]
    contest_brief = collections["contest_brief"]

    # 获取所有比赛的列表
    for contest in contest_brief.find():
        if (
            contest["contest_start_date"] < start_time
            or contest["contest_end_date"] > end_time
        ):
            continue
        contest_code = contest["contest_code"]
        if contest_metadata.find_one({"code": contest_code}):
            # print(f"Contest {contest_code} metadata already exists.")
            continue
        print(f"Fetching metadata for contest {contest_code}...")
        metadata = get_contest_metadata(contest_code)
        if metadata:
            contest_metadata.insert_one(metadata)
        else:
            print(f"Failed to fetch metadata for contest {contest_code}.")
        time.sleep(sleep_time)


def get_all_division_metadata():
    """
    获取所有division的元数据
    """
    collections = get_collection_dict()
    contest_metadata = collections["contest_metadata"]
    division_metadata = collections["division_metadata"]

    for contest in contest_metadata.find():
        child_contests = contest["child_contests"]
        for division_brief in child_contests.values():
            division_code = division_brief["contest_code"]
            division_link = division_brief["contest_link"]
            if division_metadata.find_one({"code": division_code}):
                # print(f"Division {division_code} metadata already exists.")
                continue
            metadata = get_division_metadata(division_link)
            if metadata:
                division_metadata.insert_one(metadata)
            else:
                print(f"Failed to fetch metadata for division {division_code}.")
            time.sleep(sleep_time)


def get_all_problem_related_metadata():
    """
    获取所有与problem相关的元数据，包括：
    1. problem_metadata
    2. submission_metadata
    """
    collections = get_collection_dict()
    division_metadata = collections["division_metadata"]
    problem_metadata = collections["problem_metadata"]
    explained_solution = collections["explained_solution"]
    correct_solution = collections["correct_solution"]

    for division in division_metadata.find():
        problems = division["problems"]
        for problem_brief in problems.values():
            problem_code = problem_brief["code"]
            problem_url = problem_brief["problem_url"]

            # problem_metadata
            if problem_metadata.find_one({"code": problem_code}):
                # print(f"Problem {problem_code} metadata already exists.")
                pass
            else:
                metadata = get_problem_metadata(problem_url)
                if metadata:
                    metadata["code"] = problem_code
                    problem_metadata.insert_one(metadata)
                else:
                    print(f"Failed to fetch metadata for problem {problem_code}.")
                time.sleep(sleep_time)

            # explained_solution
            if explained_solution.find_one({"code": problem_code}):
                # print(f"Problem {problem_code} explained solution already exists.")
                pass
            else:
                explained_solution_list = get_explained_solution_list(problem_code)
                if explained_solution_list:
                    explained_solution_list["code"] = problem_code
                    explained_solution.insert_one(explained_solution_list)
                else:
                    print(
                        f"Failed to fetch explained solution for problem {problem_code}."
                    )
                time.sleep(sleep_time)

            # correct_solution
            if correct_solution.find_one({"code": problem_code}):
                # print(f"Problem {problem_code} correct solution already exists.")
                pass
            else:
                try:
                    data_list = []
                    for language in valid_languages:
                        correct_solution_list = get_solution_list(
                            problem_code, language
                        )
                        time.sleep(sleep_time * 5)
                        data_list.extend(correct_solution_list["data"])
                    correct_solution_list["data"] = data_list
                except Exception as e:
                    print(
                        f"Failed to fetch correct solution for problem {problem_code}. Error: {e}"
                    )
                    continue
                if correct_solution_list:
                    correct_solution_list["code"] = problem_code
                    correct_solution.insert_one(correct_solution_list)
                else:
                    print(
                        f"Failed to fetch correct solution for problem {problem_code}."
                    )


def get_all_solutions():
    """
    获取所有的solution内容，以及相关的注释（如果有）
    """
    collections = get_collection_dict()
    solution = collections["solution"]
    explained_solution = collections["explained_solution"]
    correct_solution = collections["correct_solution"]

    explained_solution_set = set()
    correct_solution_set = set()

    for explained in explained_solution.find():
        for item in explained["annotations"]:
            if item["language"] in valid_languages:
                explained_solution_set.add(item["submission_id"])

    for correct in correct_solution.find():
        for item in correct["data"]:
            correct_solution_set.add(item["solution"])

    correct_solution_set = correct_solution_set - explained_solution_set
    for submission_id in explained_solution_set:
        if solution.find_one({"submission_id": submission_id}):
            # print(f"Solution for submission {submission_id} already exists.")
            continue
        submission = dict()
        solution_data = get_solution(submission_id)
        annotation_data = get_annotation(submission_id)
        if solution_data:
            submission["submission_id"] = submission_id
            submission["solution"] = solution_data["data"]
            submission["annotation"] = annotation_data["annotations"]
            solution.insert_one(submission)
        else:
            print(f"Failed to fetch solution for submission {submission_id}.")
        time.sleep(sleep_time)
    for submission_id in correct_solution_set:
        if solution.find_one({"submission_id": submission_id}):
            # print(f"Solution for submission {submission_id} already exists.")
            continue
        submission = dict()
        solution_data = get_solution(submission_id)
        if solution_data:
            submission["submission_id"] = submission_id
            try:
                submission["solution"] = solution_data["data"]
            except:
                print(solution_data)
                continue
            submission["annotation"] = []
            solution.insert_one(submission)
        else:
            print(f"Failed to fetch solution for submission {submission_id}.")
        time.sleep(sleep_time)
