import re
import json
from collections import defaultdict, deque
import time
from datetime import datetime
import sys
import os
from dotenv import load_dotenv
import argparse
import glob
import subprocess
sys.path.append('../consistency_prompt/examples')
sys.path.append('../consistency_prompt')
sys.path.append('../consistency_prompt/gptchecker')
import data_relationship
import ast
from gptchecker import GPTChecker
# import trigger_code_parse

skip_elements = [
    "travel2.service.TravelServiceImpl.queryByBatch > preserve.service.PreserveServiceImpl.preserve",
    "travel.service.TravelServiceImpl.queryByBatch > preserveOther.service.PreserveOtherServiceImpl.preserve",
    "order.service.OrderServiceImpl.queryOrdersForRefresh > cancel.service.CancelServiceImpl.calculateRefund",
    "other.service.OrderOtherServiceImpl.queryOrdersForRefresh > execute.service.ExecuteServiceImpl.ticketCollect",
    "other.service.OrderOtherServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.queryByOrderId",
    "auth.service.impl.TokenServiceImpl.getToken > user.service.impl.UserServiceImpl.getAllUsers",
    "auth.service.impl.TokenServiceImpl.getToken > foodsearch.service.FoodServiceImpl.getAllFood",
    "auth.service.impl.TokenServiceImpl.getToken > assurance.service.AssuranceServiceImpl.getAllAssuranceTypes",
    "auth.service.impl.TokenServiceImpl.getToken > contacts.service.ContactsServiceImpl.findContactsByAccountId",
    "foodsearch.service.FoodServiceImpl.getAllFood > preserve.service.PreserveServiceImpl.preserve",
    "verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken",
    "auth.service.impl.TokenServiceImpl.getToken > execute.service.ExecuteServiceImpl.ticketCollect",
    "other.service.OrderOtherServiceImpl.queryOrdersForRefresh > cancel.service.CancelServiceImpl.calculateRefund"
]

env_path = '../consistency_prompt/.env'
load_dotenv(dotenv_path=env_path)
api_key = os.getenv('API_KEY')

dataflow = """
#trainticket_login_seeds: ['verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh','auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh','auth.service.impl.TokenServiceImpl.getToken > user.service.impl.UserServiceImpl.getAllUsers'] 52s
#trainticket_cancel_seeds: ['verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'order.service.OrderServiceImpl.queryOrdersForRefresh > cancel.service.CancelServiceImpl.calculateRefund', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > cancel.service.CancelServiceImpl.calculateRefund'] 9.6909s
#getorder:['auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh'] 19.0419 seconds
#trainticket_change_seeds: ['auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > travel.service.TravelServiceImpl.queryByBatch', 'auth.service.impl.TokenServiceImpl.getToken > travel2.service.TravelServiceImpl.queryByBatch', 'auth.service.impl.TokenServiceImpl.getToken > rebook.service.RebookServiceImpl.rebook', 'travel.service.TravelServiceImpl.queryByBatch > rebook.service.RebookServiceImpl.rebook','rebook.service.RebookServiceImpl.rebook > inside_payment.service.InsidePaymentServiceImpl.payDifference'] 20.95
#getConsign:['auth.service.impl.TokenServiceImpl.getToken > consign.service.ConsignServiceImpl.queryByAccountId'] 11.62
#getCollect:['verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh'] 13.8993
#trainticket_enter_seeds:['auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > execute.service.ExecuteServiceImpl.ticketExecute', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > execute.service.ExecuteServiceImpl.ticketExecute','order.service.OrderServiceImpl.queryOrdersForRefresh > execute.service.ExecuteServiceImpl.ticketExecute', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > execute.service.ExecuteServiceImpl.ticketExecute'] 15.6334
#getEnter:['verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh'] 17.6727
#trainticket_pay_seeds:['auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'order.service.OrderServiceImpl.queryOrdersForRefresh > inside_payment.service.InsidePaymentServiceImpl.pay', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > inside_payment.service.InsidePaymentServiceImpl.pay', 'inside_payment.service.InsidePaymentServiceImpl.pay > order.service.OrderServiceImpl.queryOrdersForRefresh', 'inside_payment.service.InsidePaymentServiceImpl.pay > other.service.OrderOtherServiceImpl.queryOrdersForRefresh'] 29.5432s
#trainticket_consign_seeds: ['auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.queryByOrderId', 'order.service.OrderServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.queryByOrderId'] 12.95 ['verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh'] 16.577 ['auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'order.service.OrderServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.queryByOrderId', 'order.service.OrderServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.updateConsignRecord', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.queryByOrderId', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.updateConsignRecord'] 22.2460
#trainticket_preserve_seeds: ['verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken', 'auth.service.impl.TokenServiceImpl.getToken > assurance.service.AssuranceServiceImpl.getAllAssuranceTypes', 'auth.service.impl.TokenServiceImpl.getToken > contacts.service.ContactsServiceImpl.findContactsByAccountId', 'auth.service.impl.TokenServiceImpl.getToken > foodsearch.service.FoodServiceImpl.getAllFood', 'auth.service.impl.TokenServiceImpl.getToken > preserveOther.service.PreserveOtherServiceImpl.preserve', 'contacts.service.ContactsServiceImpl.findContactsByAccountId > preserveOther.service.PreserveOtherServiceImpl.preserve', 'travel2.service.TravelServiceImpl.queryByBatch > preserveOther.service.PreserveOtherServiceImpl.preserve','contacts.service.ContactsServiceImpl.findContactsByAccountId > preserve.service.PreserveServiceImpl.preserve', 'foodsearch.service.FoodServiceImpl.getAllFood > preserve.service.PreserveServiceImpl.preserve','auth.service.impl.TokenServiceImpl.getToken > preserve.service.PreserveServiceImpl.preserve','travel.service.TravelServiceImpl.queryByBatch > preserve.service.PreserveServiceImpl.preserve'] 16s
#trainticket_collect_seeds: ['auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > execute.service.ExecuteServiceImpl.ticketCollect', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'order.service.OrderServiceImpl.queryOrdersForRefresh > execute.service.ExecuteServiceImpl.ticketCollect', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > execute.service.ExecuteServiceImpl.ticketCollect'] 28.3366
#trainticket_advancedsearch_seeds: [] 6.99,29.64,11.0810
#
"""

