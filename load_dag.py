import json

# I am going to load DAG from the json file
def load_dag(file_path):
    with open(file_path, "r") as file:
        dag = json.load(file)
    return dag

# This is the path to our json file that i named with 'dag_structure.json'.
file_path = "dag_structure.json"

# We nee dto load the DAG
dag = load_dag(file_path)

# We print the DAG structure here.
print("Loaded DAG Structure:")
print(json.dumps(dag, indent=4))
