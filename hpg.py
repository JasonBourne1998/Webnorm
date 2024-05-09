import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import os 
from slimit.parser import Parser
from slimit.visitors import nodevisitor
from slimit import ast

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

def analyze_html_js(html_file, js_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    with open(js_file, 'r', encoding='utf-8') as file:
        js_content = file.read()

    vue_data = extract_vue_data(html_content)
    functions = parse_js(js_content)

    print("Vue Data Bindings:")
    for key, value in vue_data.items():
        print(f"{key}: {value}")

    print("\nJavaScript Functions:")
    for func_name, params in functions.items():
        print(f"{func_name}({', '.join(params)})")
        


if __name__ == "__main__":
    # nodes, edges = parse_graphml('/home/yifannus2023/JAW/data/out/output.graphml')
    # print(nodes)
    # analyze_data_flow(nodes, edges, "434")
    html_parser("/home/yifannus2023/train-ticket-modify/ts-ui-dashboard/static/client_order_list.html")
    # html_file = '/home/yifannus2023/train-ticket-modify/ts-ui-dashboard/static/client_order_list.html'
    # js_file = '/home/yifannus2023/train-ticket-modify/ts-ui-dashboard/static/assets/js/client_order_list.js'
    # analyze_html_js(html_file, js_file)