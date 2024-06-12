import json
import re
from consistency_prompt.gptchecker.tester import Tester
import multiprocessing

def read_txt_file(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    return lines

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def main(txt_file_path,start_idx, end_idx, json_file_path,data_constraints,commonsense_constraints,trigger_constraints):
    # 读取 txt 文件和 json 文件
    logs = read_txt_file(txt_file_path)[start_idx:end_idx]
    trainticket_class = read_json_file(json_file_path)
    commonsense_constraints = read_json_file(commonsense_constraints)
    data_constraints = read_json_file(data_constraints)
    trigger_constraints = read_json_file(trigger_constraints)
    # for i,j in commonsense_constraints.items():
    #     print(j)
    for log in logs:
        method_name,class_name = extract_class_method(log)
        # print(method_name,class_name)
        if (method_name and class_name) and "gettoken" not in method_name.lower():
            # print(list(commonsense_constraints.keys()))
            if class_name + "." + method_name in list(commonsense_constraints.keys()):
                code_str = commonsense_constraints[class_name + "." + method_name]
                classname = trainticket_class[class_name + "." + method_name]["input"][0]
                # print(log,code_str,classname)
                exec_namespace = {}
                try:
                    exec(code_str, exec_namespace)
                    assert 'is_valid' in exec_namespace
                    is_valid = exec_namespace['is_valid']
                    result = Tester.test_commonsense_contraint([log], classname, is_valid)
                except Exception as e:
                    # print(method_name,class_name,code_str)
                    print("---error---")
                    print(str(e))  # 打印异常信息
            for dataflow, constraint in data_constraints.items():
                pre,follow = dataflow.split(">")[0].strip(), dataflow.split(">")[1].strip()
                if class_name + "." + method_name in follow:
                    code_str = data_constraints[dataflow]
                    pre_classname = trainticket_class[pre]["output"][0]
                    after_classname = trainticket_class[follow]["input"][0]
                    # print(pre,follow)
                    # print(code_str)
                    exec_namespace = {}
                    pre_log,pre_class_name, pre_method_name = find_last_log(log,pre,txt_file_path)
                    if pre_method_name:
                        logset = []
                        for lg in pre_log:
                            logset.append(lg)
                        logset.append(log)
                        if not ("queryByBatch" in pre_method_name and "preserve" in method_name):
                            try:
                                exec(code_str, exec_namespace)
                                assert 'is_related' in exec_namespace
                                is_related = exec_namespace['is_related']
                                result = Tester.test_input_constraint(logset, pre_classname,after_classname, is_related)
                            except Exception as e:
                                print("---error---")
                                print(str(e))  
            for triggerflow, constraint in trigger_constraints.items():
                pre,follow = triggerflow.split(">")[0].strip(), triggerflow.split(">")[1].strip()
                if class_name + "." + method_name in follow:
                    code_str = trigger_constraints[triggerflow]
                    exec_namespace = {}
                    if pre not in "findByUsername":
                        pre_classname = trainticket_class[pre]["output"][0]
                        after_classname = trainticket_class[follow]["input"][0]
                        pre_log,pre_class_name, pre_method_name = find_last_log(log,pre,txt_file_path)
                    else:
                        pre_log,pre_class_name, pre_method_name = find_last_log(log,"findByUsername",txt_file_path)
                    if pre_method_name:
                        logset = []
                        for lg in pre_log:
                            logset.append(lg)
                        logset.append(log)
                        # print(pre_class_name, pre_method_name,class_name,method_name)
                        if not ("queryByBatch" in pre_method_name and "preserve" in method_name):
                            try:
                                exec(code_str, exec_namespace)
                                assert 'is_branch_a' in exec_namespace
                                is_related = exec_namespace['is_branch_a']
                                result = Tester.test_flow_constraint(logset, [True], is_related)
                            except Exception as e:
                                print("---error---")
                                print(str(e))  # 打印异常信息
                    
def extract_class_method(line):
    class_method_pattern = re.compile(r'Entering in Method: (\w+), Class: ([\w\.]+)')
    method_name,class_name = None,None
    match = class_method_pattern.search(line)
    if match:
        method_name = match.group(1)
        class_name = match.group(2)
    return method_name,class_name

def find_last_log(after_log,pre_classname,txt_file_path):
    logs = read_txt_file(txt_file_path)
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
    import time
    start_time = time.time()
    txt_file_path = '/home/yifannus2023/TamperLogPrompt/Attack_data_modify.txt'
    data_constraints = '/home/yifannus2023/TamperLogPrompt/data_constrains.json'
    commonsense_constraints = '/home/yifannus2023/TamperLogPrompt/commonsense_constraint.json'
    trigger_constraints = "/home/yifannus2023/TamperLogPrompt/trigger_constraints.json"
    trainticket_class = "/home/yifannus2023/TamperLogPrompt/trainticket_class_def.json"

    logs = read_txt_file(txt_file_path)
    chunk_size = len(logs) // 32

    processes = []

    for i in range(32):
        start_idx = i * chunk_size
        end_idx = (i + 1) * chunk_size if i < 31 else len(logs)
        process = multiprocessing.Process(target=main, args=(txt_file_path, start_idx, end_idx, trainticket_class, data_constraints, commonsense_constraints, trigger_constraints))
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"脚本运行了 {elapsed_time:.2f} 秒")
