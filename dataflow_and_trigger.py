import re
import json
from collections import defaultdict,deque
import time
from datetime import datetime
import sys
sys.path.append("consistency_prompt/")
import consistency_prompt.data_relationship
from gptchecker import GPTChecker

dataflow = """
#login_seeds: [] 52s
# cancel_seeds: ['verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'order.service.OrderServiceImpl.queryOrdersForRefresh > cancel.service.CancelServiceImpl.calculateRefund', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > cancel.service.CancelServiceImpl.calculateRefund'] 9.6909s
#['auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh'] 19.0419 seconds
# Change ['auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > travel.service.TravelServiceImpl.queryByBatch', 'auth.service.impl.TokenServiceImpl.getToken > travel2.service.TravelServiceImpl.queryByBatch', 'auth.service.impl.TokenServiceImpl.getToken > rebook.service.RebookServiceImpl.rebook', 'travel.service.TravelServiceImpl.queryByBatch > rebook.service.RebookServiceImpl.rebook','rebook.service.RebookServiceImpl.rebook > inside_payment.service.InsidePaymentServiceImpl.payDifference'] 20.95
#getConsign['auth.service.impl.TokenServiceImpl.getToken > consign.service.ConsignServiceImpl.queryByAccountId'] 11.62
#getCollect['verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh'] 13.8993
#Enter['auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > execute.service.ExecuteServiceImpl.ticketExecute', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > execute.service.ExecuteServiceImpl.ticketExecute','order.service.OrderServiceImpl.queryOrdersForRefresh > execute.service.ExecuteServiceImpl.ticketExecute', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > execute.service.ExecuteServiceImpl.ticketExecute'] 15.6334
#getEnter['verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh'] 17.6727
#Payseeds ['auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'order.service.OrderServiceImpl.queryOrdersForRefresh > inside_payment.service.InsidePaymentServiceImpl.pay', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > inside_payment.service.InsidePaymentServiceImpl.pay', 'inside_payment.service.InsidePaymentServiceImpl.pay > order.service.OrderServiceImpl.queryOrdersForRefresh', 'inside_payment.service.InsidePaymentServiceImpl.pay > other.service.OrderOtherServiceImpl.queryOrdersForRefresh'] 29.5432s
# Consign ['auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.queryByOrderId', 'order.service.OrderServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.queryByOrderId'] 12.95 ['verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh'] 16.577 ['auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'order.service.OrderServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.queryByOrderId', 'order.service.OrderServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.updateConsignRecord', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.queryByOrderId', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.updateConsignRecord'] 22.2460
# Preserve ['verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken', 'auth.service.impl.TokenServiceImpl.getToken > assurance.service.AssuranceServiceImpl.getAllAssuranceTypes', 'auth.service.impl.TokenServiceImpl.getToken > contacts.service.ContactsServiceImpl.findContactsByAccountId', 'auth.service.impl.TokenServiceImpl.getToken > foodsearch.service.FoodServiceImpl.getAllFood', 'auth.service.impl.TokenServiceImpl.getToken > preserveOther.service.PreserveOtherServiceImpl.preserve', 'contacts.service.ContactsServiceImpl.findContactsByAccountId > preserveOther.service.PreserveOtherServiceImpl.preserve', 'travel.service.TravelServiceImpl.queryByBatch > preserveOther.service.PreserveOtherServiceImpl.preserve', 'travel2.service.TravelServiceImpl.queryByBatch > preserveOther.service.PreserveOtherServiceImpl.preserve',,'contacts.service.ContactsServiceImpl.findContactsByAccountId > preserve.service.PreserveServiceImpl.preserve', 'foodsearch.service.FoodServiceImpl.getAllFood > preserve.service.PreserveServiceImpl.preserve','travel2.service.TravelServiceImpl.queryByBatch > preserve.service.PreserveServiceImpl.preserve','auth.service.impl.TokenServiceImpl.getToken > preserve.service.PreserveServiceImpl.preserve','travel.service.TravelServiceImpl.queryByBatch > preserve.service.PreserveServiceImpl.preserve'] 16s
#Login ['verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh']  ['verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken', 'auth.service.impl.TokenServiceImpl.getToken > user.service.impl.UserServiceImpl.getAllUsers'] 10.7168
#Collect ['auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > execute.service.ExecuteServiceImpl.ticketCollect', 'auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'order.service.OrderServiceImpl.queryOrdersForRefresh > execute.service.ExecuteServiceImpl.ticketCollect', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > execute.service.ExecuteServiceImpl.ticketCollect'] 28.3366
#Adsearch [] 6.99,29.64,11.0810
#
"""