dataflowFLAG = False
TriggerflowFLAG = True

# 定义日志的正则表达式模式
log_pattern = re.compile(
    r'(?P<ip>[\d\.]+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<url>[^\s]+) (?P<protocol>[^\"]+)" (?P<status>\d+) (?P<size>\d+) "(?P<referer>[^\"]*)" "[^\"]*"'
)
checker = GPTChecker(
    api_key=api_key,
    model="gpt-4o",
    max_tokens=2048,
    top_p=0.9,
    temperature=0.0
)
# 文件路径
log_file_path = "Train_data_modify.txt"
task_file_path = "pre_defined_task.json"
API_service_path = "API_service.json"
with open("openAPI.json") as fp:
    OPENAPI = json.load(fp)
    
with open("log_target.json") as fp:
    desire_log = json.load(fp)
    
with open("API_service.json") as fp:
    API_service = json.load(fp)

with open('trainticket_class_def.json') as fp:
    trainticket_class_def = json.load(fp)

with open('../data_constraints.json') as fp:
    data_constrains = json.load(fp)

with open('dataset/dataflow_transition/dataflow.json') as fp:
    data_constrains_logs = json.load(fp)
    
with open('dataset/trigger_transition/trigger.json') as fp:
    trigger_constrains_logs = json.load(fp)

def read_log_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

# 读取预定义任务文件
def read_task_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# 检查日志组是否符合种子模板
def check_group_with_seeds(expanded_seed_logs, group):
    group_logs = [[f"{entry['method']}<{entry['url']}", entry['referer'].split("32677/")[1].split("?")[0]] 
                  for entry in group if ("/index.html" not in entry['url'] and "/api/v1/verifycode/generate" not in entry['url'])]
    
    if len(group_logs) < len(expanded_seed_logs) or ("foodservice" in group_logs[-1][0]) or ("contact" in group_logs[-1][0]):
        return False
    
    for api in group_logs:
        FLAG = False
        for expanded_seed_l in expanded_seed_logs:
            for seed_log in expanded_seed_l[0]:
                if isinstance(expanded_seed_l[1], str):
                    if seed_log in api[0] and expanded_seed_l[1] in api[1]:
                        FLAG = True
                        break
                else:
                    if any(seed_log in api[0] and path in api[1] for path in expanded_seed_l[1]):
                        FLAG = True
                        break
        if not FLAG:
            return False
    return True


# 记录符合条件的序列
def match_logs_with_tasks(index_logs, tasks):
    sequences = defaultdict(set)
    group_indices = defaultdict(set)
    expanded_seed_logs = {}
            
    for task_name,seeds in tasks.items():
        extend_logs = []
        for seed in seeds:
            # #print(seed)
            if len(seed) == 2:
                seed_logs, seed_end = seed
                # if len(seed_logs) > 1:
                #     for i in seed_logs:
                #         extend_logs.append([i, seed_end])
                # else:
                extend_logs.append([seed_logs, seed_end])
                
        expanded_seed_logs[task_name] = extend_logs
    # #print("e4343",expanded_seed_logs)
    # time.sleep(3)
    for index, group in index_logs:
        # if index in {331, 372, 37}:
            # #print(index,group)
            for task_name, seeds in tasks.items():
                # if "trainticket_change_seeds" in task_name:
                    # #print('login seeds',seeds)
                    FLAG = check_group_with_seeds(expanded_seed_logs[task_name],group)
                    if FLAG:
                        # time.sleep(5)
                        sequence = [f"{entry['method']}<{normalize_url(entry['url'])}" for entry in group]
                        sequence = normalize_sequence(sequence)
                        sequence = tuple(sequence)
                        # #print("the seq is:",index,sequence)
                        if sequence not in sequences[task_name]:
                            sequences[task_name].add(sequence)
                            group_indices[task_name].add(index)

    return group_indices

def normalize_sequence(sequence):
    api_pairs = [
        ["/api/v1/orderservice/order/refresh", "/api/v1/orderOtherService/orderOther/refresh"],
        ["/api/v1/travel2service/trips/left", "/api/v1/travelservice/trips/left"],
        ["/api/v1/foodservice/foods/", "/api/v1/contactservice/contacts/account/", "/api/v1/assuranceservice/assurances/types"]
    ]
    sorted_entries = []
    for pair in api_pairs:
        for api in pair:
            sorted_entries.extend([entry for entry in sequence if api in entry])
    sorted_entries.extend([entry for entry in sequence if all(api not in entry for pair in api_pairs for api in pair)])
    return sorted_entries

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
    # #print(keys)
    for i in range(len(keys)):
        # #print(keys[i])
        if "login_seeds" not in keys[i]:
            for j in range(len(keys)):
                if "login_seeds" not in keys[j]:
                    if i != j and seed_sets[keys[i]].issubset(seed_sets[keys[j]]):
                        # 一个一个元素删除子集中的元素
                        for element in seed_sets[keys[i]]:
                            if element in seed_sets[keys[j]]:
                                seed_sets[keys[j]].remove(element)
    return seed_sets

def issuperset(seqA,seqB):
    # #print("eee",seqA,seqB)
    for i in seqA:
        if i not in seqB:
            return False
    for i in seqB:
        if i not in seqA:
            return False
    return True

