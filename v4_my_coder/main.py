import json
from pprint import pprint

from agents.developer import DeveloperAgent
from agents.project_manager import ProjectManagerAgent
from config import OBJECTIVE

print("***** Objective *****")
print(OBJECTIVE)
print()

project_manager = ProjectManagerAgent(objective=OBJECTIVE)
project_tasks = project_manager.run()

print("***** Project Tasks *****")
pprint(project_tasks)
print()

for task in project_tasks:
    print("***** Task *****")
    pprint(task)
    print()

    developer_agent = DeveloperAgent(task=task)
    code = developer_agent.run()
    developer_agent.write_code(code=code)

    print("***** Code *****")
    pprint(code)
    print()