# 提取所有关系的正则表达式
import re



# 定义日志的正则表达式模式
log_pattern = re.compile(
    r'(?P<ip>[\d\.]+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<url>[^\s]+) (?P<protocol>[^\"]+)" (?P<status>\d+) (?P<size>\d+) "(?P<referer>[^\"]*)" "[^\"]*"'
)
checker = GPTChecker(
    api_key="sk-proj-enNNZd2GZEkaDuRa3rPfT3BlbkFJph7uEdwchQlAXWY5gm2G",
    model="gpt-4o",
    max_tokens=2048,
    top_p=0.9,
    temperature=0.0
)
# 文件路径
log_file_path = "/home/yifannus2023/TamperLogPrompt/Train_data_modify.txt"
task_file_path = "/home/yifannus2023/TamperLogPrompt/pre_defined_task.json"
API_service_path = "/home/yifannus2023/TamperLogPrompt/API_service.json"
with open("openAPI.json") as fp:
    OPENAPI = json.load(fp)
    
with open("log_target.json") as fp:
    desire_log = json.load(fp)
    
with open("API_service.json") as fp:
    API_service = json.load(fp)

with open('trainticket_class_def.json') as fp:
    trainticket_class_def = json.load(fp)

with open('data_constrains.json') as fp:
    data_constrains = json.load(fp)

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
    print("fjkaf",len(group_logs),group_logs[-1],len(expanded_seed_logs),expanded_seed_logs)
    if len(group_logs) >= len(expanded_seed_logs) and ("foodservice" not in group_logs[-1][0]) and ("contact" not in group_logs[-1][0] ):
        for api in group_logs:
            FLAG = False
            print("new",api)
                
            for expanded_seed_l in expanded_seed_logs:
                # print(expanded_seed_l)
                if len(expanded_seed_l[0]) == 1:
                    # print("4331",api, expanded_seed_l[0],expanded_seed_l[1])
                    if expanded_seed_l[0][0] in api[0] and expanded_seed_l[1] in api[1]:
                        FLAG = True
                        break
                else:
                    # print("433",api, expanded_seed_l[0],expanded_seed_l[1])
                    for seed_log in expanded_seed_l[0]:
                        if type(expanded_seed_l[1]) == str:
                            if seed_log in api[0] and expanded_seed_l[1] in api[1]:
                                FLAG = True
                                break
                        else:
                            print("login",seed_log,expanded_seed_l[1])
                            for path in expanded_seed_l[1]:
                                if seed_log in api[0] and path in api[1]:
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
    # print("e4343",expanded_seed_logs)
    # time.sleep(3)
    for index, group in index_logs:
        # if index in {331, 372, 37}:
            # print(index,group)
            for task_name, seeds in tasks.items():
                if "trainticket_change_seeds" in task_name:
                    # print('login seeds',seeds)
                    FLAG = check_group_with_seeds(expanded_seed_logs[task_name],group)
                    if FLAG:
                        # time.sleep(5)
                        sequence = [f"{entry['method']}<{normalize_url(entry['url'])}" for entry in group]
                        sequence = normalize_sequence(sequence)
                        sequence = tuple(sequence)
                        # print("the seq is:",index,sequence)
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
    # print(keys)
    for i in range(len(keys)):
        # print(keys[i])
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
    # print("eee",seqA,seqB)
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
    method_url = f"{log_entry['method']} {log_entry['url']}"
    for api_name, api_url in OPENAPI.items():
        if api_url.lower() in method_url.lower():
            return api_name
    return None