def match_log_with_api(log_entry):    
    """
    根据日志条目匹配相应的API定义
    """
    method_url = f"{log_entry['method']} {log_entry['url']}".lower()
    return next((api_name for api_name, api_url in OPENAPI.items() if api_url.lower() in method_url), None)


def convert_to_datetime(timestamp_str):
    # 拆分日期和时间部分
    date_str, rest = timestamp_str.split(':', 1)
    time_str, tz_and_microseconds = rest.split(' ', 1)
    # #print(tz_and_microseconds.split('.'))
    tz_str, _,microseconds_str = tz_and_microseconds.split('.')
    
    # 获取微秒部分的最后三位数字
    microseconds = int(microseconds_str[-3:]) * 1000
    
    # 合并日期和时间部分，并解析时区
    datetime_part = datetime.strptime(date_str + ':' + time_str, "%d/%b/%Y:%H:%M:%S")
    
    # 将微秒部分添加到datetime对象
    final_datetime = datetime_part.replace(microsecond=microseconds)
    # #print(final_datetime)
    return final_datetime

def find_between_log(logs, startingtime, endingtime):
    log_timestamp1 = convert_to_datetime(startingtime)
    log_timestamp2 = convert_to_datetime(endingtime)
    for log in logs:
        parsedlogs = parse_log(log)
        if parsedlogs and log_timestamp1 <= parsedlogs['timestamp'] <= log_timestamp2:
            return parsedlogs
    return None


def process_logs(logs, api_log_entry):
    """
    处理日志，找到最接近API日志条目的日志
    """
    # matched_logs = []
    closest_logs = []
    startingtime = api_log_entry[0]["timestamp"]
    endingtime = api_log_entry[-1]["timestamp"]
    for trace in api_log_entry:
        if (int(trace["status"]) > 199 and int(trace["status"]) < 300) or ("food" in trace["url"].lower()):
            matched_api = match_log_with_api(trace)
            if matched_api:
                matched_logs = matched_api
                # #print("APII",matched_logs)
                desire_logs = desire_log[matched_logs]
                closest_log = find_between_log(desire_logs, startingtime,endingtime)
                if closest_log:
                    # #print('Find')
                    pass
                else:
                    return None
                closest_logs.append(closest_log)
        else:
            return None
    return closest_logs

def find_inconsistent_sequences(seeds_trace):
    inconsistent_sequences = {}
    # #print('the seeds trace is:',seeds_trace)
    for key, sequences in seeds_trace.items():
        seen_types = []
        inconsistent_sequences[key] = []
        for idx, sequence in sequences:
            sequence_types = set(entry.split('<')[1] for entry in sequence)
            if not any(issuperset(seen, sequence_types) for seen in seen_types):
                seen_types.append(sequence_types)
                inconsistent_sequences[key].append([idx, sequence])

    return inconsistent_sequences


def collect_logs(index_logs,sample):
    trace_nums = []
    for index, group in index_logs:
        groups = [i["method"]+"<"+normalize_url(i["url"]) for i in group]
        # #print(groups,"===",sample,issuperset(groups,sample))
        if issuperset(groups,sample):
            trace_nums.append(group)
    return trace_nums    

def parse_log(log_string):
    timestamp_pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}'
    match = re.search(timestamp_pattern, log_string)
    
    if match:
        timestamp_str = match.group(0)
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
        data = {
            'timestamp': timestamp,
            'method': re.search(r'Method:\s*([\S]+)', log_string).group(1) if re.search(r'Method:\s*([\S]+)', log_string) else None,
            'class': re.search(r'Class: ([\w\.]+)', log_string).group(1) if re.search(r'Class: ([\w\.]+)', log_string) else None,
            'arguments': [re.search(r'Arguments: \[(.+?)\],', log_string).group(1)] if re.search(r'Arguments: \[(.+?)\],', log_string) else None,
            'return': re.search(r'Return: (.+)\)', log_string).group(1) if re.search(r'Return: (.+)\)', log_string) else None,
            'url': re.search(r'URL:\s*([\S]+)', log_string).group(1) if re.search(r'URL:\s*([\S]+)', log_string) else None
        }
        return data


def find_relative_logs(traces,API1,API2):
    closest_logs = []
    Log1,Log2 = None,None
    startingtime = traces[0]["timestamp"]
    endingtime = traces[-1]["timestamp"]
    for trace in traces:
        if (int(trace["status"]) > 199 and int(trace["status"]) < 300) or ("food" in trace["url"].lower()):
            matched_api = match_log_with_api(trace)
            if matched_api:
                matched_logs = matched_api
                # #print("APII",matched_logs)
                desire_logs = desire_log[matched_logs]
                closest_log = find_between_log(desire_logs, startingtime,endingtime)
                # #print('log',closest_log,trace,API1,API2)
                if closest_log:
                    if trace["method"]+"<"+normalize_url(trace["url"]) == API1:
                        # #print('Find log1')
                        Log1 = closest_log
                    elif trace["method"]+"<"+normalize_url(trace["url"]) == API2:
                        # #print('Find log2')
                        Log2 = closest_log
                else:
                    return None,None
    return Log1,Log2

def dict_to_string(d):
    return " ".join(f"{key}: {', '.join(map(str, value)) if isinstance(value, list) else value}" for key, value in d.items())

def deploy_dataflow(data):
    pattern = re.compile(r'#([^:]+):\s*(\[.*?\])\s*(\d+\.?\d*)s?')
    pattern_no_time = re.compile(r'#([^:]+):\s*(\[.*?\])')
    pattern_no_key = re.compile(r'#(\[.*?\])\s*(\d+\.?\d*)\s*seconds')
    pattern_composite = re.compile(r'#([^\[\]]+)\s*(\[.*?\])\s*(\d+\.?\d*)')

    # 初始化字典
    result_dict = {}

    # 解析字符串
    for line in data.split('\n'):
        match = pattern.match(line)
        match_no_time = pattern_no_time.match(line)
        match_no_key = pattern_no_key.match(line)
        match_composite = pattern_composite.match(line)
        
        if match:
            key, value, time = match.groups()
            # #print(value.strip())
            result_dict[key.strip()] = {"sequence": ast.literal_eval(value.strip()), "time": float(time)}
        elif match_no_time:
            key, value = match_no_time.groups()
            result_dict[key.strip()] = value.strip()
        elif match_no_key:
            key, time = match_no_key.groups()
            result_dict[key.strip()] = float(time)
        elif match_composite:
            key, value, time = match_composite.groups()
            result_dict[key.strip()] = {"sequence":  ast.literal_eval(value.strip()), "time": float(time)}
    return result_dict

