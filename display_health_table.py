import json
import asyncio
import random
from collections import deque
from tabulate import tabulate # type: ignore

# I am loading DAG from json file
def load_dag(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# We Simulate asynchronous health check for a component
async def check_health(component):
    await asyncio.sleep(random.uniform(0.5, 1.5))  # Simulate network delay
    status = random.choice(["Healthy", "Unhealthy"])  # Random health status
    return component, status

# We Simulate asynchronous health check for all compo using bfs.
async def perform_health_checks(dag, start_node):
    queue = deque([start_node])
    visited = set()
    health_results = {}

    tasks = []  # List to store async tasks

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            queue.extend(dag.get(node, []))

            # Async task for health check.
            tasks.append(check_health(node))

    # Running all health checks Async
    results = await asyncio.gather(*tasks)

    # Store results in dictionary
    for component, status in results:
        health_results[component] = status

    return health_results

# Load DAG
file_path = "dag_structure.json"
dag = load_dag(file_path)

# Run the health checks
async def main():
    health_results = await perform_health_checks(dag, "Step 1")

    # Convert results into a table format
    table_data = [[component, status] for component, status in health_results.items()]
    
    # Display table
    print("\nSystem Health Status:")
    print(tabulate(table_data, headers=["Component", "Status"], tablefmt="grid"))

# Run the async event loop
asyncio.run(main())