def convert_to_datetime(timestamp_str):
    # 拆分日期和时间部分
    date_str, rest = timestamp_str.split(':', 1)
    time_str, tz_and_microseconds = rest.split(' ', 1)
    # print(tz_and_microseconds.split('.'))
    tz_str, _,microseconds_str = tz_and_microseconds.split('.')
    
    # 获取微秒部分的最后三位数字
    microseconds = int(microseconds_str[-3:]) * 1000
    
    # 合并日期和时间部分，并解析时区
    datetime_part = datetime.strptime(date_str + ':' + time_str, "%d/%b/%Y:%H:%M:%S")
    
    # 将微秒部分添加到datetime对象
    final_datetime = datetime_part.replace(microsecond=microseconds)
    # print(final_datetime)
    return final_datetime

def find_between_log(logs, startingtime,endingtime):
    """
    找到与目标时间戳最接近的日志条目
    """
    print("tsjtkgjf",startingtime,endingtime)
    closest_log = None
    smallest_diff = float('inf')
    for log in logs:
        parsedlogs = parse_log(log)
        if parsedlogs:
            log_timestamp1 = convert_to_datetime(startingtime)
            log_timestamp2 = convert_to_datetime(endingtime)
            # if "preserveOther.service.PreserveOtherServiceImpl" in parsedlogs["class"]: print(parsedlogs["timestamp"],"==",log_timestamp1,log_timestamp2)
            if (parsedlogs['timestamp'] - log_timestamp1).total_seconds() >= 0 and (parsedlogs['timestamp'] - log_timestamp2).total_seconds() <= 0:
                closest_log = parsedlogs
                break
    return closest_log

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
                print("APII",matched_logs)
                desire_logs = desire_log[matched_logs]
                closest_log = find_between_log(desire_logs, startingtime,endingtime)
                if closest_log:
                    print('Find')
                else:
                    return None
                closest_logs.append(closest_log)
        else:
            return None
    return closest_logs

def find_inconsistent_sequences(seeds_trace):
    inconsistent_sequences = {}

    for key, sequences in seeds_trace.items():
        seen_types = []
        if key not in inconsistent_sequences:
            inconsistent_sequences[key] = []
        print(sequences)
        for seq in sequences:
            idx, sequence = seq
            sequence_types = set(entry.split('<')[1] for entry in sequence)
            if not seen_types:
                seen_types.append(sequence_types)
                inconsistent_sequences[key].append([idx,sequence])
            else:
                is_unique = True
                for seen in seen_types:
                    # print('jfks',seen,sequence_types,issuperset(seen,sequence_types))
                    if issuperset(seen,sequence_types):
                        is_unique = False
                        break
                if is_unique:
                    # print('add',sequence_types,seen_types)
                    seen_types.append(sequence_types)    
                    inconsistent_sequences[key].append([idx,sequence])                

    return inconsistent_sequences

def collect_logs(index_logs,sample):
    trace_nums = []
    for index, group in index_logs:
        groups = [i["method"]+"<"+normalize_url(i["url"]) for i in group]
        # print(groups,"===",sample,issuperset(groups,sample))
        if issuperset(groups,sample):
            trace_nums.append(group)
    return trace_nums    

