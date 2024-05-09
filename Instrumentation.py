import os
import re
import regex
import copy
import time 
import config_templates
import xml.etree.ElementTree as ET
from xml.dom import minidom
# Performs code instrumentation for logging, inserts logger definitions and 
# Logging statements into class declarations and public function declarations

class instrument:
    
    def __init__(self,folder_name):
        # self.script = [] # Need Instrument
        # Traverse the directory and add files that contains Controller or Impl, but not Test or Class
        # for root, dirs, files in os.walk(folder_name):
        #     for file_name in files:
        #         file_path = os.path.join(root, file_name)
        #         # Instrument the Controller and Impl
        #         if (all(keyword in file_name for keyword in ["Controller"]) or all(keyword in file_name for keyword in ["Impl"])) and \
        #             all(keyword not in file_name for keyword in ["Test","class"]): 
        #             self.script.append(file_path) 
        # for script in self.script:  
        #     try: 
        #         self.instrument_function_info(script)
        #     except Exception as error:
        #         print(error)
        #         pass
        self.script = {} # Need Instrument
        for root, dirs, files in os.walk(folder_name):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                # if "service/impl" in file_path:
                #         print(file_path)
                # Instrument the Controller and Impl
                if (all(keyword in file_name for keyword in ["Controller"])) and \
                    all(keyword not in file_name for keyword in ["Test","class"]): 
                    
                    with open(file_path, 'r', encoding='utf-8') as file:
                        for line in file:
                            if re.match(r'\s*package\s+.*;', line):
                                self.script[file_path.split("/controller")[0]] = line.strip().split(".controller")[0].split("package ")[1]
                                break
        print(self.script,len(list(self.script.keys())))
        # self.instrument_AOP()
        
    # Called for each of the files to be instrumented    
    def instrument_function_info(self,file_path):
        self.log_line_template = 'logger.info("[{}]");'

        with open(file_path, "r") as file:
            content = file.read()

        #TODO: Inserts logger defination
        # modified_content = re.sub(r"import\s+.*?;\s*", r"\g<0>import org.slf4j.Logger;\nimport org.slf4j.LoggerFactory;\n", ≈, count=1)

        # Log class declaration
        class_pattern = r'public class ([A-Za-z0-9_]+)(?:\s+implements [A-Za-z0-9_]+)?(?:\s*{)'
        modified_content = re.sub(class_pattern, lambda m: m.group() + ' \n    private static final Logger logger = LogManager.getLogger(' + m.group(1) + '.class);\n', content)
        with open(file_path, "w") as file:
            file.write(modified_content)
        print("Instrument function info Done!")
        
    def instrument_AOP(self):
        repo_config_template = config_templates.get_repo_config_template()
        for javaclass,package in self.script.items():
            self.create_folders_and_files(javaclass,package,repo_config_template)
                

    def create_folders_and_files(self,base_path,package,repo_config_template):
        CustomRepositoryFactoryBean_template = config_templates.get_CustomRepositoryFactoryBean_template()
        SecrecyPostProcessor_template = config_templates.get_SecrecyPostProcessor_template()
        SubSecrecyFilter_template = config_templates.get_SubSecrecyFilter_template()
        print(base_path)
        # for base_path in script_paths:
            # Check and Create 'security' and 'config' folder
        security_path = os.path.join(base_path, 'security')
        config_path = os.path.join(base_path, 'config')
        service_path = os.path.join(base_path, 'service')
        
        if not os.path.exists(security_path):
            os.makedirs(security_path)
        if not os.path.exists(config_path):
            os.makedirs(config_path)
        
        # Create RepoConfig.java folder
        package_name = base_path.replace('/', '.').strip('.')
        config_content = repo_config_template.format(package_name=package)
        CustomRepositoryFactoryBean_content = CustomRepositoryFactoryBean_template.format(package_name=package)
        SecrecyPostProcessor_content = SecrecyPostProcessor_template.format(package_name=package)
        SubSecrecyFilter_content = SubSecrecyFilter_template.format(package_name=package)
        #################### 
        config_file_path = os.path.join(config_path, 'RepoConfig.java')
        CustomRepositoryFactoryBean_file_path = os.path.join(security_path, 'CustomRepositoryFactoryBean.java')
        SecrecyPostProcessor_file_path = os.path.join(security_path, 'SecrecyPostProcessor.java')
        SubSecrecyFilter_file_path = os.path.join(security_path, 'SubSecrecyFilter.java')
        print(os.listdir(base_path))
        if "repository" not in os.listdir(base_path):
            if os.path.exists(config_file_path):
                os.remove(config_file_path)
            if os.path.exists(CustomRepositoryFactoryBean_file_path):
                os.remove(CustomRepositoryFactoryBean_file_path)
            if os.path.exists(SecrecyPostProcessor_file_path):
                os.remove(SecrecyPostProcessor_file_path)
            if os.path.exists(SubSecrecyFilter_file_path):
                os.remove(SubSecrecyFilter_file_path)
            without_repository_AOP_template = config_templates.get_without_repository_AOP_template()
            print(without_repository_AOP_template)
            without_repository_AOP_content = without_repository_AOP_template.format(package_name=package)
            LoggingAspect_path = os.path.join(service_path, 'LoggingAspect.java')
            with open(LoggingAspect_path, 'w') as file:
                file.write(without_repository_AOP_content) 
        else:
            with open(config_file_path, 'w') as file:
                file.write(config_content)
            with open(CustomRepositoryFactoryBean_file_path, 'w') as file:
                file.write(CustomRepositoryFactoryBean_content)
            with open(SecrecyPostProcessor_file_path, 'w') as file:
                file.write(SecrecyPostProcessor_content)
            with open(SubSecrecyFilter_file_path, 'w') as file:
                file.write(SubSecrecyFilter_content) 
            repository_AOP_template = config_templates.get_repository_AOP_template()
            repository_AOP_content = repository_AOP_template.format(package_name=package)
            LoggingAspect_path = os.path.join(service_path, 'LoggingAspect.java')
            with open(LoggingAspect_path, 'w') as file:
                file.write(repository_AOP_content) 
            pom_path = base_path.split("src/")[0] + "pom.xml"
            self.add_dependency_to_pom(pom_path)
    

    def add_dependency_to_pom(self,pom_path):
        tree = ET.parse(pom_path)
        root = tree.getroot()

        # XML 名称空间
        ns = {'maven': 'http://maven.apache.org/POM/4.0.0'}
        ET.register_namespace('', ns['maven'])

        # 寻找或创建 <dependencies> 标签
        dependencies = root.find('maven:dependencies', ns)
        if dependencies is None:
            dependencies = ET.SubElement(root, 'dependencies')

        # 创建新的 <dependency> 标签
        dependency = ET.SubElement(dependencies, 'dependency')
        group_id = ET.SubElement(dependency, 'groupId')
        group_id.text = 'org.springframework.data'
        artifact_id = ET.SubElement(dependency, 'artifactId')
        artifact_id.text = 'spring-data-commons'

        # 写回文件
        tree.write(pom_path, encoding='utf-8', xml_declaration=True)

# 调用函数，提供 pom.xml 的路径
# add_dependency_to_pom('path/to/your/pom.xml')


if __name__ == "__main__":
    a = instrument("../train-ticket-modify/")