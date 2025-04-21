import streamlit as st
import pandas as pd

# Corrected city mapping
graph = {
    'Chicago': {'McLain': 40, 'Aurora': 60, 'Parker': 50},
    'McLain': {'Aurora': 10, 'Parker': 70},
    'Aurora': {'Parker': 20, 'Smallville': 55, 'Farmer': 40},
    'Parker': {'Smallville': 10, 'Farmer': 60},
    'Smallville': {'Farmer': 80},
    'Farmer': {}
}

# Handwritten Dijkstra Algorithm
def dijkstra(graph, start, end):
    heap = [(0, start, [])]  # (cost_so_far, current_node, path_so_far)
    visited = set()
    
    while heap:
        # Sort heap manually since we don't import heapq
        heap.sort()
        (cost, node, path) = heap.pop(0)
        
        if node in visited:
            continue
        visited.add(node)
        path = path + [node]
        
        if node == end:
            return (path, cost)
        
        for neighbor, weight in graph[node].items():
            if neighbor not in visited:
                heap.append((cost + weight, neighbor, path))
    
    return (None, float('inf'))

# Streamlit App
def main():
    st.title("Shortest Path Finder App (Corrected City Mapping)")
    st.write("This app solves the shortest path problem between fictional cities without external libraries.")

    mode = st.selectbox("Interpret numbers as:", ["Miles (distance)", "Cost (dollars)", "Time (minutes)"])
    st.write(f"Numbers are currently interpreted as **{mode}**.")

    # Show the graph as text
    st.subheader("City Connections")
    for city, neighbors in graph.items():
        for neighbor, cost in neighbors.items():
            st.write(f"{city} ➔ {neighbor}: {cost} {mode.lower()}")

    # Find and display the shortest path
    st.subheader("Shortest Path from Chicago to Farmer")
    path, total_cost = dijkstra(graph, 'Chicago', 'Farmer')
    if path:
        st.success(f"The shortest path is: {' -> '.join(path)}")
        st.info(f"Total {mode.lower()}: {total_cost}")
    else:
        st.error("No path exists from Chicago to Farmer.")

    # Show the adjacency table
    st.subheader("Distance/Cost/Time Table")
    rows = []
    cities = list(graph.keys())
    for from_city in cities:
        row = {}
        for to_city in cities:
            row[to_city] = graph[from_city].get(to_city, "-")
        rows.append(pd.Series(row, name=from_city))
    df = pd.DataFrame(rows)
    st.dataframe(df)

if __name__ == "__main__":
    main()


