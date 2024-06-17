import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import heapq
import matplotlib.animation as animation

class UnionFind:
    def __init__(self, nodes):
        self.parent = {node: node for node in nodes}
        self.rank = {node: 0 for node in nodes}

    def find(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, node1, node2):
        root1 = self.find(node1)
        root2 = self.find(node2)

        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1

def kruskal(graph):
    edges = [(weight, u, v) for u in graph for v, weight in graph[u].items()]
    edges.sort()
    uf = UnionFind(graph.keys())
    mst_edges = []
    steps = []

    for weight, u, v in edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst_edges.append((u, v, weight))
            steps.append(list(mst_edges))

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
    return matrix

def visualize_kruskal(graph):
    mst_edges, steps = kruskal(graph)

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
            mst_edges = steps[i]
            edges_to_draw = [(u, v) for u, v, w in mst_edges]
            nx.draw_networkx_edges(G, pos, edgelist=edges_to_draw, edge_color='r', width=2.5, ax=ax)

        return ax,

    ani = animation.FuncAnimation(fig, animate, frames=len(steps), init_func=init, interval=1000, blit=True)
    plt.show()

if __name__ == "__main__":
    matrix = get_user_input()
    graph = create_graph_from_matrix(matrix)
    visualize_kruskal(graph)