def parse_log(log_string):
    # print(log_string)
    timestamp_pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}'

    # 检查 log_string 是否包含符合正则表达式的时间戳
    match = re.search(timestamp_pattern, log_string)

    if match:
        timestamp_str = match.group(0)
        # print(f"Found timestamp: {timestamp_str}")
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
        # print(log_string)
        if "Entering in Method:" in log_string:
            method_name = re.search(r'Entering in Method: (\w+)', log_string).group(1)

            # 提取类名
            class_name = re.search(r'Class: ([\w\.]+)', log_string).group(1)

            # 提取参数
            arguments_match = re.search(r'Arguments: \[(.+?)\],', log_string)
            if arguments_match:
                arguments_str = arguments_match.group(1)
            else:
                arguments_str = None

            # 提取返回值
            return_match = re.search(r'Return: (.+)\)', log_string)
            if return_match:
                return_str = return_match.group(1)
            else:
                return_str = None

            # 提取URL
            url_match = re.search(r'URL:\s*([\S]+)', log_string)
            if url_match:
                url_str = url_match.group(1)
            else:
                url_str = None

            # 提取方法
            method_match = re.search(r'Method:\s*([\S]+)', log_string)
            if method_match:
                method_str = method_match.group(1)
            else:
                method_str = None

            return {
                'timestamp': timestamp,
                'method': method_str,
                'class': class_name,
                'arguments': [arguments_str],
                'return': return_str
            }
        # elif "Execution of repository method" in log_string:
        #     method_name = re.search(r'Execution of repository method: (\w+)', log_string).group(1)

        #     # 提取参数
        #     arguments_match = re.search(r'Arguments: \[(.+?)\],', log_string)
        #     if arguments_match:
        #         arguments_str = arguments_match.group(1)
        #     else:
        #         arguments_str = None

        #     # 提取返回值
        #     return_match = re.search(r'Result: (.+)\)', log_string)
        #     if return_match:
        #         return_str = return_match.group(1)
        #     else:
        #         return_str = None

        #     # 提取方法
        #     method_match = re.search(r'method:\s*([\S]+)', log_string)
        #     if method_match:
        #         method_str = method_match.group(1)
        #     else:
        #         method_str = None

        #     return {
        #         'timestamp': timestamp,
        #         'method': method_str,
        #         'arguments': [None],
        #         'return': return_str
        #     }

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
                print("APII",matched_logs)
                desire_logs = desire_log[matched_logs]
                closest_log = find_between_log(desire_logs, startingtime,endingtime)
                print('log',closest_log,trace,API1,API2)
                if closest_log:
                    if trace["method"]+"<"+normalize_url(trace["url"]) == API1:
                        print('Find log1')
                        Log1 = closest_log
                    elif trace["method"]+"<"+normalize_url(trace["url"]) == API2:
                        print('Find log2')
                        Log2 = closest_log
                else:
                    return None,None
    return Log1,Log2

def dict_to_string(d):
    result = []
    for key, value in d.items():
        if isinstance(value, list):
            value = ', '.join(map(str, value))
            result.append(f"{key}: {value}")
                
        # if "timestamp" not in key:
        #     result.append(f"{key}: {value}")
    return " ".join(result)



