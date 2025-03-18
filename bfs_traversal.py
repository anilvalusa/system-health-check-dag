import json
from collections import deque

# Load DAG from JSON file
def load_dag(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# Here is the BFS Traversal Function
def bfs_traverse(dag, start_node):
    queue = deque([start_node])  
    visited = set()  
    traversal_order = []  

    while queue:
        node = queue.popleft()  # We need to get the first node from queue.
        if node not in visited:
            traversal_order.append(node)  # We Record the node.
            visited.add(node)
            queue.extend(dag.get(node, []))  # And we Add child nodes to the queue.

    return traversal_order

# DAG file loading
file_path = "dag_structure.json"
dag = load_dag(file_path)

# We Perform BFS from Step 1
bfs_order = bfs_traverse(dag, "Step 1")

# We Print the traversal order
print("BFS Traversal Order:")
print(" -> ".join(bfs_order))