def run_flow_constraint_script(script_path):
    try:
        result = subprocess.run(
            ["python3", script_path],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.split("the code is:")[1].strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.returncode}\n{e.stderr}"

def parse_result(script_path,output):
    with open(script_path, encoding='utf-8') as file:
        code = file.read()
    match = re.search(r'parent_url\s*=\s*"([^"]+)"', code)
    if match:
        parent_url = match.group(1)
    else:
        parent_url = None
    match = re.search(r'child_url1\s*=\s*"([^"]+)"', code)
    if match:
        child_url1 = match.group(1)
    else:
        child_url1 = None
    match = re.search(r'child_url2\s*=\s*"([^"]+)"', code)
    if match:
        child_url2 = match.group(1)
    else:
        child_url2 = None
    print(parent_url,child_url1,child_url2)
    index_a = output.find('def is_branch_a')
    index_b = output.find('def is_branch_b')

    if index_a != -1 and index_b != -1:
        code_a = output[:index_b].strip() 
        code_b = output[:index_a].strip() + "\n" + output[index_b:].strip()         
    else:
        code_a = None
        code_b = None
    extracted_data = {}
    extracted_data[parent_url + " > " + child_url1] = code_a
    extracted_data[parent_url + " > " + child_url2] = code_b
    
    return extracted_data
    
def collect_all_flow_constraints(examples_folder):
    pattern = os.path.join(examples_folder, "flow_constraint*.py")
    flow_constraint_files = glob.glob(pattern)
    
    all_mappings = {}
    
    for script_path in flow_constraint_files:
        script_name = os.path.basename(script_path)
        # print(f"Running script: {script_name}")
        output = run_flow_constraint_script(script_path)
        # print(f"Output from {script_name}:\n{output}\n")
        
        if output.startswith("Error:"):
            all_mappings[script_name] = {"error": output}
            continue
        
        mappings = parse_result(script_path,output)
        
        all_mappings.update(mappings)
    
    return all_mappings

