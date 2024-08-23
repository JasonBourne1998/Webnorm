import json
import re
from consistency_prompt.gptchecker.tester import Tester
import multiprocessing
import time
from collections import defaultdict

class_method_pattern = re.compile(r'Entering in Method: (\w+), Class: ([\w\.]+)')
code_cache = {}

def read_txt_file(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    return lines

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def main(logs, trainticket_class, data_constraints, commonsense_constraints, trigger_constraints, start_idx, end_idx):
    # 获取切片日志
    log_slice = logs[start_idx:end_idx]
    
    for log in log_slice:
        method_name, class_name = extract_class_method(log)
        if method_name and class_name and "gettoken" not in method_name.lower():
            # 构建 commonsense key
            commonsense_key = f"{class_name}.{method_name}"
            if commonsense_key in commonsense_constraints:
                # 使用缓存来减少 exec 执行
                if commonsense_key not in code_cache:
                    code_str = commonsense_constraints[commonsense_key]
                    exec_namespace = {}
                    try:
                        exec(code_str, exec_namespace)
                        assert 'is_valid' in exec_namespace
                        code_cache[commonsense_key] = exec_namespace['is_valid']
                    except Exception as e:
                        print("---error---")
                        print(str(e), "\n", code_str)
                        continue  # 跳过此错误的log处理
                is_valid = code_cache[commonsense_key]
                classname = trainticket_class[commonsense_key]["input"][0]
                result = Tester.test_commonsense_contraint([log], classname, is_valid)
            
            # 数据流约束检查
            for dataflow, constraint in data_constraints.items():
                pre, follow = map(str.strip, dataflow.split(">"))
                if commonsense_key in follow:
                    if dataflow not in code_cache:
                        code_str = data_constraints[dataflow]
                        exec_namespace = {}
                        try:
                            exec(code_str, exec_namespace)
                            assert 'is_related' in exec_namespace
                            code_cache[dataflow] = exec_namespace['is_related']
                        except Exception as e:
                            print("---error---")
                            print(str(e), "\n", code_str)
                            continue
                    is_related = code_cache[dataflow]
                    pre_classname = trainticket_class[pre]["output"][0]
                    after_classname = trainticket_class[follow]["input"][0]
                    pre_log, pre_class_name, pre_method_name = find_last_log(log, pre, logs)
                    if pre_method_name:
                        logset = pre_log + [log]
                        if not ("queryByBatch" in pre_method_name and "preserve" in method_name):
                            result = Tester.test_input_constraint(logset, pre_classname, after_classname, is_related)

            # 触发约束检查
            for triggerflow, constraint in trigger_constraints.items():
                pre, follow = map(str.strip, triggerflow.split(">"))
                if commonsense_key in follow:
                    if triggerflow not in code_cache:
                        code_str = trigger_constraints[triggerflow]
                        exec_namespace = {}
                        try:
                            exec(code_str, exec_namespace)
                            assert 'is_branch_a' in exec_namespace
                            code_cache[triggerflow] = exec_namespace['is_branch_a']
                        except Exception as e:
                            print("---error---")
                            print(str(e), "\n", code_str)
                            continue
                    is_branch_a = code_cache[triggerflow]
                    if pre != "findByUsername":
                        pre_classname = trainticket_class[pre]["output"][0]
                        after_classname = trainticket_class[follow]["input"][0]
                        pre_log, pre_class_name, pre_method_name = find_last_log(log, pre, logs)
                    else:
                        pre_log, pre_class_name, pre_method_name = find_last_log(log, "findByUsername", logs)
                    if pre_method_name:
                        logset = pre_log + [log]
                        if not ("queryByBatch" in pre_method_name and "preserve" in method_name):
                            result = Tester.test_flow_constraint(logset, [True], is_branch_a)  
                    
def extract_class_method(line):
    method_name,class_name = None,None
    match = class_method_pattern.search(line)
    if match:
        method_name = match.group(1)
        class_name = match.group(2)
    return method_name,class_name

def find_last_log(after_log,pre_classname,logs):
    # logs = read_txt_file(txt_file_path)
    idx = logs.index(after_log)
    if pre_classname in "findByUsername":
        for i in range(idx,0,-1):
            log = logs[i]
            if "Execution of repository method: findByUsername" in log:
                return [log],"gettoken", "gettoken"
    class_name, method_name = ".".join(pre_classname.split(".")[:-1]),pre_classname.split(".")[-1]
    orderclass = ["order.service.OrderServiceImpl","other.service.OrderOtherServiceImpl"]
    for i in range(idx,0,-1):
        log = logs[i]
        if class_name in log and method_name in log:
            if "queryOrdersForRefresh" in method_name:
                orderclass.remove(class_name)
                other_mehthod,other_class = "queryOrdersForRefresh",orderclass[0]
                for j in range(idx,0,-1):
                    other_log = logs[j]
                    if other_mehthod in other_log and other_class in other_log:
                        if "other" in other_class: 
                            other_log = other_log.replace("QueryInfo","OrderInfo")
                        else:
                            other_log = other_log.replace("OrderInfo","QueryInfo")
                        return [log,other_log],class_name, method_name
                        
            else:
                return [log],class_name, method_name
    return None, None, None

if __name__ == "__main__":
    # time.sleep(10)
    with open('res.log', 'r') as file:
        example_log = file.read()
    print(example_log)
    # import time
    # start_time = time.time()
    # txt_file_path = 'Test_data.txt'
    # data_constraints = 'data_constraints.json'
    # commonsense_constraints = 'commonsense_constraints.json'
    # trigger_constraints = "trigger_constraints.json"
    # trainticket_class = "Event_graph/trainticket_class_def.json"

    # logs = read_txt_file(txt_file_path)
    # trainticket_class = read_json_file(trainticket_class)
    # commonsense_constraints = read_json_file(commonsense_constraints)
    # data_constraints = read_json_file(data_constraints)
    # trigger_constraints = read_json_file(trigger_constraints)

    # chunk_size = len(logs) 

    # processes = []
    # for i in range(32):
    #     start_idx = i * chunk_size
    #     end_idx = (i + 1) * chunk_size if i < 31 else len(logs)
    #     process = multiprocessing.Process(target=main, args=(
    #         logs, trainticket_class, data_constraints, commonsense_constraints, trigger_constraints, start_idx, end_idx))
    #     processes.append(process)

    # for process in processes:
    #     process.start()

    # for process in processes:
    #     process.join()

    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(f"脚本运行了 {elapsed_time:.2f} 秒")