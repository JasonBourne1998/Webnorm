import javalang

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
    for _, class_node in tree.filter(javalang.tree.ClassDeclaration):
        for method in class_node.methods:
            method_info = {
                'name': method.name,
                'parameters': [(param.name, param.type.name) for param in method.parameters],
                'return_type': method.return_type.name if method.return_type else 'void',
                'modifiers': list(method.modifiers),
                'body': method.body
            }
            methods.append(method.name)
    return methods

def find_rest_template_calls_in_method(tree, method_name):
    target_method_calls = []
    for _, class_declaration in tree.filter(javalang.tree.ClassDeclaration):
        for method in class_declaration.methods:
            # print(method,method.name)
            if method.name == method_name:
                for _, node in method.filter(MethodInvocation):
                    # print(node)
                    if node.member == 'exchange' and node.qualifier == 'restTemplate':
                        url = node.arguments[0] if len(node.arguments) > 0 else None
                        http_method = node.arguments[1] if len(node.arguments) > 1 else None
                        response_type = node.arguments[3] if len(node.arguments) > 3 else None
                        url_value = extract_expression_value(url)
                        http_method_value = extract_expression_value(http_method)
                        response_type_value = extract_expression_value(response_type) if response_type else "Unknown"
                        target_method_calls.append({
                            'method_name': method_name,
                            'url': url_value,
                            'http_method': http_method_value
                        })
    return target_method_calls

if __name__ == "__main__":
    folder_name = "/home/yifannus2023/train-ticket-modify"
    import os
    scripts = []
    for root, dirs, files in os.walk(folder_name):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    # Instrument the Controller and Impl
                    if ( all(keyword in file_name for keyword in ["Impl"])) and \
                        all(keyword not in file_name for keyword in ["Test","class"]): 
                        scripts.append(file_path)   
    for script in scripts:
        print("======================")
        print("the script is:",script)
        java_file_path = script
        tree = parse_java_file(java_file_path)
        methods = extract_methods_from_java(tree)
        print(methods)
        for i in methods:
            rest_template_calls = find_rest_template_calls_in_method(tree, i)
            print(i,rest_template_calls)

