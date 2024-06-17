import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import heapq
import matplotlib.animation as animation

def dijkstra(graph, start):
    priority_queue = [(0, start)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    shortest_path_tree = {}
    steps = []

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_node]:
            continue

        steps.append((current_node, dict(distances)))

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
                shortest_path_tree[neighbor] = current_node
    
    return distances, shortest_path_tree, steps

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
    end_node = input("Enter the end node: ").upper()
    return matrix, start_node, end_node

def visualize_dijkstra(graph, start, end):
    distances, shortest_path_tree, steps = dijkstra(graph, start)

    G = nx.Graph(graph)
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
            current_node, distances = steps[i]
            nx.draw_networkx_nodes(G, pos, nodelist=[current_node], node_color='yellow', node_size=700, ax=ax)
            for node in distances:
                if distances[node] < float('inf'):
                    nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color='lightgreen', node_size=700, ax=ax)
                    if node in shortest_path_tree:
                        edge = (shortest_path_tree[node], node)
                        nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color='r', width=2.5, ax=ax)

        if end in distances and distances[end] < float('inf'):
            path = []
            node = end
            while node != start:
                path.append((shortest_path_tree[node], node))
                node = shortest_path_tree[node]
            path = list(reversed(path))
            nx.draw_networkx_edges(G, pos, edgelist=path, edge_color='b', width=3.0, ax=ax)

        return ax,

    ani = animation.FuncAnimation(fig, animate, frames=len(steps), init_func=init, interval=1000, blit=True)
    plt.show()

if __name__ == "__main__":
    matrix, start_node, end_node = get_user_input()
    graph = create_graph_from_matrix(matrix)
    visualize_dijkstra(graph, start_node, end_node)
