import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import heapq
import matplotlib.animation as animation

def prim(graph, start):
    priority_queue = [(0, start, None)]  # (weight, current_node, previous_node)
    visited = {node: False for node in graph}
    mst_edges = []
    steps = []

    while priority_queue:
        current_weight, current_node, previous_node = heapq.heappop(priority_queue)

        if visited[current_node]:
            continue

        visited[current_node] = True
        if previous_node is not None:
            mst_edges.append((previous_node, current_node, current_weight))
        steps.append((current_node, list(mst_edges)))

        for neighbor, weight in graph[current_node].items():
            if not visited[neighbor]:
                heapq.heappush(priority_queue, (weight, neighbor, current_node))

    return mst_edges, steps

def create_graph_from_matrix(matrix):
    num_nodes = len(matrix)
    graph = {chr(65+i): {} for i in range(num_nodes)}
    for i in range(num_nodes):
        for j in range(num_nodes):
            if matrix[i][j] != 0:
                graph[chr(65+i)][chr(65+j)] = matrix[i][j]
    return graph

def get_user_input():
    num_nodes = int(input("Enter the number of nodes: "))
    print("Enter the adjacency matrix (space-separated rows, 0 for no arc):")
    matrix = []
    for i in range(num_nodes):
        row = list(map(int, input(f"Row {i + 1}: ").split()))
        matrix.append(row)
    start_node = input("Enter the start node: ").upper()
    return matrix, start_node

def visualize_prim(graph, start):
    mst_edges, steps = prim(graph, start)

    G = nx.Graph()
    for node in graph:
        for neighbor, weight in graph[node].items():
            G.add_edge(node, neighbor, weight=weight)

    pos = nx.spring_layout(G)

    fig, ax = plt.subplots(figsize=(10, 8))

    def init():
        ax.clear()
        nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=15, font_weight='bold', ax=ax)
        edge_labels = {(u, v): f'{d:.2f}' for u, v, d in G.edges(data='weight') if d is not None}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
        return ax,

    def animate(i):
        ax.clear()
        nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=15, font_weight='bold', ax=ax)
        edge_labels = {(u, v): f'{d:.2f}' for u, v, d in G.edges(data='weight') if d is not None}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

        if i < len(steps):
            current_node, mst_edges = steps[i]
            nx.draw_networkx_nodes(G, pos, nodelist=[current_node], node_color='yellow', node_size=700, ax=ax)
            edges_to_draw = [(u, v) for u, v, w in mst_edges]
            nx.draw_networkx_edges(G, pos, edgelist=edges_to_draw, edge_color='r', width=2.5, ax=ax)

        return ax,

    ani = animation.FuncAnimation(fig, animate, frames=len(steps), init_func=init, interval=1000, blit=True)
    plt.show()

if __name__ == "__main__":
    matrix, start_node = get_user_input()
    graph = create_graph_from_matrix(matrix)
    visualize_prim(graph, start_node)
