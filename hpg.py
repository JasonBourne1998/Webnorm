import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import os 
import xml.etree.ElementTree as ET
from slimit.parser import Parser
from slimit.visitors import nodevisitor
from slimit import ast
import json
import esprima

namespaces = {'graphml': 'http://graphml.graphdrawing.org/xmlns'} 
class Node:
    def __init__(self, id, label, type, code, location, value):
        self.id = id
        self.label = label
        self.type = type
        self.code = code
        self.location = location
        self.value = value
        self.children = []

class Edge:
    def __init__(self, source, target, relation_label, relation_type, arguments):
        self.source = source
        self.target = target
        self.relation_label = relation_label
        self.relation_type = relation_type
        self.arguments = arguments

class API_node:
    def __init__(self, API, source, target, trigger, herf, data):
        self.API = API
        self.source = source #source API / Html / data
        self.target = target #Target API / Html / data
        self.trigger = trigger  #Trigger API / Html / data
        self.herf = herf #Can redirect ? 
        self.data = data #Caontain Data

def parse_graphml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 命名空间
    ns = {'graphml': 'http://graphml.graphdrawing.org/xmlns'}

    # 提取节点
    nodes = {}
    for node_elem in root.findall('graphml:graph/graphml:node', ns):
        node_id = node_elem.get('id')
        label = node_elem.find('graphml:data[@key="Label"]', ns).text
        type = node_elem.find('graphml:data[@key="Type"]', ns).text
        code = node_elem.find('graphml:data[@key="Code"]', ns).text
        location = node_elem.find('graphml:data[@key="Location"]', ns).text
        value = node_elem.find('graphml:data[@key="Value"]', ns).text
        nodes[node_id] = Node(node_id, label, type, code, location, value)

    # 提取边
    edges = []
    for edge_elem in root.findall('graphml:graph/graphml:edge', ns):
        source_id = edge_elem.get('source')
        target_id = edge_elem.get('target')
        relation_label = edge_elem.find('graphml:data[@key="RelationLabel"]', ns).text
        relation_type = edge_elem.find('graphml:data[@key="RelationType"]', ns).text
        arguments = edge_elem.find('graphml:data[@key="Arguments"]', ns).text
        edges.append(Edge(source_id, target_id, relation_label, relation_type, arguments))

    return nodes, edges

def analyze_data_flow(nodes, edges, start_node_id):
    start_node = nodes.get(start_node_id)
    if not start_node:
        print("Start node not found.")
        return

    queue = [start_node]
    visited = set()

    while queue:
        current_node = queue.pop(0)
        print(f"Visiting node {current_node.id} of type {current_node.type} with code {current_node.code}")

        for edge in edges:
            if edge.source == current_node.id:
                child_node = nodes.get(edge.target)
                if child_node and child_node not in visited:
                    current_node.children.append(child_node)
                    queue.append(child_node)
                    visited.add(child_node)
                    print(f" - Following edge to {child_node.id} {child_node.type}")

