import re
import textwrap
from typing import Callable

from .logger import environment
from typing import List, Tuple, Callable, Literal

history = []

class Tester:
    @classmethod
    @environment
    def test_input_constraint(
        self,
        logs: List[str],
        class_name1: str,
        class_name2: str,
        function: Callable
    ) -> Tuple[bool, str]:
        REASON_TEMPLATE = """
        There should be one or more match(es) among entities [A] and [B] in the logs:
        Entity [A] ({class_name1}):

        {objects1}

        Entity [B] ({class_name2}):

        {objects2}

        Please try again.
        """
        passed, fails, reason = False, 0, []
        objects1, objects2 = [], []
        
        if class_name1 == "None":
            object = {}
            for log in logs:
                if "authorization" in log:
                    pattern = r'authorization:"Bearer ([^"]+)"'
                    match = re.search(pattern, log)
                    if match:
                        token = match.group(1)
                        object["authorization"] = token
            objects1.append(object)
            
        if class_name2 == "None":
            object = {}
            for log in logs:
                if "authorization" in log:
                    pattern = r'authorization:"Bearer ([^"]+)"'
                    match = re.search(pattern, log)
                    if match:
                        token = match.group(1)
                        object["authorization"] = token
            objects2.append(object)
        if "Order" not in class_name1:
            for log in logs:
                if logs.index(log) % 2 == 0:
                    _, objects = self._log_to_dict(class_name1, log)
                    objects1 += objects
                if logs.index(log) % 2 != 0:
                    _, objects = self._log_to_dict(class_name2, log)
                    objects2 += objects
        else:
            for log in logs:
                if logs.index(log) != len(logs)-1:
                    _, objects = self._log_to_dict(class_name1, log)
                    objects1 += objects
                else:
                    _, objects = self._log_to_dict(class_name2, log)
                    objects2 += objects
        # print("232",objects1,objects2)
        if len(objects1) == 1 and len(objects2) == 1:
            for i, object1 in enumerate(objects1):
                for j, object2 in enumerate(objects2):
                    try:
                        if function(object1, object2): passed = True
                    except Exception as e:
                        print("the error is:",e,object1, object2)
                        continue
        else:
            for i, object1 in enumerate(objects1):
                for j, object2 in enumerate(objects2):
                    try:
                        if function(object1, object2): passed = True
                    except Exception as e:
                        # print('the errorlist is:',e,object1, object2)
                        continue
        if not passed:
            reason = textwrap.dedent(REASON_TEMPLATE)
            reason = reason.format(
                class_name1=class_name1,
                class_name2=class_name2,
                objects1="\n".join(f"[A{i}] {object}" for i, object in enumerate(objects1)),
                objects2="\n".join(f"[B{i}] {object}" for i, object in enumerate(objects2))
            )
            fails = 1
            # print("the reason is:",reason)
        return passed, fails, reason


    @classmethod
    @environment
    def test_flow_constraint(
        self, 
        logs: list[str], 
        branches: list[bool], 
        function: Callable
    ) -> tuple[bool, list[str]]:
        passed, fails, reasons = True, 0, []
        # print("the logs asfhjfh",logs,branches,function)
        for log, expected in zip(logs, branches):
            actual = function(log)
            if actual != expected:
                fails += 1
                passed = False
                reasons.append(F"Expected: {expected} | Actual: {actual} | Test case: {log}")
                
        return passed, fails, reasons

    @classmethod
    @environment
    def test_commonsense_contraint(
        self,
        logs: list[str],
        class_name: str,
        function: Callable
    ) -> tuple[bool, list[str]]:
        passed, fails, reasons = True, 0, []
        for log in logs:
            objects_str, objects = self._log_to_dict(class_name, log)
            # print(objects_str, objects)
            for object_str, object in zip(objects_str, objects):
                try:
                    function(object)
                except Exception as e:
                    fails += 1
                    passed = False
                    reasons.append(F"Expected: True | Actual: False | Test case: {object_str} | Reason: {e}")

        return passed, fails, reasons
    
    @classmethod
    @environment
    def test_database_constraint(
        self,
        logs1: list[str],
        logs2: list[str],
        class_name: str,
        function: Callable
    ) -> tuple[bool, list[str]]:
        REASON_TEMPLATE = """
        No instances should have inconsistencies in these logs as they are ground truth, please relax your constraint and  try again.
        Event 1 instances:
        
        {objects1}

        Event 2 instances:

        {objects2}

        Please try again.
        """
        
        passed, fails, reason = False, 0, []

        event1 = []        
        for log in logs1:
            _, objects = self._log_to_dict(class_name, log)
            event1 += objects
            
        event2 = []        
        for log in logs2:
            _, objects = self._log_to_dict(class_name, log)
            event2 += objects
                
        for i, object1 in enumerate(event1):
            for j, object2 in enumerate(event2):
                try:
                    if function(object1, object2): passed = True
                except Exception as e:
                    continue
                    
        if not passed:
            fails = 1
            reason = textwrap.dedent(REASON_TEMPLATE)
            reason = reason.format(
                objects1="\n".join(f"[A{i}] {object}" for i, object in enumerate(event1)),
                objects2="\n".join(f"[B{i}] {object}" for i, object in enumerate(event2))
            )

        return passed, fails, reason
    
    @staticmethod
    def _log_to_dict(class_name: str, log: str) -> tuple[list[str], list[dict]]:
        """Extract the Class(key=value) substring from log and convert into a Python dict
        """ 
        float_pattern = r"^[+-]?(\d*\.\d+|\d+\.\d*)$"
        integer_pattern = r"^[+-]?\d+$"
        object_pattern = fr"{class_name}\((.*?)\)"
        objects_str: list[str] = re.findall(object_pattern, log, re.DOTALL)
        objects: list[dict] = []
        # print("343xs",objects_str,class_name,log,log in history)
        # if log not in history:
        for object_str in objects_str:
            # print("object_str",object_str)
            object = {}
            pairs = object_str.split(",")
            for pair in pairs:
                if "consigneeName" in pair:
                    key, value = "consigneeName",pair.split("consigneeName=")[1]
                elif "consigneePhone" in pair:
                    # print('the pais',pair,pair.split("consigneePhone="))
                    key, value = "consigneePhone",str(pair.split("consigneePhone=")[1])
                elif "documentNumber" in pair:
                    key, value = "documentNumber",str(pair.split("documentNumber=")[1])
                elif "name=<script>location.href=" in pair:
                    key, value = "name",str(pair.split("name=")[1])
                elif "name=<div style=" in pair:
                    key, value = "name",str(pair.split("name=")[1])
                elif "phoneNumber=" in pair:
                    key, value = "phoneNumber",str(pair.split("phoneNumber=")[1])
                elif "foodName=" in pair:
                    key, value = "foodName",str(pair.split("foodName=")[1])
                else:
                    key, value = pair.split("=")
                key, value = key.strip(), value.strip()
                if re.match(float_pattern, value): value = float(value)
                elif re.match(integer_pattern, value) and "consigneePhone" not in key and "phoneNumber" not in key  and "password" not in key and "phone" not in key and "price" not in key: value = int(value)
                object[key] = value
            if "orderMoneyDifference" in log and object:
                match = re.search(r"orderMoneyDifference=([0-9]+\.[0-9]+)", log)
                if match:
                    order_money_difference = float(match.group(1))
                    object["orderMoneyDifference"] = order_money_difference
                    print("the obj is:",object)
            if "authorization" in log and object:
                pattern = r'authorization:"Bearer ([^"]+)"'
                match = re.search(pattern, log)
                if match:
                    # print("insert token in obj")
                    token = match.group(1)
                    object["authorization"] = token
            objects.append(object)   
            history.append(log)
            
        if "string" in class_name.lower():
            object = {}
            pattern = r'[0-9a-fA-F-]{36}'
            match = re.search(pattern, log)
            if match and "authorization" in log:
                if "string accountId orderId" in class_name:
                    object[class_name.split("string")[2].strip()] = match.group(1)
                object[class_name.split("string")[1].strip()] = match.group(0)
                # objects.append(object)
                pattern = r'authorization:"Bearer ([^"]+)"'
                match = re.search(pattern, log)
                if match:
                    # print("insert token in obj")
                    token = match.group(1)
                    object["authorization"] = token
                objects.append(object)
            elif match and "authorization" not in log:
                object[class_name.split("string")[1].strip()] = match.group(0)
                objects.append(object)
            history.append(log)
            # print("the objects",objects)
        # print('the objects is:',objects)
        return objects_str, objects