import re
import os
import json
from datetime import datetime

import numpy as np

log_format = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}\s\w+\s+1\s---\s\[.*\]\s[a-zA-z.]+:\s(?P<content>.*)"
arguments_format = r"^\[(?P<values>.*), \[.*\]\]"

patterns = [
    {
        "prefix": "Before executing method:",
        "regex":  r"^Before executing method: (?P<method>.*)$",
        "groups": ["method"]
    },
    {
        "prefix": "Entering in Method:",
        "regex": r"^Entering in Method: (?P<method>.*), Class: (?P<class>.*), Arguments: (?P<arguments>.*), Request Headers: (?P<headers>.*), Execution Time: (?P<time>.*) milliseconds, Return: (?P<return>.*)$",
        "groups": ["method", "class", "arguments", "headers", "time", "return"]
    },
    {
        "prefix": "Successfully executed method:",
        "regex": r"^Successfully executed method: (?P<method>.*)$",
        "groups": ["method"]
    },
    {
        "prefix": "Before execution of repository method:",
        "regex": r"^Before execution of repository method: (?P<method>.*)$",
        "groups": ["method"]
    },
    {
        "prefix": "Execution of repository method:",
        "regex": r"^Execution of repository method: (?P<method>.*), Execution Time: (?P<time>.*) milliseconds, Result: (?P<result>.*)$",
        "groups": ["method", "time", "result"]
    }
]

def parse_log(log: str):
    match = re.match(log_format, log)
    if not match: return -1, {}

    content = match.groupdict().get("content", None)
    assert content is not None

    result = {}
    for i, pattern in enumerate(patterns):
        if content.startswith(pattern["prefix"]):
            match = re.match(pattern["regex"], content)
            assert match is not None

            groups = match.groupdict()
            for group in pattern["groups"]:
                result[group] = groups.get(group)
                assert result[group] is not None

            break

    if "arguments" in result:
        match = re.match(arguments_format, result["arguments"])
        if match:
            values = match.groupdict().get("values")
            result["arguments"] = values
        else:
            result["arguments"] = ""

    return i, result
        
logs = open("./Train_data_modify.txt").read().splitlines()


method_data = {}
repository_method_data = {}

for log in logs:
    pattern_type, data = parse_log(log)
    if not data: continue

    if pattern_type == 1:
        method = data["method"] 
        method_data[method] = method_data.get(method, []) + [data]

    elif pattern_type == 4:
        method = data["method"] 
        repository_method_data[method] = method_data.get(method, []) + [data]

for method_name, replicas in method_data.items():
    if len(replicas) <= 1: continue
    snapshots: list[np.ndarray] = np.split(replicas, np.arange(5, len(replicas), 20))
    target_dir = os.path.join(os.getcwd(), 'dataset', 'method', method_name)
    if not os.path.exists(target_dir): os.makedirs(target_dir, exist_ok=True)

    for i, snapshot in enumerate(snapshots):
        if len(snapshot.tolist()) <= 1: continue
        with open(f"./dataset/method/{method_name}/snapshot_{i}.json", "w") as f:
            json.dump(snapshot.tolist(), f)

for method_name, replicas in repository_method_data.items():
    if len(replicas) <= 1: continue
    snapshots: list[np.ndarray] = np.split(replicas, np.arange(20, len(replicas), 20))
    target_dir = os.path.join(os.getcwd(), 'dataset', 'repository_method', method_name)
    if not os.path.exists(target_dir): os.makedirs(target_dir, exist_ok=True)

    for i, snapshot in enumerate(snapshots):
        if len(snapshot.tolist()) <= 1: continue
        with open(f"./dataset/repository_method/{method_name}/snapshot_{i}.json", "w") as f:
            json.dump(snapshot.tolist(), f)