def main():
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
        print("====")
        print(f"{task_name}: {indices}")

    # 执行函数
    result = remove_subsets(group_indices)
    print("the res is:",result)
    seeds_trace = {}
    for i,j in result.items():
        seeds_trace[i] = []
        for k in j:
            logset = []
            sequence = []
            print("---------",i,k)
            for idx in index_logs[k-1][1]:
                sequence.append(idx)
            sequence = [f"{entry['method']}<{normalize_url(entry['url'])}" for entry in sequence]
            # sequence = normalize_sequence(sequence)
            # sequence = tuple(sequence)
            print(f"==322232",sequence)
            for trace in sequence:
                if trace not in logset:
                    logset.append(trace)
            print('trace',logset)
            seeds_trace[i].append([k,logset])
    common_sequences = find_inconsistent_sequences(seeds_trace)
    print(common_sequences)
    # for seeds_name, sequence in common_sequences.items(): 
    #     if "trainticket_preserve_seeds" in seeds_name:
    #         start_time = time.time()
    #         for idx,sample in sequence:
    #             # if "PUT</api/v1/consignservice/consigns" in sample:
    #             prompt_logs = []
    #             dataset = collect_logs(index_logs,sample)
    #             dataset.append(index_logs[idx-1][1])
    #             trace_dataset = dataset
    #             # print('trace_dataset',dataset,"--",index_logs[idx-1][1])
    #             # time.sleep(2)
    #             for trace_seq in trace_dataset:
    #                 print('trace',trace_seq)
    #                 # time.sleep(5)
    #                 cloest_logs = process_logs(log_lines,trace_seq)
    #                 if len(prompt_logs) < 6 and cloest_logs and cloest_logs not in  prompt_logs:
    #                     prompt_logs.append(cloest_logs)
    #             print(sample,prompt_logs)
    #             query  = " ".join(sample)
    #             logs = ""
    #             for idx,dict_logs in enumerate(prompt_logs):
    #                 title = "<logset" + str(idx) + ">" + "\n"
    #                 output = title + "\n\n".join(dict_to_string(d) for d in dict_logs)
    #                 logs += output
    #             print(query,logs)
    #             _,result = checker.check_data_relationship(logs,trace)
    #             print(result)
    #             time.sleep(5)
    #         end_time = time.time()
    #         execution_time = end_time - start_time
    #         print(f"time: {execution_time} sec")
    #         print(len(sequence))
            # if len(sequence) > 1:
                # pass TODO:Integrate the trigger condition
    pattern = re.compile(r"\'(.*?)\'")
    matches = pattern.findall(dataflow)

    # 去除重复的项
    unique_matches = list(set(matches))
    long_string = ", ".join(unique_matches)

    print("unique_matches",unique_matches,len(unique_matches))
    # time.sleep(432)
    for i, disp_match in enumerate(unique_matches):
        # if i >= 10: break
        start,end = disp_match.split(">")
        print("the start and end",start,end)
        start_API,end_API = API_service[start.strip()], API_service[end.strip()]
        print("the start and end API",start_API,end_API)
        totallog1s = []
        totallog2s = []
        # print(disp_match)
        # if "order.service.OrderServiceImpl.queryOrdersForRefresh" in start.strip() and "consign.service.ConsignServiceImpl.queryByOrderId" in end.strip():
        if disp_match in ["auth.service.impl.TokenServiceImpl.getToken > execute.service.ExecuteServiceImpl.ticketExecute"]:
            try:
                for seeds_name, sequence in common_sequences.items(): 
                    for idx,seq in sequence:
                        if start_API in seq and end_API in seq:
                            print("swq",idx,seq)
                            logs = index_logs[idx-1]
                            log1,log2 = find_relative_logs(logs[1],start_API,end_API)
                            print(log1,"---",log2)
                            if "queryOrdersForRefresh" in start and ("pay" in end or "cancel" in end or "consign" in end):
                                pattern = r'orderId=([a-f0-9\-]+)'
                                match = re.search(pattern, log2["arguments"][0])
                                if match:
                                    order_id = match.group(1)
                                    print(f"Extracted orderId: {order_id}",log1["return"])
                                    if order_id not in log1["return"]:
                                        break
                            if log1 and log2 and len(totallog1s) < 3:
                                totallog1s.append(log1)
                                totallog2s.append(log2)
                if len(totallog1s) >= 1:
                    alllogs = []
                    for i in range(len(totallog1s)):
                        alllogs.append(totallog1s[i])
                        alllogs.append(totallog2s[i])
                    logs = ""
                    # print("alllogs",alllogs)
                    # title = "<logset" + str(idx%2) + ">" + "\n"
                    output = "\n".join(dict_to_string(d) for d in alllogs)
                    # print('the logs are:',output)
                    class_definition1,class_definition2 = trainticket_class_def[start.strip()]['output'][1],trainticket_class_def[end.strip()]["input"][1]
                    print("class def1 and def2",class_definition1,class_definition2)
                    entity1,entity2 = trainticket_class_def[start.strip()]['output'][0],trainticket_class_def[end.strip()]["input"][0]
                    print(alllogs)
                    time.sleep(30)
                    _,result = checker.check_input_constraint(class_name1=entity1, class_name2=entity2, class_definition1=class_definition1,
                    class_definition2=class_definition2,logs=[str(log) for log in alllogs])
                    print(result)
                    code_string = json.dumps(result, indent=4, ensure_ascii=False)
                    data_constrains[disp_match] = code_string
            except:
                pass
    print(data_constrains)
    # with open('data_constrains.json', 'w') as f:
    #     json.dump(data_constrains, f, indent=4)