def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="Script to set dataflowFLAG and TriggerflowFLAG.")
    
    parser.add_argument(
        '-d', '--dataflowFLAG', 
        type=bool, 
        default=False, 
        help='Set this to True or False. Warning: Setting this to True may incur high ChatGPT costs.'
    )
    parser.add_argument(
        '-t', '--TriggerflowFLAG', 
        type=bool, 
        default=False, 
        help='Set this to True or False. Warning: Setting this to True may incur high ChatGPT costs.'
    )
    parser.add_argument(
            '-dc', '--dataconstraintFLAG', 
            type=bool, 
            default=False, 
            help='Set this to True or False. Warning: Setting this to True may incur high ChatGPT costs.'
        )
    
    args = parser.parse_args()

    global dataflowFLAG, TriggerflowFLAG, dataconstraintFLAG
    dataflowFLAG = args.dataflowFLAG
    TriggerflowFLAG = args.TriggerflowFLAG
    dataconstraintFLAG = args.dataconstraintFLAG
    
    log_lines = read_log_file(log_file_path)
    tasks = read_task_file(task_file_path)
    
    index_logs = []
    capture = False
    log_group = []
    group_index = 1
    # idx = 0
    
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
        # idx += 1
        index_logs.append(( group_index, log_group))

    group_indices = match_logs_with_tasks(index_logs, tasks)

    for task_name, indices in group_indices.items():
        #print("====")
        #print(f"{task_name}: {indices}")
        pass

    # 执行函数
    result = remove_subsets(group_indices)
    # #print("the res is:",result)
    seeds_trace = {}
    for i,j in result.items():
        seeds_trace[i] = []
        for k in j:
            logset = []
            sequence = []
            # #print("---------",i,k)
            for idx in index_logs[k-1][1]:
                sequence.append(idx)
            sequence = [f"{entry['method']}<{normalize_url(entry['url'])}" for entry in sequence]
            # sequence = normalize_sequence(sequence)
            # sequence = tuple(sequence)
            # #print(f"==322232",sequence)
            for trace in sequence:
                if trace not in logset:
                    logset.append(trace)
            # #print('trace',logset)
            seeds_trace[i].append([k,logset])
    common_sequences = find_inconsistent_sequences(seeds_trace)
    #print("the common seq is:",common_sequences)
    for seeds_name, sequence in common_sequences.items(): 
        if dataflowFLAG:
            start_time = time.time()
            for idx,sample in sequence:
                prompt_logs = []
                dataset = collect_logs(index_logs,sample)
                dataset.append(index_logs[idx-1][1])
                trace_dataset = dataset
                for trace_seq in trace_dataset:
                    cloest_logs = process_logs(log_lines,trace_seq)
                    if len(prompt_logs) < 6 and cloest_logs and cloest_logs not in  prompt_logs:
                        prompt_logs.append(cloest_logs)
                query  = " ".join(sample)
                logs = ""
                for idx,dict_logs in enumerate(prompt_logs):
                    title = "<logset" + str(idx) + ">" + "\n"
                    output = title + "\n\n".join(dict_to_string(d) for d in dict_logs)
                    logs += output
                _,result = checker.check_data_relationship(logs,trace)
                
    
    if dataconstraintFLAG and api_key == "null":
        with open("data_constraint_res.log", "r") as f:
            log_content = f.read()
            print(log_content)
    if dataconstraintFLAG and api_key != "null":
        #TODO: Integrate the dataflow blank 
        pattern = re.compile(r"\'(.*?)\'")
        matches = pattern.findall(dataflow)

        # 去除重复的项
        unique_matches = list(set(matches))
        long_string = ", ".join(unique_matches)

        #print("unique_matches",unique_matches,len(unique_matches))
        # time.sleep(10)
        # data_constrains = {}
        # Calculate the dataconstraint
        lack = []
        for i, disp_match in enumerate(unique_matches):
            # if i >= 10: break
            # if disp_match in skip_elements:
            #     # print(f"Skipping element: {disp_match}")
            #     continue  
            start,end = disp_match.split(">")
            #print("the start and end",start,end)
            start_API,end_API = API_service[start.strip()], API_service[end.strip()]
            #print("the start and end API",start_API,end_API)
            totallog1s = []
            totallog2s = []
            # #print(disp_match)
            if True:
            # if disp_match and (disp_match not in list(data_constrains.keys())) and ("verifycode.service.impl.VerifyCodeServiceImpl.getImageCode" not in disp_match) :
            # if "other.service.OrderOtherServiceImpl.queryOrdersForRefresh" in start.strip() and "inside_payment.service.InsidePaymentServiceImpl.pay" in end.strip():
                if disp_match:
                    try:
                        for seeds_name, sequence in common_sequences.items(): 
                            for idx,seq in sequence:
                                if start_API in seq and end_API in seq:
                                    #print("swq",idx,seq)
                                    logs = index_logs[idx-1]
                                    log1,log2 = find_relative_logs(logs[1],start_API,end_API)
                                    #print(log1,"---",log2)
                                    if "queryOrdersForRefresh" in start and ("pay" in end or "cancel" in end or "consign" in end):
                                        pattern = r'orderId=([a-f0-9\-]+)'
                                        match = re.search(pattern, log2["arguments"][0])
                                        if match:
                                            order_id = match.group(1)
                                            #print(f"Extracted orderId: {order_id}",log1["return"])
                                            if order_id not in log1["return"]:
                                                break
                                    if log1 and log2 and len(totallog1s) < 3:
                                        totallog1s.append(log1)
                                        totallog2s.append(log2)
                        if len(totallog1s) >= 1 and disp_match not in list(data_constrains_logs.keys()):
                            print(22,disp_match)
                            alllogs = []
                            for i in range(len(totallog1s)):
                                alllogs.append(totallog1s[i])
                                alllogs.append(totallog2s[i])
                            logs = ""
                            # #print("alllogs",alllogs)
                            # title = "<logset" + str(idx%2) + ">" + "\n"
                            output = "\n".join(dict_to_string(d) for d in alllogs)
                            # #print('the logs are:',output)
                            class_definition1,class_definition2 = trainticket_class_def[start.strip()]['output'][1],trainticket_class_def[end.strip()]["input"][1]
                            #print("class def1 and def2",class_definition1,class_definition2)
                            entity1,entity2 = trainticket_class_def[start.strip()]['output'][0],trainticket_class_def[end.strip()]["input"][0]
                            #print(alllogs)
                            # time.sleep(30)
                            passed,result = checker.check_input_constraint(class_name1=entity1, class_name2=entity2, class_definition1=class_definition1,
                            class_definition2=class_definition2,logs=[str(log) for log in alllogs])
                            #print(result)
                            if passed:
                                code_string = json.dumps(result, indent=4, ensure_ascii=False)
                                data_constrains[disp_match] = code_string
                        else:
                            if disp_match in list(data_constrains_logs.keys()):
                                print(11,skip_elements,disp_match,11)
                                alllogs = data_constrains_logs[disp_match]
                                # print(alllogs)
                                logs = ""
                                # #print("alllogs",alllogs)
                                # title = "<logset" + str(idx%2) + ">" + "\n"
                                # output = "\n".join(dict_to_string(d) for d in alllogs)
                                # print('the logs are:',output)
                                class_definition1,class_definition2 = trainticket_class_def[start.strip()]['output'][1],trainticket_class_def[end.strip()]["input"][1]
                                # print("class def1 and def2",class_definition1,class_definition2)
                                entity1,entity2 = trainticket_class_def[start.strip()]['output'][0],trainticket_class_def[end.strip()]["input"][0]
                                # print(alllogs)
                                # time.sleep(30)
                                passed,result = checker.check_input_constraint(class_name1=entity1, class_name2=entity2, class_definition1=class_definition1,
                                class_definition2=class_definition2,logs=[str(log) for log in alllogs])
                                print("the res",result)
                                if passed:
                                    code_string = json.dumps(result, indent=4, ensure_ascii=False)
                                    data_constrains[disp_match] = code_string
                                lack.append(disp_match)
                    except Exception as error:
                        print(error)
                        pass
            # #print(data_constrains)
        #     #print(result)
        #     time.sleep(5)
        # end_time = time.time()
        # execution_time = end_time - start_time
        # #print(f"time: {execution_time} sec")
        # #print(len(sequence))
        data_transition = deploy_dataflow(dataflow)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        file_name = f"data_transition_{timestamp}.json"
        with open(file_name, 'w') as file:
            json.dump(data_constrains, file, indent=4)
        # #print("the lack is:",lack,len(lack))
        for element in unique_matches:
            if element not in list(data_constrains.keys()) and element not in lack:
                #print("the element is:",element)
                pass
    #Trigger transition
    if TriggerflowFLAG:
        # for seeds_name, sequence in common_sequences.items(): 
        #     if len(sequence) > 1:
        #         #print("the seq is:",seeds_name,sequence)
        #         if seeds_name in data_transition.keys():
        #             # #print(seeds_name,data_transition[seeds_name]["sequence"])
        #             datatrans = []
        #             for disp_match in data_transition[seeds_name]["sequence"]:
        #                 start,end = disp_match.split(">")
        #                 start_API,end_API = API_service[start.strip()], API_service[end.strip()]
        #                 # #print(start_API,end_API)
        #                 datatrans.append(start_API + " > " + end_API)
        #             #print("the datatrans is:",datatrans)
        #             branch_diffs = {}
        #             diff = None
        #             all_apis_list = []
        #             for i, (id1, branch1) in enumerate(sequence):
        #                 for j, (id2, branch2) in enumerate(sequence):
        #                     if i >= j: 
        #                         continue
        #                     diff = set(branch1).symmetric_difference(set(branch2))
        #                     #print('the diff is:',diff,set(branch1).issubset(set(branch2)),set(branch2).issubset(set(branch1)))
        #                     if set(branch1).issubset(set(branch2)) or set(branch2).issubset(set(branch1)):
        #                         break
        #                     # else:
        #                     if diff:
        #                         branch_diffs[f'branch_{id1}_vs_branch_{id2}'] = list(diff)
        #                         all_apis = set()
        #                         for apis in branch_diffs.values():
        #                             all_apis.update(apis)
        #                         all_apis_list = list(all_apis)
        #             if "POST</api/v1/travel2service/trips/left" in all_apis_list:
        #                 all_apis_list.remove("POST</api/v1/travel2service/trips/left")
        #             #print("Branch Differences:",branch_diffs,all_apis_list)
        #             branch_dataflows = {}
        #             for id, branch in sequence:
        #                 branch_dataflow = [flow for flow in datatrans if any(endpoint in flow for endpoint in branch)]
        #                 break

                    #print("\nBranch Dataflows:")
                    #print(json.dumps(branch_dataflows, indent=4))
        current_dir = os.path.dirname(os.path.abspath(__file__))
        examples_folder = os.path.abspath(os.path.join(current_dir, "../consistency_prompt/examples/"))
        
        all_api_mappings = collect_all_flow_constraints(examples_folder)        
        print("Final API Mappings:")
        for key, value in all_api_mappings.items():
            print(f"{key}:\n {value}")

