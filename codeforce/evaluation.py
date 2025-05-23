import os
import json
import subprocess
import resource

CODEFORCE_FILE = 'codeforce.jsonl'
CODE_DIR = 'text'
TEMP_CODE = 'temp_check.py'
RESULTS = []

def limit_memory(memory_mb):
    """限制子进程内存（单位：MB）"""
    memory_bytes = memory_mb * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, memory_bytes))

# 读取 codeforce.jsonl 到 id -> {samples, time_limit, memory_limit}
id2info = {}
with open(CODEFORCE_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            obj = json.loads(line.strip())
            obj_id = str(obj.get("id"))
            if obj_id and "input_output" in obj:
                id2info[obj_id] = {
                    "samples": obj["input_output"],
                    "time_limit": obj.get("time_limit", 2),  # 默认 2s
                    "memory_limit": obj.get("memory_limit", 256),  # 默认 256MB
                }
        except Exception as e:
            print(f" Failed to parse JSONL line: {e}")

# 遍历所有代码文件
for filename in os.listdir(CODE_DIR):
    if filename.endswith(".python"):
        problem_id = filename.replace(".python", "")
        filepath = os.path.join(CODE_DIR, filename)

        if problem_id not in id2info:
            print(f" ID {problem_id} not found in codeforce.jsonl")
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()

        info = id2info[problem_id]
        time_limit = info["time_limit"]
        memory_limit = info["memory_limit"]
        samples = info["samples"]

        total = len(samples)
        passed = 0
        for idx, case in enumerate(samples):
            test_input = case["input"]
            expected_output = case["output"].strip()

            with open(TEMP_CODE, 'w', encoding='utf-8') as temp_file:
                temp_file.write(code)
                temp_file.write("\n\n")
                temp_file.write("if __name__ == '__main__':\n")
                temp_file.write("    solve()\n")

            try:
                result = subprocess.run(
                    ['python3', TEMP_CODE],
                    input=test_input,
                    text=True,
                    capture_output=True,
                    timeout=time_limit,
                    preexec_fn=lambda: limit_memory(memory_limit)
                )
                output = result.stdout.strip()

                if output == expected_output:
                    passed += 1
                else:
                    print(f" ID {problem_id} - Case {idx+1}: Wrong Answer (WA)")
                    print(f"Input:\n{test_input}")
                    print(f"Expected:\n{expected_output}")
                    print(f"Got:\n{output}")

            except subprocess.TimeoutExpired:
                print(f" ID {problem_id} - Case {idx+1}: Time Limit Exceeded (TLE)")
            except MemoryError:
                print(f" ID {problem_id} - Case {idx+1}: Memory Limit Exceeded (MLE)")
            except Exception as e:
                print(f" ID {problem_id} - Case {idx+1}: Runtime Error (RE): {e}")

        print(f" ID {problem_id}: Passed {passed}/{total}\n")
        RESULTS.append((problem_id, passed, total))


if os.path.exists(TEMP_CODE):
    os.remove(TEMP_CODE)

# 打印总结
print("\n=== SUMMARY ===")
for pid, p, t in RESULTS:
    print(f"{pid}: {p}/{t} passed")
