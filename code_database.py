import regex as re
import os

def find_java_files(project_path):
    java_files = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith(".java") and ("Controller" in file and "Test" not in file):
                java_files.append(os.path.join(root, file))
    return java_files

def analyze_java_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 提取控制器的全局@RequestMapping注解
    base_route = re.search(r'@RequestMapping\("([^"]+)"\)', content)
    base_route = base_route.group(1) if base_route else ""
    # print(base_route)
    # 提取具体的方法和它们的路径
    methods = re.findall(r'@(GetMapping|PostMapping|PutMapping|DeleteMapping)(\s*\(\s*(?:(value|path)\s*=\s*)?"([^"]+)"\s*\)\s*public\s+[\w<>,\s]+\s+(\w+)\s*)', content)
    API_service_function = {}
    for http_method, params, _, API, function in methods:
        full_route = f"{base_route}{API}"
        # print(f"API: {http_method} {full_route} {API} ")
        start_index = content.index(params) + len(params) - 1
        # print(start_index)
        if "service" not in API:
            function_body = extract_function_body(content, start_index)
            # print("the function body is:",function_body)
            if function_body:
                service_calls = re.findall(r'\b(\w+ervice)\.(\w+)\((.*?)\)', function_body)
                for service, method, params in service_calls:
                    # print(f"Service Object: {service}, Method: {method}, Parameters: {params}")
                    API_service_function[http_method+" "+full_route] = method
    methods = re.findall(r'@(GetMapping|PostMapping|PutMapping|DeleteMapping)(?=\s*\(\s*\)|\s*public)(\s+[\w<>,\s]+\s+(\w+)\s*)',content)
    for http_method, params, function in methods:
        full_route = f"{base_route}"
        # print(f"API: {http_method} {full_route} ")
        start_index = content.index(params) + len(params) - 1
        # print(start_index)
        function_body = extract_function_body(content, start_index)
        # print("the function body is:",function_body)
        if function_body:
            service_calls = re.findall(r'\b(\w+ervice)\.(\w+)\((.*?)\)', function_body)
            for service, method, params in service_calls:
                # print(f"Service Object: {service}, Method: {method}, Parameters: {params}")
                API_service_function[http_method+" "+full_route] = method
    print("API_service_function:",API_service_function)
    return API_service_function

def extract_cilent_api_repository(API_list,API_service_functions):
    for API in API_list:
        pass

def extract_function_body(content, start_index):
    # print(content[start_index],len(content))
    n = len(content)
    count = 0
    FLAG = False
    for i in range(start_index, n):
        if content[i] == '{':
            count += 1
            FLAG = True
        elif content[i] == '}':
            count -= 1
        if count == 0 and FLAG:
            return content[start_index:i+1]

def find_api_calls(directory):
    api_pattern = re.compile(r'/api/v1[^"\'\s]*')  # 正则表达式匹配模式
    API_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".js") and file not in ["admin_config.js","admin_contacts.js","admin_price.js","admin_route.js","admin_station.js","admin_train.js"]:  # 确认文件是JavaScript文件
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as js_file:
                    content = js_file.read()
                    matches = api_pattern.findall(content)
                    if matches:
                        # print(f"Found in {file_path}:")
                        for match in set(matches):  
                            API_list.append(match)
                        print("\n")
    return API_list

def main():
    directory_path = "/home/yifannus2023/train-ticket-modify/ts-ui-dashboard/static/assets/js"
    API_list = find_api_calls(directory_path)
    print(API_list)
    project_path = '../train-ticket-modify'
    java_files = find_java_files(project_path)
    API_service_functions = []
    for java_file in java_files:
        print(f"Analyzing {java_file}")
        API_service_function = analyze_java_file(java_file)
        API_service_functions.append(API_service_function)
    extract_cilent_api_repository(API_list,API_service_functions)

if __name__ == "__main__":
    main()
