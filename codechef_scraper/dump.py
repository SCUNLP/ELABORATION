from datetime import datetime

from scraper.utils import get_collection_dict, valid_languages

collections = get_collection_dict()
contest_metadata = collections["contest_metadata"]
problem_metadata = collections["problem_metadata"]
explained_solution = collections["explained_solution"]
correct_solution = collections["correct_solution"]
solution = collections["solution"]

contest_id_set = set()
problem_id_set = set()
min_start = 0xFFFFFFFFFFFFFFFF
max_end = 0

contest_id_to_metadata = dict()
problem_id_to_submission_metadata = dict()
submission_id_to_content = dict()


for contest in contest_metadata.find():
    contest_id = contest["code"]
    start_time = contest["time"]["start"]
    end_time = contest["time"]["end"]
    if start_time < min_start:
        min_start = start_time
    if end_time > max_end:
        max_end = end_time

    contest_id_set.add(contest_id)
    del contest["_id"]
    contest_id_to_metadata[contest_id] = contest
    contest_id_to_metadata[contest_id]["contest_id"] = contest_id
    contest_id_to_metadata[contest_id]["problems"] = []

min_start_str = datetime.fromtimestamp(min_start).strftime(r"%Y-%m-%d")
max_end_str = datetime.fromtimestamp(max_end).strftime(r"%Y-%m-%d")

for problem in problem_metadata.find():
    contest_id = problem["intended_contest_code"]
    problem_id = problem["code"]
    if contest_id not in contest_id_set:
        # print(f"Problem {problem['code']} has an invalid contest ID: {contest_id}")
        continue
    problem_id_set.add(problem_id)
    del problem["_id"]
    contest_id_to_metadata[contest_id]["problems"].append(
        {
            "problem_id": problem_id,
            "contest_id": contest_id,
            "submissions": [],
            **problem,
        }
    )

# 先插入AC的solution
for solution_list in correct_solution.find():
    problem_id = solution_list["code"]
    if problem_id not in problem_id_set:
        # print(
        #     f"Correct solution {solution_list['code']} has an invalid problem ID: {problem_id}"
        # )
        continue

    if problem_id not in problem_id_to_submission_metadata:
        problem_id_to_submission_metadata[problem_id] = dict()
    data_list = solution_list["data"]
    for data_item in data_list:
        if data_item["language"] not in valid_languages:
            continue
        submission_id = data_item["id"]
        problem_id_to_submission_metadata[problem_id][submission_id] = data_item


# 然后用explained_solution覆盖
for solution_list in explained_solution.find():
    problem_id = solution_list["code"]
    if problem_id not in problem_id_set:
        # print(
        #     f"Explained solution {solution_list['code']} has an invalid problem ID: {problem_id}"
        # )
        continue

    if problem_id not in problem_id_to_submission_metadata:
        problem_id_to_submission_metadata[problem_id] = dict()
    annotations = solution_list["annotations"]
    for annotation in annotations:
        if annotation["language"] not in valid_languages:
            continue
        submission_id = annotation["submission_id"]
        if submission_id not in problem_id_to_submission_metadata[problem_id]:
            problem_id_to_submission_metadata[problem_id][submission_id] = annotation
        else:
            problem_id_to_submission_metadata[problem_id][submission_id].update(
                annotation
            )

for submission in solution.find():
    submission_id = submission["submission_id"]
    del submission["_id"]
    submission_id_to_content[submission_id] = submission

import json

output_filename = f"codechef_{min_start_str}_{max_end_str}.jsonl"

for metadata in contest_id_to_metadata.values():
    contest_id = metadata["contest_id"]
    for problem in metadata["problems"]:
        problem_id = problem["problem_id"]
        for submission_id, submission_metadata in problem_id_to_submission_metadata[
            problem_id
        ].items():
            if submission_id not in submission_id_to_content:
                # print(
                #     f"Submission {submission_id} has an invalid ID: {submission_id}"
                # )
                continue
            content = submission_id_to_content[submission_id]
            submission_metadata.update(content)
            submission_metadata["contest_id"] = contest_id
            submission_metadata["problem_id"] = problem_id
            problem["submissions"].append(submission_metadata)

with open(output_filename, "w") as f:
    for metadata in contest_id_to_metadata.values():
        f.write(json.dumps(metadata) + "\n")
