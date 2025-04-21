# filename: shortest_path_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Define the graph using dictionaries
graph = {
    'Origin': {'Chicago': 40, 'McLain': 60, 'Aurora': 50},
    'Chicago': {'McLain': 10, 'Parker': 70},
    'McLain': {'Aurora': 20, 'Parker': 55, 'Smallville': 40},
    'Aurora': {'Smallville': 50},
    'Parker': {'Smallville': 10, 'Farmer': 60},
    'Smallville': {'Farmer': 80},
    'Farmer': {}
}

# Handwritten Dijkstra Algorithm
def dijkstra(graph, start, end):
    import heapq
    heap = [(0, start, [])]  # (cost_so_far, current_node, path_so_far)
    visited = set()
    
    while heap:
        (cost, node, path) = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        path = path + [node]
        
        if node == end:
            return (path, cost)
        
        for neighbor, weight in graph[node].items():
            if neighbor not in visited:
                heapq.heappush(heap, (cost + weight, neighbor, path))
    
    return (None, float('inf'))

# Streamlit App
def main():
    st.title("Shortest Path Finder App (Fictional Cities, No NetworkX)")
    st.write("This app solves the shortest path problem between fictional cities without using external libraries.")

    mode = st.selectbox("Interpret numbers as:", ["Miles (distance)", "Cost (dollars)", "Time (minutes)"])
    st.write(f"Numbers are currently interpreted as **{mode}**.")

    # Show the graph as text
    st.subheader("City Connections")
    for city, neighbors in graph.items():
        for neighbor, cost in neighbors.items():
            st.write(f"{city} ➔ {neighbor}: {cost} {mode.lower()}")

    # Find and display the shortest path
    st.subheader("Shortest Path from Origin to Farmer")
    path, total_cost = dijkstra(graph, 'Origin', 'Farmer')
    if path:
        st.success(f"The shortest path is: {' -> '.join(path)}")
        st.info(f"Total {mode.lower()}: {total_cost}")
    else:
        st.error("No path exists from Origin to Farmer.")

    # Show the adjacency table
    st.subheader("Distance/Cost/Time Table")
    df_data = []
    for from_city, connections in graph.items():
        row = {}
        for to_city in graph.keys():
            if to_city in connections:
                row[to_city] = connections[to_city]
            else:
                row[to_city] = "-"
        df_data.append(pd.Series(row, name=from_city))
    df = pd.DataFrame(df_data)
    st.dataframe(df)

if __name__ == "__main__":
    main()

