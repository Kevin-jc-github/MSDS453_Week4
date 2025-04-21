import streamlit as st
import pandas as pd
from pyvis.network import Network
import streamlit.components.v1 as components

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
    heap = [(0, start, [])]
    visited = set()
    
    while heap:
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

# Build Pyvis network
def draw_network(graph):
    net = Network(height="500px", width="100%", bgcolor="#ffffff", font_color="black", directed=True)
    
    for node in graph.keys():
        net.add_node(node, label=node)

    for from_node, edges in graph.items():
        for to_node, weight in edges.items():
            net.add_edge(from_node, to_node, label=str(weight))

    return net

# Streamlit App
def main():
    st.title("Shortest Path Finder App with Network Visualization")
    st.write("This app solves the shortest path problem and shows the network graph dynamically.")

    mode = st.selectbox("Interpret numbers as:", ["Miles (distance)", "Cost (dollars)", "Time (minutes)"])
    st.write(f"Numbers are currently interpreted as **{mode}**.")

    # Find and display the shortest path
    st.subheader("Shortest Path from Chicago to Farmer")
    path, total_cost = dijkstra(graph, 'Chicago', 'Farmer')
    if path:
        st.success(f"The shortest path is: {' -> '.join(path)}")
        st.info(f"Total {mode.lower()}: {total_cost}")
    else:
        st.error("No path exists from Chicago to Farmer.")

    # Show the network graph
    st.subheader("City Network Visualization")
    net = draw_network(graph)
    net.save_graph("network.html")
    HtmlFile = open("network.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height=550)

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