if __name__ == "__main__":
    main()

['other.service.OrderOtherServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.updateConsignRecord', 'auth.service.impl.TokenServiceImpl.getToken > preserve.service.PreserveServiceImpl.preserve', 'travel2.service.TravelServiceImpl.queryByBatch > preserveOther.service.PreserveOtherServiceImpl.preserve', 'travel2.service.TravelServiceImpl.queryByBatch > preserve.service.PreserveServiceImpl.preserve', 'contacts.service.ContactsServiceImpl.findContactsByAccountId > preserve.service.PreserveServiceImpl.preserve', 'auth.service.impl.TokenServiceImpl.getToken > user.service.impl.UserServiceImpl.getAllUsers', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > travel2.service.TravelServiceImpl.queryByBatch', 'auth.service.impl.TokenServiceImpl.getToken > consign.service.ConsignServiceImpl.queryByAccountId', 'foodsearch.service.FoodServiceImpl.getAllFood > preserve.service.PreserveServiceImpl.preserve', 'inside_payment.service.InsidePaymentServiceImpl.pay > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.queryByOrderId']
['auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'order.service.OrderServiceImpl.queryOrdersForRefresh > cancel.service.CancelServiceImpl.calculateRefund', 'order.service.OrderServiceImpl.queryOrdersForRefresh > inside_payment.service.InsidePaymentServiceImpl.pay', 'auth.service.impl.TokenServiceImpl.getToken > assurance.service.AssuranceServiceImpl.getAllAssuranceTypes', 'order.service.OrderServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.queryByOrderId', 'auth.service.impl.TokenServiceImpl.getToken > contacts.service.ContactsServiceImpl.findContactsByAccountId', 'contacts.service.ContactsServiceImpl.findContactsByAccountId > preserveOther.service.PreserveOtherServiceImpl.preserve', 'auth.service.impl.TokenServiceImpl.getToken > execute.service.ExecuteServiceImpl.ticketCollect', 'inside_payment.service.InsidePaymentServiceImpl.pay > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > rebook.service.RebookServiceImpl.rebook', 'order.service.OrderServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.updateConsignRecord', 'travel.service.TravelServiceImpl.queryByBatch > preserveOther.service.PreserveOtherServiceImpl.preserve', 'verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > cancel.service.CancelServiceImpl.calculateRefund', 'auth.service.impl.TokenServiceImpl.getToken > preserveOther.service.PreserveOtherServiceImpl.preserve', 'travel.service.TravelServiceImpl.queryByBatch > preserve.service.PreserveServiceImpl.preserve', 'auth.service.impl.TokenServiceImpl.getToken > travel.service.TravelServiceImpl.queryByBatch', 'auth.service.impl.TokenServiceImpl.getToken > execute.service.ExecuteServiceImpl.ticketExecute', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > inside_payment.service.InsidePaymentServiceImpl.pay', 'auth.service.impl.TokenServiceImpl.getToken > foodsearch.service.FoodServiceImpl.getAllFood','','']

{'trainticket_search_seeds': [['GET</index.html', 'POST</api/v1/travelservice/trips/left', 'POST</api/v1/travel2service/trips/left']], 'trainticket_cancel_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh', 'GET</api/v1/cancelservice/cancel/refound/', 'GET</api/v1/cancelservice/cancel/'], ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderservice/order/refresh', 'POST</api/v1/orderOtherService/orderOther/refresh', 'GET</api/v1/cancelservice/cancel/refound/']], 'trainticket_getorder_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderservice/order/refresh', 'POST</api/v1/orderOtherService/orderOther/refresh']], 'trainticket_change_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh', 'POST</api/v1/travelservice/trips/left', 'POST</api/v1/travel2service/trips/left', 'POST</api/v1/rebookservice/rebook'], ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh', 'POST</api/v1/travelservice/trips/left', 'POST</api/v1/travel2service/trips/left', 'POST</api/v1/rebookservice/rebook', 'POST</api/v1/rebookservice/updateorder']], 'trainticket_getconsign_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'GET</api/v1/consignservice/consigns/account/']], 'trainticket_getcollect_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh']], 'trainticket_enter_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh', 'GET</api/v1/executeservice/execute/execute/']], 'trainticket_getenter_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh']], 'trainticket_pay_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderservice/order/refresh', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/inside_pay_service/inside_payment'], ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderservice/order/refresh', 'POST</api/v1/orderOtherService/orderOther/refresh']], 'trainticket_consign_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh', 'GET</api/v1/consignservice/consigns/order/', 'PUT</api/v1/consignservice/consigns'], ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh', 'GET</api/v1/consignservice/consigns/order/'], ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderservice/order/refresh', 'POST</api/v1/orderOtherService/orderOther/refresh']], 'trainticket_preserve_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/travel2service/trips/left', 'POST</api/v1/travelservice/trips/left', 'GET</api/v1/assuranceservice/assurances/types', 'GET</api/v1/contactservice/contacts/account/', 'GET</api/v1/foodservice/foods/', 'POST</api/v1/preserveservice/preserve'], ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/travel2service/trips/left', 'POST</api/v1/travelservice/trips/left', 'GET</api/v1/assuranceservice/assurances/types', 'GET</api/v1/contactservice/contacts/account/', 'GET</api/v1/foodservice/foods/'], ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/travelservice/trips/left', 'POST</api/v1/travel2service/trips/left', 'GET</api/v1/assuranceservice/assurances/types', 'GET</api/v1/contactservice/contacts/account/', 'GET</api/v1/foodservice/foods/', 'POST</api/v1/preserveotherservice/preserveOther']], 'trainticket_login_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'GET</api/v1/userservice/users']], 'trainticket_collect_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh', 'GET</api/v1/executeservice/execute/collected/']], 'trainticket_advancedsearch_seeds': [['GET</index.html', 'POST</api/v1/travelplanservice/travelPlan/minStation'], ['GET</index.html', 'POST</api/v1/travelplanservice/travelPlan/cheapest'], ['GET</index.html', 'POST</api/v1/travelplanservice/travelPlan/quickest']]}

