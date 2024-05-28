import re
import json
from collections import defaultdict
import time

# 定义日志的正则表达式模式
log_pattern = re.compile(
    r'(?P<ip>[\d\.]+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<url>[^\s]+) (?P<protocol>[^\"]+)" (?P<status>\d+) (?P<size>\d+) "(?P<referer>[^\"]*)" "[^\"]*"'
)

# 文件路径
log_file_path = "/home/yifannus2023/TamperLogPrompt/Train_data_modify.txt"
task_file_path = "/home/yifannus2023/TamperLogPrompt/pre_defined_task.json"

# 读取日志文件
def read_log_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

# 读取预定义任务文件
def read_task_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# 检查日志组是否符合种子模板
def check_group_with_seeds(expanded_seed_logs,group):
    group_logs = [[f"{entry['method']}<{entry['url']}", entry['referer'].split("32677/")[1].split("?")[0]] for entry in group if ("/index.html" not in entry['url'] and "/api/v1/verifycode/generate" not in entry['url'])]
    print("fjkaf",len(group_logs),len(expanded_seed_logs),expanded_seed_logs)
    if len(group_logs) >= len(expanded_seed_logs):
        for api in group_logs:
            FLAG = False
            print("new",api)
                
            for expanded_seed_l in expanded_seed_logs:
                # print(expanded_seed_l)
                if len(expanded_seed_l[0]) == 1:
                    print("4331",api, expanded_seed_l[0],expanded_seed_l[1])
                    if expanded_seed_l[0][0] in api[0] and expanded_seed_l[1] in api[1]:
                        FLAG = True
                        break
                else:
                    print("433",api, expanded_seed_l[0],expanded_seed_l[1])
                    for seed_log in expanded_seed_l[0]:
                        if seed_log in api[0] and expanded_seed_l[1] in api[1]:
                            FLAG = True
                            break
            if not FLAG:
                return False
        return True
    else: return False

# 记录符合条件的序列
def match_logs_with_tasks(index_logs, tasks):
    sequences = defaultdict(set)
    group_indices = defaultdict(set)
    expanded_seed_logs = {}
            
    for task_name,seeds in tasks.items():
        extend_logs = []
        for seed in seeds:
            # print(seed)
            if len(seed) == 2:
                seed_logs, seed_end = seed
                # if len(seed_logs) > 1:
                #     for i in seed_logs:
                #         extend_logs.append([i, seed_end])
                # else:
                extend_logs.append([seed_logs, seed_end])
                
        expanded_seed_logs[task_name] = extend_logs
    print("e4343",expanded_seed_logs)
    time.sleep(3)
    for index, group in index_logs:
        if index in {2}:
            # print(index,group)
            for task_name, seeds in tasks.items():
                # if "trainticket_getorder_seeds" in task_name:
                    # print('login seeds',seeds)
                    FLAG = check_group_with_seeds(expanded_seed_logs[task_name],group)
                    if FLAG:
                        sequence = tuple(f"{entry['method']}<{normalize_url(entry['url'])}" for entry in group)

                        print("the seq is:",index,sequence)
                        if sequence not in sequences[task_name]:
                            sequences[task_name].add(sequence)
                            group_indices[task_name].add(index)

    return group_indices

def normalize_url(url):
    specific_apis = [
        "/api/v1/cancelservice/cancel/refound/",
        "/api/v1/cancelservice/cancel/",
        "/api/v1/consignservice/consigns/account/",
        "/api/v1/consignservice/consigns/order/",
        "/api/v1/foodservice/foods/",
        "/api/v1/contactservice/contacts/account/",
        "/api/v1/executeservice/execute/execute/",
        "/api/v1/executeservice/execute/collected/"
    ]
    for api in specific_apis:
        if api in url:
            return api
    return url

def remove_subsets(seed_sets):
    keys = list(seed_sets.keys())
    for i in range(len(keys)):
        for j in range(len(keys)):
            if i != j and seed_sets[keys[i]].issubset(seed_sets[keys[j]]):
                # 一个一个元素删除子集中的元素
                for element in seed_sets[keys[i]]:
                    if element in seed_sets[keys[j]]:
                        seed_sets[keys[j]].remove(element)
    return seed_sets

def main():
    log_lines = read_log_file(log_file_path)
    tasks = read_task_file(task_file_path)
    
    index_logs = []
    capture = False
    log_group = []
    group_index = 1

    # 读取并解析日志文件
    for line in log_lines:
        match = log_pattern.match(line)
        if match:
            data = match.groupdict()
            if data['method'] == 'GET' and data['url'] == '/index.html':
                if capture:
                    # 将当前组添加到 index_logs 中，并重置 log_group
                    index_logs.append((group_index, log_group))
                    group_index += 1
                    log_group = []
                capture = True
            log_group.append(data)

    if log_group:
        index_logs.append((group_index, log_group))

    group_indices = match_logs_with_tasks(index_logs, tasks)

    for task_name, indices in group_indices.items():
        print("====")
        print(f"{task_name}: {indices}")



    # 执行函数
    result = remove_subsets(group_indices)
    print(result)
    

if __name__ == "__main__":
    main()
