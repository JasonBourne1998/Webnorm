import os
import json
import sys
from dotenv import load_dotenv
sys.path.append("../")
from consistency_prompt.gptchecker import GPTChecker

env_path = '../consistency_prompt/.env'
load_dotenv(dotenv_path=env_path)
api_key = os.getenv('API_KEY')

if api_key == "null":
    with open('commonsense_class_res.log', 'r') as file:
        example_log = file.read()
    print(example_log)
    sys.exit()

dataset_dir = os.path.join("dataset/method")
class_definition_file = open("commonsense_class.json")
class_definitions: dict[str, dict] = json.load(class_definition_file)
checker = GPTChecker(
    api_key=api_key,
    model="gpt-4o",
    max_tokens=2048,
    top_p=0.9,
    temperature=0.0,
    turns=10
)

result = {}

for full_method_name, class_io in class_definitions.items():
    method_name = full_method_name.split(".")[-1]
    class_name = class_io["class_name"]
    class_definition = class_io["input"]
    snapshot_path = os.path.join(dataset_dir, method_name, "snapshot_0.json")
    snapshot_file = open(snapshot_path)
    snapshot: dict = json.load(snapshot_file)
    logs = [log["arguments"] for log in snapshot]

    _, code = checker.check_commonsense_constraint(class_name, class_definition, logs)

    result[full_method_name] = code

with open("commonsense_constraints_class.json", "w") as f:
    json.dump(result, f)