# filename: shortest_path_app.py

import streamlit as st
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Define the updated table with city names
data = {
    'Chicago': {'Origin': 40, 'Chicago': 0, 'McLain': 10, 'Aurora': float('inf'), 'Parker': 70, 'Smallville': float('inf'), 'Farmer': float('inf')},
    'McLain': {'Origin': 60, 'Chicago': float('inf'), 'McLain': 0, 'Aurora': 20, 'Parker': 55, 'Smallville': 40, 'Farmer': float('inf')},
    'Aurora': {'Origin': 50, 'Chicago': float('inf'), 'McLain': float('inf'), 'Aurora': 0, 'Parker': float('inf'), 'Smallville': 50, 'Farmer': float('inf')},
    'Parker': {'Origin': float('inf'), 'Chicago': float('inf'), 'McLain': float('inf'), 'Aurora': float('inf'), 'Parker': 0, 'Smallville': 10, 'Farmer': 60},
    'Smallville': {'Origin': float('inf'), 'Chicago': float('inf'), 'McLain': float('inf'), 'Aurora': float('inf'), 'Parker': float('inf'), 'Smallville': 0, 'Farmer': 80},
}
towns = ['Origin', 'Chicago', 'McLain', 'Aurora', 'Parker', 'Smallville', 'Farmer']

# Create the graph
def create_graph():
    G = nx.DiGraph()
    for city in data:
        for neighbor in data[city]:
            if not pd.isna(data[city][neighbor]) and data[city][neighbor] != float('inf'):
                G.add_edge(neighbor, city, weight=data[city][neighbor])
    return G

# Main Streamlit app
def main():
    st.title("Shortest Path Finder App (Fictional Cities Edition)")
    st.write("This app solves a shortest path problem between fictional cities.")

    mode = st.selectbox("Interpret numbers as:", ["Miles (distance)", "Cost (dollars)", "Time (minutes)"])
    st.write(f"Numbers are currently interpreted as **{mode}**.")

    G = create_graph()

    # Draw the network
    st.subheader("Network Graph")
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots()
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=9)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    st.pyplot(fig)

    # Find shortest path
    st.subheader("Shortest Path from Origin to Farmer")
    try:
        path = nx.dijkstra_path(G, source='Origin', target='Farmer', weight='weight')
        distance = nx.dijkstra_path_length(G, source='Origin', target='Farmer', weight='weight')
        st.success(f"The shortest path is: {' -> '.join(path)}")
        st.info(f"Total {mode.lower()}: {distance}")
    except nx.NetworkXNoPath:
        st.error("No path exists between Origin and Farmer.")

    # Show table
    st.subheader("Distance/Cost/Time Table")
    df = pd.DataFrame(data).fillna('-')
    st.dataframe(df)

if __name__ == "__main__":
    main()

