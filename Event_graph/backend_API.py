import javalang
import re
import os
import json
from javalang.tree import MethodInvocation, MemberReference, Literal, BinaryOperation, ClassReference

def parse_java_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    tree = javalang.parse.parse(data)
    return tree

def extract_expression_value(expr):
    if isinstance(expr, Literal):
        return expr.value
    elif isinstance(expr, BinaryOperation):
        left = extract_expression_value(expr.operandl)
        right = extract_expression_value(expr.operandr)
        return f"{left}{right}"
    elif isinstance(expr, MemberReference):
        return expr.member
    elif isinstance(expr, ClassReference):
        return expr.type.name
    elif isinstance(expr, MethodInvocation):
        if expr.member == 'toString':
            return "Method Call: toString"
        return "Complex Method Call"
    else:
        return str(expr)

def extract_methods_from_java(tree):
    """ Extract all methods from the Java AST tree. """
    methods = []
    rest = []
    method_bodies = {}
    for _, class_node in tree.filter(javalang.tree.ClassDeclaration):
        for method in class_node.methods:
            method_info = {
                'name': method.name,
                'parameters': [(param.name, param.type.name) for param in method.parameters],
                'return_type': method.return_type.name if method.return_type else 'void',
                'modifiers': list(method.modifiers),
                'body': method.body
            }
            methods.append(method_info)
            rest.append(method.name)
            method_bodies[method.name] = method
    return methods, method_bodies, rest

def get_method_body_code(file_path, method):
    """ Extract the method body code as a string from the source file. """
    with open(file_path, 'r') as file:
        data = file.read()
    
    # Adjust the pattern to handle newlines and whitespace characters
    pattern = re.compile(r'(public|private|protected)\s+(?:\w+|<[^<>]+(?:<(?:[^<>]+|[^<>]*)*>)?>)+\s+{}\s*\([^)]*\)\s*\{{'.format(method.name), re.DOTALL)
    match = pattern.search(data)
    
    if match:
        start = match.start()
        end = match.end()
        brackets = 1
        while end < len(data) and brackets > 0:
            if data[end] == '{':
                brackets += 1
            elif data[end] == '}':
                brackets -= 1
            end += 1
        return data[start:end]
    return ""

def extract_url_path(url):
    """ Extract the URL path that contains /api/v1 and handle dynamic path parameters """
    match = re.search(r'(/api/v1[^\s"]*)', url)
    print('jf',url)
    if match:
        url_path = match.group(1)
        rest = url.split(url_path)[-1].strip()
        print(rest)
        if rest and len(rest) > 1:
            # dynamic_parts = re.findall(r'["\']([^"\']+)["\']', rest)
            # if dynamic_parts:
            #     dynamic_str = ''.join([f'{{{part}}}' for part in dynamic_parts])
                return url_path + "{"
        return url_path
    return url

def find_method_calls_in_body(body_code, method_list):
    """ Find all method calls in the given method body code. """
    invocations = []
    seen_methods = set()  # Set to track methods that have already been added to the list
    for method in method_list:
        pattern = re.compile(r'(?<![.\w])\b{}\b'.format(method['name']))
        matches = pattern.finditer(body_code)
        for match in matches:
            if method['name'] not in seen_methods:
                invocations.append((match.start(), method['name']))
                seen_methods.add(method['name'])
    invocations.sort()  # Sort by the order of appearance in the code
    return [invocation[1] for invocation in invocations]

def find_url_assignments(body_code, url_variable):
    """ Find all assignments to the URL variable in the given method body code. """
    # print("the:",url_variable,body_code)
    pattern = re.compile(r'{}[\s]*=[\s]*([^;]+);'.format(url_variable))
    # print(pattern)
    matches = pattern.findall(body_code)
    # print("match:",matches)
    return matches

def find_rest_template_calls_in_method(tree, method_name,file_path):
    target_method_calls = []
    for _, class_declaration in tree.filter(javalang.tree.ClassDeclaration):
        for method in class_declaration.methods:
            if method.name == method_name:
                for _, node in method.filter(MethodInvocation):
                    if node.member == 'exchange' and node.qualifier and 'restTemplate' in node.qualifier:
                        url = node.arguments[0] if len(node.arguments) > 0 else None
                        http_method = node.arguments[1] if len(node.arguments) > 1 else None
                        response_type = node.arguments[3] if len(node.arguments) > 3 else None
                        url_value = extract_expression_value(url)
                        
                        if '/api/v1' not in url_value:
                            print(file_path,method.name)
                            body_code = get_method_body_code(file_path, method)
                            url_assignments = find_url_assignments(body_code, url_value)
                            for assignment in url_assignments:
                                # print(assignment)
                                if '/api/v1' in assignment:
                                    url_value = assignment
                                    break
                        
                        url_path = extract_url_path(url_value)
                        http_method_value = extract_expression_value(http_method)
                        response_type_value = extract_expression_value(response_type) if response_type else "Unknown"
                        target_method_calls.append({
                            'method_name': method_name,
                            'url': url_path,
                            'http_method': http_method_value
                        })
    return target_method_calls

