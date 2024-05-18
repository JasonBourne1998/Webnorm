import re
import textwrap
from typing import Callable

from .logger import environment


class Tester:
    @classmethod
    @environment
    def test_input_constraint(
        self,
        logs: list[str],
        class_name1: str,
        class_name2: str,
        function: Callable
    ) -> tuple[bool, str]:
        REASON_TEMPLATE = """
        There should be one or more match(es) among entities [A] and [B] in the logs:
        Entity [A] ({class_name1}):

        {objects1}

        Entity [B] ({class_name2}):

        {objects2}

        Please try again.
        """
        passed, fails, reason = False, 0, None
        objects1, objects2 = [], []

        for log in logs:
            _, objects = self._log_to_dict(class_name1, log)
            objects1 += objects
            _, objects = self._log_to_dict(class_name2, log)
            objects2 += objects

        for object1 in objects1:
            for object2 in objects2:
                try:
                    if function(object1, object2): passed = True
                except:
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
            for object_str, object in zip(objects_str, objects):
                try:
                    function(object)
                except Exception as e:
                    fails += 1
                    passed = False
                    reasons.append(F"Expected: True | Actual: False | Test case: {object_str} | Reason: {e}")

        return passed, fails, reasons
    
    @staticmethod
    def _log_to_dict(class_name: str, log: str) -> tuple[list[str], list[dict]]:
        """Extract the Class(key=value) substring from log and convert into a Python dict
        """
        float_pattern = r"^[+-]?(\d*\.\d+|\d+\.\d*)$"
        integer_pattern = r"^[+-]?\d+$"
        object_pattern = fr"{class_name}\((.*?)\)"
        objects_str: list[str] = re.findall(object_pattern, log, re.DOTALL)
        objects: list[dict] = []

        for object_str in objects_str:
            object = {}
            pairs = object_str.split(",")
            for pair in pairs:
                key, value = pair.split("=")
                key, value = key.strip(), value.strip()
                if re.match(float_pattern, value): value = float(value)
                elif re.match(integer_pattern, value): value = int(value)
                object[key] = value
            objects.append(object)

        return objects_str, objects