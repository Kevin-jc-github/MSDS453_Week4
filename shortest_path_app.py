import streamlit as st
import pandas as pd
from pyvis.network import Network
import streamlit.components.v1 as components

# 💥 更帅气的 title
st.set_page_config(page_title="🚦 City Navigator Pro", layout="wide")

st.title("🚦 City Navigator Pro: The Ultimate Shortest Path Finder")
st.markdown("Welcome to the **futuristic city transport simulator**. Navigate between fictional cities with style. 🌆🛰️")

# 城市图结构
graph = {
    'Chicago': {'McLain': 40, 'Aurora': 60, 'Parker': 50},
    'McLain': {'Aurora': 10, 'Parker': 70},
    'Aurora': {'Parker': 20, 'Smallville': 55, 'Farmer': 40},
    'Parker': {'Smallville': 10, 'Farmer': 60},
    'Smallville': {'Farmer': 80},
    'Farmer': {}
}

# 🧠 手写Dijkstra算法
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

# 🧩 pyvis 动态图生成器（高亮路径）
def draw_network(graph, highlight_path=None):
    net = Network(height="500px", width="100%", bgcolor="#222222", font_color="white", directed=True)
    
    for node in graph.keys():
        color = "#ffa726" if highlight_path and node in highlight_path else "#26c6da"
        net.add_node(node, label=node, color=color)

    for from_node, edges in graph.items():
        for to_node, weight in edges.items():
            if highlight_path and from_node in highlight_path and to_node in highlight_path:
                edge_color = "#ff5252"
                width = 4
            else:
                edge_color = "gray"
                width = 1
            net.add_edge(from_node, to_node, label=str(weight), color=edge_color, width=width)

    return net

# 🌟 页面功能开始
mode = st.selectbox("Interpret numbers as:", ["Miles (distance)", "Cost (dollars)", "Time (minutes)"])
st.toast(f"Mode set to: {mode}", icon="🚗")

st.subheader("📍 Finding Shortest Path from Chicago ➡️ Farmer")
path, total_cost = dijkstra(graph, 'Chicago', 'Farmer')
if path:
    st.success(f"✅ Shortest Path: {' ➡️ '.join(path)}")
    st.info(f"🧾 Total {mode.lower()}: **{total_cost}**")
else:
    st.error("🚫 No path exists from Chicago to Farmer.")

# 🌐 显示 network 图
st.subheader("🌐 Fictional City Network")
net = draw_network(graph, highlight_path=path)
net.save_graph("network.html")
HtmlFile = open("network.html", 'r', encoding='utf-8')
components.html(HtmlFile.read(), height=550)

# 📊 显示邻接矩阵
st.subheader("📊 Distance/Cost/Time Table")
rows = []
cities = list(graph.keys())
for from_city in cities:
    row = {}
    for to_city in cities:
        row[to_city] = graph[from_city].get(to_city, "-")
    rows.append(pd.Series(row, name=from_city))
df = pd.DataFrame(rows)
st.dataframe(df)

# 🎉 彩蛋动画
st.balloons()