def find_all_rest_template_calls(method_name, methods, method_bodies, file_path):
    """ Recursively find all RestTemplate calls in the given method and its called methods. """
    method_calls = set()
    rest_template_calls = []

    def _find_calls(current_method):
        if current_method in method_calls:
            return
        method_calls.add(current_method)
        body_code = get_method_body_code(file_path, method_bodies[current_method])
        method_invocations = find_method_calls_in_body(body_code, methods)
        for invocation in method_invocations:
            if invocation not in method_calls:
                _find_calls(invocation)
        
        rest_calls = find_rest_template_calls_in_method(parse_java_file(file_path), current_method, file_path)
        rest_template_calls.extend(rest_calls)

    _find_calls(method_name)
    return rest_template_calls

def find_service_method(controller_file_path, rest_call):
    with open(controller_file_path, 'r') as file:
        content = file.read()
    
    url_path = rest_call['url']
    http_method = rest_call['http_method'].lower()
    # print(http_method, rest_call['url'], url_path)
    
    mapping_pattern = {
        'get': r'@GetMapping',
        'post': r'@PostMapping',
        'put': r'@PutMapping',
        'delete': r'@DeleteMapping'
    }

    if http_method not in mapping_pattern:
        return None

    # 修改后的正则表达式以支持path或value和public或private方法
    pattern = (
        mapping_pattern[http_method] +
        r'\((?:path|value)\s*=\s*["\']' +
        re.escape(url_path.split('service')[1]).replace(r'\{', r'{').replace(r'\}', r'}') +
        r'["\'][^)]*\)\s*(?:public|private|protected)\s+[^\{]*\{'
    )
    print('The pattern is:', pattern)
    match = re.search(pattern, content, re.DOTALL)
    print(match)
    if match:
        method_declaration = match.group()
        print(method_declaration)
        # 提取方法体
        method_body_start = content.find('{', match.end() - 1)
        method_body_end = method_body_start
        brackets = 1
        while brackets > 0 and method_body_end < len(content):
            method_body_end += 1
            if content[method_body_end] == '{':
                brackets += 1
            elif content[method_body_end] == '}':
                brackets -= 1
        method_body = content[method_body_start:method_body_end + 1]

        # 查找 return 语句
        service_call_pattern = re.compile(r'return\s+ok\((\w+\.\w+)\(')
        service_call_match = service_call_pattern.search(method_body)
        if service_call_match:
            return service_call_match.group(1)
    return None

def convert_service_to_directory(service_name):
    """ Convert service name to corresponding directory format. """
    print("11",service_name)
    return "ts-" + service_name.replace('service', '-service') if 'service' in service_name else "ts-" + service_name.replace('Service', '-Service')

def find_controller_file(service_directory, url_path):
    """ Find the controller file in the given service directory. """
    # print('in path',url_path.split('service/')[1])
    for root, dirs, files in os.walk(service_directory):
        for file in files:
            if file.endswith("Controller.java") and "Test" not in file:
                controller_file_path = os.path.join(root, file)
                with open(controller_file_path, 'r') as file:
                    content = file.read()
                    if url_path.split('service/')[1] in content:
                        return controller_file_path
    return None

if __name__ == "__main__":
    folder_name = "/home/yifannus2023/train-ticket-modify"
    import os
    scripts = []
    for root, dirs, files in os.walk(folder_name):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # Instrument the Controller and Impl
            if all(keyword in file_name for keyword in ["Impl"]) and all(keyword not in file_name for keyword in ["Test","class"]):
                scripts.append(file_path)
    results = {}
    supply = []
    for script in scripts:
        print("======================")
        print("the script is:", script)
        results[script] = {}
        # if ("rebook" in script.lower()) or ("travel" in script.lower()):
        java_file_path = script
        tree = parse_java_file(java_file_path)
        methods, method_bodies, rest = extract_methods_from_java(tree)
        for method in methods:
            method_name = method['name']
            print(f"Method: {method_name}")
            body_code = get_method_body_code(java_file_path, method_bodies[method_name])
            method_invocations = find_method_calls_in_body(body_code, methods)
            rest_template_calls = find_rest_template_calls_in_method(tree, method_name, java_file_path)
            all_rest_template_calls = find_all_rest_template_calls(method_name, methods, method_bodies, java_file_path)
            method_info = {
                'method_name': method_name,
                'invocations': method_invocations,
                'rest_template_calls': rest_template_calls,
                'all_rest_template_calls': all_rest_template_calls,
                'service_methods': []
            }
            for rest_call in all_rest_template_calls:
                try:
                    service_name = rest_call['url'].split('/')[3]
                    service_directory = os.path.join(folder_name, convert_service_to_directory(service_name))
                    controller_file_path = find_controller_file(service_directory, rest_call['url'])
                    if controller_file_path:
                        service_method = find_service_method(controller_file_path, rest_call)
                        if service_method:
                            method_info['service_methods'].append(service_method)
                        else:
                            if (rest_call['http_method'],rest_call['url']) not in supply and (rest_call['http_method'] not in "DELETE"):
                                supply.append((rest_call['http_method'],rest_call['url']))
                    else:
                        print(f"Controller file not found for service: {service_directory}")
                except Exception as e:
                    print(f"Error processing rest_call {rest_call}: {e}")
            results[script][method_name] = method_info
    
    with open('method_analysis.json', 'w') as json_file:
        json.dump(results, json_file, indent=4)
    
    print("Results saved to method_analysis.json")
    print(supply)
    
