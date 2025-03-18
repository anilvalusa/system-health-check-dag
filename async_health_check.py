import json
import asyncio
import random
from collections import deque

# Loading the DAG from JSON file
def load_dag(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# Asynchronous health check for component
async def check_health(component):
    await asyncio.sleep(random.uniform(0.5, 1.5))  
    status = random.choice(["Healthy", "Unhealthy"]) 
    return component, status

# Asynchronous health check for all  component using bfs
async def perform_health_checks(dag, start_node):
    queue = deque([start_node])
    visited = set()
    health_results = {}

    tasks = []  

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            queue.extend(dag.get(node, []))

            # Iam Creating  an async task for the health check
            tasks.append(check_health(node))

    # Run all health checks asynchronously
    results = await asyncio.gather(*tasks)

    # Store results in a dictionary
    for component, status in results:
        health_results[component] = status

    return health_results

# Load DAG
file_path = "dag_structure.json"
dag = load_dag(file_path)

# Run the health checks
async def main():
    health_results = await perform_health_checks(dag, "Step 1")

    # Printing health check results
    print("\nSystem Health Status:")
    for component, status in health_results.items():
        print(f"{component}: {status}")

# Run the async event loop
asyncio.run(main())