def html_parser(html_dir):
    with open(html_dir, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')

    elements_with_vfor = soup.find_all(lambda tag: tag.has_attr('v-for'))
    click_elements = soup.find_all(lambda tag: tag.has_attr('v-on:click'))

    # 分析每个元素的v-on:click属性
    api_relations = []
    for element in click_elements:
        action = element['v-on:click']
        method_match = re.search(r"(\w+)\((.*?)\)", action)
        if method_match:
            method_name = method_match.group(1)
            parameters = method_match.group(2)
            api_relations.append((method_name, parameters))
    
    for elem in elements_with_vfor:
        print("Element with v-for:", elem)
        print("v-for content:", elem['v-for'])
        
    results = {}
    for method, params in api_relations:
        param_list = [param.strip() for param in params.split(",")]
        results[method] = {param: set() for param in param_list}

        print("the binding is:",soup.find_all(lambda tag: tag.string and "{{" in tag.string and "}}" in tag.string))
        all_tags = soup.find_all(lambda tag: tag.string and "{{" in tag.string and "}}" in tag.string)
        for tag in all_tags:
            content = tag.string.strip()
            if "{{" in content and "}}" in content:
                expressions = content.split("}}")
                for expr in expressions:
                    if "{{" in expr:
                        key = expr.split("{{")[-1].strip()
                        if key in results[method]:
                            results[method][key].add(str(tag))

        for method, bindings in results.items():
            print(f"Method: {method}")
            for param, tags in bindings.items():
                print(f"  Param: {param}, Occurrences:")
                for tag in tags:
                    print(f"    {tag}")

def extract_vue_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    vue_data = {}

    # 提取所有带 v-model 的标签
    for tag in soup.find_all(lambda tag: tag.get('v-model')):
        vue_data[tag['v-model']] = {'type': 'v-model', 'tag': str(tag)}

    # 提取 v-for 内部的变量定义
    for tag in soup.find_all(lambda tag: tag.get('v-for')):
        expression = tag['v-for']
        # 简单的解析假设形如 "(item, index) in items"
        match = re.match(r'\((\w+),\s*(\w+)\)\s*in\s*(\w+)', expression)
        if match:
            item, index, items = match.groups()
            vue_data[index] = {'type': 'v-for', 'tag': str(tag)}
            vue_data[item] = {'type': 'v-for', 'tag': str(tag)}
    
    return vue_data

def parse_js(js_content):
    parser = Parser()
    tree = parser.parse(js_content)
    functions = {}

    for node in nodevisitor.visit(tree):
        if isinstance(node, ast.FunctionDeclaration):
            func_name = node.identifier.value
            params = [param.to_ecma() for param in node.parameters]
            functions[func_name] = params
    
    return functions

        
def analyze_html_js(file_name,graph_file,api_type):
    tree = ET.parse(graph_file)
    # js_code = read_js_code(file_name)
    if api_type == "axis":
        axis_range = extract_axis(tree)
        print(axis_range)
        url_nodes, method_nodes, data_nodes, header_nodes = extract_info(tree)
        print("the url_nodes is:",(url_nodes),len(url_nodes))
        print("the method_nodes is:",(method_nodes),len(method_nodes))
        print("the data_nodes is:",(data_nodes),len(data_nodes))
        print("the header_nodes is:",(header_nodes),len(header_nodes))
        for method_node in method_nodes: #TODO: Initialize the node
            pass
        func_API,function_range = extract_trigger_obj(tree,axis_range)
        print(func_API,type(func_API),function_range)
        method_range,mounted_range = extract_methods_range(tree)
        method_trigger = {}
        for function_name, _ in func_API.items():
            initial_caller = find_initial_caller(file_name, function_name,function_range,tree,mounted_range,method_range)
            method_trigger[function_name] = initial_caller
        print(method_trigger)
        
        extract_if_condition(tree,axis_range)

def find_nodes_by_key(root, key,value):
    namespaces = {'graphml': 'http://graphml.graphdrawing.org/xmlns'} 
    nodes = []
    for node in root.findall('graphml:graph/graphml:node', namespaces):
        for data in node.findall('graphml:data[@key="Code"]', namespaces):
            if data.text == value and (value == "url" or value == "headers"):
                nodes.append(node)
                # print(node.attrib.items())
            elif data.text == value and value == "type":
                edge = root.findall(f".//graphml:graph/graphml:edge[@target='{node.get('id')}']", namespaces)[0]
                # print("the edges is:",edge.get('source'))
                source_edges = root.findall(f".//graphml:graph/graphml:edge[@source='{edge.get('source')}']", namespaces)[-1]
                # print("the source edge is:",source_edges.get('id'))
                data_arguments = source_edges.find("graphml:data[@key='Arguments']", namespaces)
                # print(type(data_arguments.text.lower()),type(json.dumps({"kwarg":"post"})))
                # print(data_arguments.text.lower().strip(), json.dumps({"kwarg":"post"}).strip())
                if "post" in data_arguments.text.lower() or "put" in data_arguments.text.lower() or "delete" in data_arguments.text.lower() or "get" in data_arguments.text.lower():
                    nodes.append(node)
            elif data.text == value and value == "data":
                edge = root.findall(f".//graphml:graph/graphml:edge[@target='{node.get('id')}']", namespaces)[0]
                print("the edges is:",edge.get('source'))
                source_edges = root.findall(f".//graphml:graph/graphml:edge[@source='{edge.get('source')}']", namespaces)
                init_node_id = source_edges[0].get('source')
                init_node = root.findall(f".//graphml:graph/graphml:node[@id='{init_node_id}']", namespaces)[0]
                kind_data = init_node.find('graphml:data[@key="Kind"]', namespaces)
                type_data = init_node.find('graphml:data[@key="Type"]', namespaces)      
                # print("the node is:",init_node,init_node.get('id'),type_data.text )
                if type_data.text == "Property" and kind_data.text == "init":
                    if len(source_edges) == 2:
                        source_edge = source_edges[0]
                        if source_edges.index(source_edge) == 0:
                            if "data" in source_edge.find("graphml:data[@key='Arguments']", namespaces).text.lower() and "kwarg" in source_edge.find("graphml:data[@key='Arguments']", namespaces).text.lower():
                                if len(nodes) == 0:
                                    print(node.get('id'),node.find('graphml:data[@key="Location"]', namespaces).text)
                                    nodes.append(node)
                                elif node not in nodes and ( abs(int(node.get('id'))-int(nodes[-1].get('id'))) > 2 ) :
                                    print(node.get('id'),node.find('graphml:data[@key="Location"]', namespaces).text)
                                    nodes.append(node)
                                else:pass
    return nodes

def extract_trigger_obj(root,code_range):
    function_range = {}
    res = {}
    nodes = []
    for node in root.findall('graphml:graph/graphml:node', namespaces):
        Kind = node.findall('graphml:data[@key="Kind"]', namespaces)[0]
        Type = node.findall('graphml:data[@key="Type"]', namespaces)[0]
        if Kind.text == "init" and Type.text == "Property":
            Location = convert_to_dict(node.find('graphml:data[@key="Location"]', namespaces).text)
            id, ifContain =  judge_contain_Location(Location,code_range)
            if ifContain:
                source_edge = root.findall(f".//graphml:graph/graphml:edge[@source='{node.get('id')}']", namespaces)[0]
                func_name = source_edge.find("graphml:data[@key='Arguments']", namespaces).text.split(":")[-1].split("}")[0][1:-1]
                function_code_range = convert_to_dict(root.find(f".//graphml:graph/graphml:node[@id='{source_edge.get('source')}']", namespaces).find("graphml:data[@key='Location']", namespaces).text)
                # print('the range is:',func_name,function_code_range)
                if ("onConfirm" not in func_name) and ("methods" not in func_name) and ("success" not in func_name):
                    # if func_name not in res.keys():
                    #     res[func_name] = []
                    res[func_name] = id
                if func_name != "methods":
                    function_range[func_name] = function_code_range
    return res,function_range

def extract_if_condition(root,code_range):
    pass

def judge_contain_Location(main_range,ranges):
    main_start_line = main_range['start']['line']
    main_end_line = main_range['end']['line']
    ids = []
    for id, range in ranges:
        range_start_line = range['start']['line']
        range_end_line = range['end']['line']

        # 检查 main_range 是否包含当前 range
        if main_start_line <= range_start_line and main_end_line >= range_end_line:
            print(f"Main range contains range with ID {id}.")
            ids.append(id)
    if ids:return ids, True
    return None,False

def extract_axis(root):
    ajax_nodes = []
    for node in root.findall('graphml:graph/graphml:node', namespaces):
        for data in node.findall('graphml:data[@key="Code"]', namespaces):
            if data.get('key') == 'Code' and data.text == 'ajax':
                node = root.find(f".//graphml:graph/graphml:node[@id='{int(node.get('id'))+1}']", namespaces)
                print(node,data.text)
                location_data = node.findall('graphml:data[@key="Location"]', namespaces)[0]
                if location_data is not None:
                    print(f"Node ID: {node.get('id')}, Location: {location_data.text}")
                    ajax_nodes.append((node.get('id'), convert_to_dict(location_data.text)))
    return ajax_nodes

def convert_to_dict(location_str):
    json_str = location_str.replace("start", '"start"').replace("end", '"end"')
    json_str = json_str.replace("line", '"line"').replace("column", '"column"')
    location_dict = json.loads(json_str)
    return location_dict

def extract_info(root):
    url_nodes = find_nodes_by_key(root, 'code','url')
    method_nodes = find_nodes_by_key(root,'code', 'type')
    data_nodes = find_nodes_by_key(root,'code', 'data')
    header_nodes = find_nodes_by_key(root,'code', 'headers')
    return url_nodes, method_nodes, data_nodes, header_nodes  

def extract_methods_range(root):
    for node in root.findall('graphml:graph/graphml:node', namespaces):
        for data in node.findall('graphml:data[@key="Code"]', namespaces): 
            if data.get('key') == 'Code' and data.text == 'methods':
                source_edge = root.findall(f".//graphml:graph/graphml:edge[@target='{node.get('id')}']", namespaces)[0]
                node_id = root.find(f".//graphml:graph/graphml:node[@id='{source_edge.get('source')}']", namespaces)
                methods_range = node_id.find('graphml:data[@key="Location"]', namespaces).text
            if data.get('key') == 'Code' and data.text == 'mounted':
                source_edge = root.findall(f".//graphml:graph/graphml:edge[@target='{node.get('id')}']", namespaces)[0]
                node_id = root.find(f".//graphml:graph/graphml:node[@id='{source_edge.get('source')}']", namespaces)
                mounted_range = node_id.find('graphml:data[@key="Location"]', namespaces).text
    return convert_to_dict(methods_range),convert_to_dict(mounted_range)

def find_initial_caller(filename, target_function,function_range,root,mounted_range,method_range):
    pattern = target_function+"("
    trigger_function = set()
    with open(filename, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file, 1):  # enumerate从1开始计数
            if (i > method_range["start"]["line"] and i < method_range["end"]["line"]):
                if pattern in line:
                    # print('jfis,',pattern,line)
                    if (i < function_range[target_function]["start"]["line"]) or  (i > function_range[target_function]["end"]["line"]):
                        trigger_function.add(traverse(filename,target_function,function_range,i,mounted_range,root))
    return trigger_function 

def traverse(filename,target_function,function_range,line,mounted_range,root):
    func_name = None
    # print('the target function is:',target_function)
    for node in root.findall('graphml:graph/graphml:node', namespaces):
        Code = node.find('graphml:data[@key="Code"]', namespaces).text
        if Code == "methods":
            method_node = node
            # print("22",method_node.get('id'),target_function,line)
            method_obj = str(int(method_node.get('id')) + 1)
            for method_attr in root.findall(f".//graphml:graph/graphml:edge[@source='{method_obj}']", namespaces):
                if "arg" in method_attr.find('graphml:data[@key="Arguments"]', namespaces).text :
                    method_attr_range = convert_to_dict(root.find(f".//graphml:graph/graphml:node[@id='{method_attr.get('target')}']", namespaces).find('graphml:data[@key="Location"]', namespaces).text)
                    # print('the wjkf',method_attr_range,line)
                    if (line > method_attr_range["start"]["line"]) and  (line < method_attr_range["end"]["line"]):
                        for func in  root.findall(f".//graphml:graph/graphml:edge[@source='{method_attr.get('target')}']", namespaces):
                            # print('func',func.find("graphml:data[@key='Arguments']", namespaces).text.lower())
                            if "kwarg" in func.find("graphml:data[@key='Arguments']", namespaces).text.lower():
                                func_name = func.find("graphml:data[@key='Arguments']", namespaces).text.split(":")[-1].split("}")[0][1:-1]
                        # print("the method_attr_range is:",func_name, method_attr_range)
    if not func_name:
        return target_function  
    mounted_content = extract_lines(filename, mounted_range["start"]["line"], mounted_range["end"]["line"])
    for content_line in mounted_content:
        if func_name in content_line:
            return "mounted" 

    pattern = func_name + "("
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for i, file_line in enumerate(file, 1):  # 从1开始编号
                if pattern in file_line and (i < function_range["start"]["line"] or i > function_range["end"]["line"]):
                    new_func_name = traverse(filename, func_name, function_range, i, mounted_range, root)
                    return new_func_name or target_function  # 如果 new_func_name 是 None，则返回 target_function
    except Exception as e:
        pass

    return func_name or target_function
            
def read_js_code(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print("File not found. Please check the path and try again.")
        return None

def extract_lines(file_path, start_line, end_line):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    selected_lines = lines[start_line-1:end_line]  # 因为索引是从0开始的

    return selected_lines


if __name__ == "__main__":
    # nodes, edges = parse_graphml('/home/yifannus2023/JAW/data/out/output.graphml')
    # print(nodes)
    # analyze_data_flow(nodes, edges, "434")
    # html_parser("/home/yifannus2023/train-ticket-modify/ts-ui-dashboard/static/client_order_list.html")
    analyze_html_js("/home/yifannus2023/train-ticket-modify/ts-ui-dashboard/static/assets/js/client_order_list.js","/home/yifannus2023/JAW/data/out/output1.graphml","axis")