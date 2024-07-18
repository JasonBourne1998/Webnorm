import json
from dataflow_and_trigger import *

log_file_path = "/home/yifannus2023/TamperLogPrompt/Train_data_modify.txt"
log_lines = read_log_file(log_file_path)
with open("/home/yifannus2023/TamperLogPrompt/openAPI.json","r") as fp:
    API_data = json.load(fp)
res = {}
for API_name, API_path in API_data.items():
    if API_name not in list(res.keys()):
        res[API_name] = []
    for line in log_lines:
        service,function = API_name.split(" ")
        if service in line and function in line:
            res[API_name].append(line)
# print(res)
with open("/home/yifannus2023/TamperLogPrompt/log_target.json","w") as fp:
    json.dump(res,fp)
    