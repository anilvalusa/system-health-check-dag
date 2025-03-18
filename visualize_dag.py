import json
import asyncio
import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# Load DAG from JSON file
def load_dag(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# Simulate an asynchronous health check for a component
async def check_health(component):
    await asyncio.sleep(random.uniform(0.5, 1.5))  
    status = random.choice(["Healthy", "Unhealthy"]) 
    return component, status

# Perform asynchronous health checks for all components using BFS
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

            # Create an async task for the health check
            tasks.append(check_health(node))

    # Run all health checks asynchronously
    results = await asyncio.gather(*tasks)

    # Store results in dictionary
    for component, status in results:
        health_results[component] = status

    return health_results

# Visualize DAG with health status
def visualize_dag(dag, health_results):
    G = nx.DiGraph()

    # Add edges
    for node, dependencies in dag.items():
        for dep in dependencies:
            G.add_edge(node, dep)

    # Node colors based on health status
    node_colors = ["red" if health_results[node] == "Unhealthy" else "green" for node in G.nodes()]

    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G)  # Positioning of nodes
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color="black", node_size=2000, font_size=10, font_weight="bold")
    plt.title("System Health Status (Failed Components in Red)")
    plt.show()

# Load DAG
file_path = "dag_structure.json"
dag = load_dag(file_path)

# Run the health checks and visualize
async def main():
    health_results = await perform_health_checks(dag, "Step 1")

    # Print health status
    print("\nSystem Health Status:")
    for component, status in health_results.items():
        print(f"{component}: {status}")

    # Visualize DAG with colors
    visualize_dag(dag, health_results)

# Run the async event loop
asyncio.run(main())