if __name__ == "__main__":
    main()

['other.service.OrderOtherServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.updateConsignRecord', 'auth.service.impl.TokenServiceImpl.getToken > preserve.service.PreserveServiceImpl.preserve', 'travel2.service.TravelServiceImpl.queryByBatch > preserveOther.service.PreserveOtherServiceImpl.preserve', 'travel2.service.TravelServiceImpl.queryByBatch > preserve.service.PreserveServiceImpl.preserve', 'contacts.service.ContactsServiceImpl.findContactsByAccountId > preserve.service.PreserveServiceImpl.preserve', 'auth.service.impl.TokenServiceImpl.getToken > user.service.impl.UserServiceImpl.getAllUsers', 'auth.service.impl.TokenServiceImpl.getToken > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > travel2.service.TravelServiceImpl.queryByBatch', 'auth.service.impl.TokenServiceImpl.getToken > consign.service.ConsignServiceImpl.queryByAccountId', 'foodsearch.service.FoodServiceImpl.getAllFood > preserve.service.PreserveServiceImpl.preserve', 'inside_payment.service.InsidePaymentServiceImpl.pay > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.queryByOrderId']
['auth.service.impl.TokenServiceImpl.getToken > other.service.OrderOtherServiceImpl.queryOrdersForRefresh', 'order.service.OrderServiceImpl.queryOrdersForRefresh > cancel.service.CancelServiceImpl.calculateRefund', 'order.service.OrderServiceImpl.queryOrdersForRefresh > inside_payment.service.InsidePaymentServiceImpl.pay', 'auth.service.impl.TokenServiceImpl.getToken > assurance.service.AssuranceServiceImpl.getAllAssuranceTypes', 'order.service.OrderServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.queryByOrderId', 'auth.service.impl.TokenServiceImpl.getToken > contacts.service.ContactsServiceImpl.findContactsByAccountId', 'contacts.service.ContactsServiceImpl.findContactsByAccountId > preserveOther.service.PreserveOtherServiceImpl.preserve', 'auth.service.impl.TokenServiceImpl.getToken > execute.service.ExecuteServiceImpl.ticketCollect', 'inside_payment.service.InsidePaymentServiceImpl.pay > order.service.OrderServiceImpl.queryOrdersForRefresh', 'auth.service.impl.TokenServiceImpl.getToken > rebook.service.RebookServiceImpl.rebook', 'order.service.OrderServiceImpl.queryOrdersForRefresh > consign.service.ConsignServiceImpl.updateConsignRecord', 'travel.service.TravelServiceImpl.queryByBatch > preserveOther.service.PreserveOtherServiceImpl.preserve', 'verifycode.service.impl.VerifyCodeServiceImpl.getImageCode > auth.service.impl.TokenServiceImpl.getToken', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > cancel.service.CancelServiceImpl.calculateRefund', 'auth.service.impl.TokenServiceImpl.getToken > preserveOther.service.PreserveOtherServiceImpl.preserve', 'travel.service.TravelServiceImpl.queryByBatch > preserve.service.PreserveServiceImpl.preserve', 'auth.service.impl.TokenServiceImpl.getToken > travel.service.TravelServiceImpl.queryByBatch', 'auth.service.impl.TokenServiceImpl.getToken > execute.service.ExecuteServiceImpl.ticketExecute', 'other.service.OrderOtherServiceImpl.queryOrdersForRefresh > inside_payment.service.InsidePaymentServiceImpl.pay', 'auth.service.impl.TokenServiceImpl.getToken > foodsearch.service.FoodServiceImpl.getAllFood','','']

{'trainticket_search_seeds': [['GET</index.html', 'POST</api/v1/travelservice/trips/left', 'POST</api/v1/travel2service/trips/left']], 'trainticket_cancel_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh', 'GET</api/v1/cancelservice/cancel/refound/', 'GET</api/v1/cancelservice/cancel/'], ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderservice/order/refresh', 'POST</api/v1/orderOtherService/orderOther/refresh', 'GET</api/v1/cancelservice/cancel/refound/']], 'trainticket_getorder_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderservice/order/refresh', 'POST</api/v1/orderOtherService/orderOther/refresh']], 'trainticket_change_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh', 'POST</api/v1/travelservice/trips/left', 'POST</api/v1/travel2service/trips/left', 'POST</api/v1/rebookservice/rebook'], ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh', 'POST</api/v1/travelservice/trips/left', 'POST</api/v1/travel2service/trips/left', 'POST</api/v1/rebookservice/rebook', 'POST</api/v1/rebookservice/updateorder']], 'trainticket_getconsign_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'GET</api/v1/consignservice/consigns/account/']], 'trainticket_getcollect_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh']], 'trainticket_enter_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh', 'GET</api/v1/executeservice/execute/execute/']], 'trainticket_getenter_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh']], 'trainticket_pay_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderservice/order/refresh', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/inside_pay_service/inside_payment'], ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderservice/order/refresh', 'POST</api/v1/orderOtherService/orderOther/refresh']], 'trainticket_consign_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh', 'GET</api/v1/consignservice/consigns/order/', 'PUT</api/v1/consignservice/consigns'], ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh', 'GET</api/v1/consignservice/consigns/order/'], ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderservice/order/refresh', 'POST</api/v1/orderOtherService/orderOther/refresh']], 'trainticket_preserve_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/travel2service/trips/left', 'POST</api/v1/travelservice/trips/left', 'GET</api/v1/assuranceservice/assurances/types', 'GET</api/v1/contactservice/contacts/account/', 'GET</api/v1/foodservice/foods/', 'POST</api/v1/preserveservice/preserve'], ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/travel2service/trips/left', 'POST</api/v1/travelservice/trips/left', 'GET</api/v1/assuranceservice/assurances/types', 'GET</api/v1/contactservice/contacts/account/', 'GET</api/v1/foodservice/foods/'], ['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/travelservice/trips/left', 'POST</api/v1/travel2service/trips/left', 'GET</api/v1/assuranceservice/assurances/types', 'GET</api/v1/contactservice/contacts/account/', 'GET</api/v1/foodservice/foods/', 'POST</api/v1/preserveotherservice/preserveOther']], 'trainticket_login_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'GET</api/v1/userservice/users']], 'trainticket_collect_seeds': [['GET</index.html', 'GET</api/v1/verifycode/generate', 'POST</api/v1/users/login', 'POST</api/v1/orderOtherService/orderOther/refresh', 'POST</api/v1/orderservice/order/refresh', 'GET</api/v1/executeservice/execute/collected/']], 'trainticket_advancedsearch_seeds': [['GET</index.html', 'POST</api/v1/travelplanservice/travelPlan/minStation'], ['GET</index.html', 'POST</api/v1/travelplanservice/travelPlan/cheapest'], ['GET</index.html', 'POST</api/v1/travelplanservice/travelPlan/quickest']]}