# the seq is: trainticket_login_seeds [[26, ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'GET</api/v1/userservice/users']], [3, ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh']]]
# the datatrans is: ['GET</api/v1/verifycode/generate > POST</api/v1/users/login', 'POST</api/v1/users/login > POST</api/v1/orderservice/order/refresh', 'POST</api/v1/users/login > POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/users/login > POST</api/v1/orderservice/order/refresh', 'POST</api/v1/users/login > GET</api/v1/userservice/users']
# the diff is: {'POST</api/v1/orderservice/order/refresh', 'POST</api/v1/orderOtherService/orderOther/refresh', 'GET</api/v1/userservice/users'} False False
# Branch Differences: {'branch_26_vs_branch_3': ['POST</api/v1/orderservice/order/refresh', 'POST</api/v1/orderOtherService/orderOther/refresh', 'GET</api/v1/userservice/users']} ['GET</api/v1/userservice/users', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh']

# Branch Dataflows:
# {}
# the seq is: trainticket_cancel_seeds [[104, ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh', 'GET</api/v1/cancelservice/cancel/refound/', 'GET</api/v1/cancelservice/cancel/']], [1032, ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh', 'GET</api/v1/cancelservice/cancel/refound/']]]
# the datatrans is: ['GET</api/v1/verifycode/generate > POST</api/v1/users/login', 'POST</api/v1/users/login > POST</api/v1/orderservice/order/refresh', 'POST</api/v1/users/login > POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh > GET</api/v1/cancelservice/cancel/refound/', 'POST</api/v1/orderOtherService/orderOther/refresh > GET</api/v1/cancelservice/cancel/refound/']
# the diff is: {'GET</api/v1/cancelservice/cancel/'} False True
# Branch Differences: {} []

# Branch Dataflows:
# {}
# the seq is: trainticket_change_seeds [[4, ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh', 'POST</api/v1/travelservice/trips/left', 'POST</api/v1/travel2service/trips/left', 'POST</api/v1/rebookservice/rebook']], [45, ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh', 'POST</api/v1/travelservice/trips/left', 'POST</api/v1/travel2service/trips/left', 'POST</api/v1/rebookservice/rebook', 'POST</api/v1/rebookservice/updateorder']], [927, ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderservice/order/refresh', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/travelservice/trips/left', 'POST</api/v1/rebookservice/rebook', 'POST</api/v1/rebookservice/rebook/difference', 'POST</api/v1/rebookservice/updateorder']]]
# the datatrans is: ['POST</api/v1/users/login > POST</api/v1/orderservice/order/refresh', 'POST</api/v1/users/login > POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/users/login > POST</api/v1/travelservice/trips/left', 'POST</api/v1/users/login > POST</api/v1/travel2service/trips/left', 'POST</api/v1/users/login > POST</api/v1/rebookservice/rebook', 'POST</api/v1/travelservice/trips/left > POST</api/v1/rebookservice/rebook', 'POST</api/v1/rebookservice/rebook > POST</api/v1/inside_pay_service/inside_payment/difference']
# the diff is: {'POST</api/v1/rebookservice/updateorder'} True False
# the diff is: {'POST</api/v1/travel2service/trips/left', 'POST</api/v1/rebookservice/rebook/difference'} False False
# Branch Differences: {'branch_45_vs_branch_927': ['POST</api/v1/travel2service/trips/left', 'POST</api/v1/rebookservice/rebook/difference']} ['POST</api/v1/rebookservice/rebook/difference']

# Branch Dataflows:
# {}
# the seq is: trainticket_pay_seeds [[17, ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderservice/order/refresh', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/inside_pay_service/inside_payment']], [346, ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderservice/order/refresh', 'POST</api/v1/orderOtherService/orderOther/refresh']]]
# the datatrans is: ['POST</api/v1/users/login > POST</api/v1/orderservice/order/refresh', 'POST</api/v1/users/login > POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh > POST</api/v1/inside_pay_service/inside_payment', 'POST</api/v1/orderOtherService/orderOther/refresh > POST</api/v1/inside_pay_service/inside_payment', 'POST</api/v1/inside_pay_service/inside_payment > POST</api/v1/orderservice/order/refresh', 'POST</api/v1/inside_pay_service/inside_payment > POST</api/v1/orderOtherService/orderOther/refresh']
# the diff is: {'POST</api/v1/inside_pay_service/inside_payment'} False True
# Branch Differences: {} []

# Branch Dataflows:
# {}
# the seq is: trainticket_consign_seeds [[18, ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh', 'GET</api/v1/consignservice/consigns/order/', 'PUT</api/v1/consignservice/consigns']], [82, ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh', 'GET</api/v1/consignservice/consigns/order/']], [346, ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderservice/order/refresh', 'POST</api/v1/orderOtherService/orderOther/refresh']]]
# the datatrans is: ['POST</api/v1/users/login > POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/users/login > POST</api/v1/orderservice/order/refresh', 'POST</api/v1/orderOtherService/orderOther/refresh > GET</api/v1/consignservice/consigns/order/', 'POST</api/v1/orderservice/order/refresh > GET</api/v1/consignservice/consigns/order/']
# the diff is: {'PUT</api/v1/consignservice/consigns'} False True
# the diff is: {'GET</api/v1/consignservice/consigns/order/'} False True
# Branch Differences: {} []

# Branch Dataflows:
# {}
# the seq is: trainticket_advancedsearch_seeds [[97, ['GET</index.html', 'POST</api/v1/travelplanservice/travelPlan/minStation']], [36, ['GET</index.html', 'POST</api/v1/travelplanservice/travelPlan/cheapest']], [47, ['GET</index.html', 'POST</api/v1/travelplanservice/travelPlan/quickest']]]
# the datatrans is: []
# the diff is: {'POST</api/v1/travelplanservice/travelPlan/cheapest', 'POST</api/v1/travelplanservice/travelPlan/minStation'} False False
# the diff is: {'POST</api/v1/travelplanservice/travelPlan/minStation', 'POST</api/v1/travelplanservice/travelPlan/quickest'} False False
# the diff is: {'POST</api/v1/travelplanservice/travelPlan/cheapest', 'POST</api/v1/travelplanservice/travelPlan/quickest'} False False
# Branch Differences: {'branch_97_vs_branch_36': ['POST</api/v1/travelplanservice/travelPlan/cheapest', 'POST</api/v1/travelplanservice/travelPlan/minStation'], 'branch_97_vs_branch_47': ['POST</api/v1/travelplanservice/travelPlan/minStation', 'POST</api/v1/travelplanservice/travelPlan/quickest'], 'branch_36_vs_branch_47': ['POST</api/v1/travelplanservice/travelPlan/cheapest', 'POST</api/v1/travelplanservice/travelPlan/quickest']} ['POST</api/v1/travelplanservice/travelPlan/cheapest', 'POST</api/v1/travelplanservice/travelPlan/minStation', 'POST</api/v1/travelplanservice/travelPlan/quickest']

# Branch Dataflows:
# {}
# the seq is: trainticket_preserve_seeds [[331, ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/travel2service/trips/left', 'POST</api/v1/travelservice/trips/left', 'GET</api/v1/assuranceservice/assurances/types', 'GET</api/v1/contactservice/contacts/account/', 'GET</api/v1/foodservice/foods/', 'POST</api/v1/preserveservice/preserve']], [372, ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/travelservice/trips/left', 'POST</api/v1/travel2service/trips/left', 'GET</api/v1/assuranceservice/assurances/types', 'GET</api/v1/contactservice/contacts/account/', 'GET</api/v1/foodservice/foods/', 'POST</api/v1/preserveotherservice/preserveOther']]]
# the datatrans is: ['GET</api/v1/verifycode/generate > POST</api/v1/users/login', 'POST</api/v1/users/login > GET</api/v1/assuranceservice/assurances/types', 'POST</api/v1/users/login > GET</api/v1/contactservice/contacts/account/', 'POST</api/v1/users/login > GET</api/v1/foodservice/foods/', 'POST</api/v1/users/login > POST</api/v1/preserveotherservice/preserveOther', 'GET</api/v1/contactservice/contacts/account/ > POST</api/v1/preserveotherservice/preserveOther', 'POST</api/v1/travelservice/trips/left > POST</api/v1/preserveotherservice/preserveOther', 'POST</api/v1/travel2service/trips/left > POST</api/v1/preserveotherservice/preserveOther', 'GET</api/v1/contactservice/contacts/account/ > POST</api/v1/preserveservice/preserve', 'GET</api/v1/foodservice/foods/ > POST</api/v1/preserveservice/preserve', 'POST</api/v1/travel2service/trips/left > POST</api/v1/preserveservice/preserve', 'POST</api/v1/users/login > POST</api/v1/preserveservice/preserve', 'POST</api/v1/travelservice/trips/left > POST</api/v1/preserveservice/preserve']
# the diff is: {'POST</api/v1/preserveservice/preserve', 'POST</api/v1/preserveotherservice/preserveOther'} False False
# Branch Differences: {'branch_331_vs_branch_372': ['POST</api/v1/preserveservice/preserve', 'POST</api/v1/preserveotherservice/preserveOther']} ['POST</api/v1/preserveotherservice/preserveOther', 'POST</api/v1/preserveservice/preserve']