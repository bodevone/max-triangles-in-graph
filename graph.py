import matplotlib.pyplot as plt
import networkx as nx

def main():
    vertices = 10
    edges = 20
    k = 5
    G = nx.dense_gnm_random_graph(vertices, edges)
    draw(G)
    solve(G, k)

def draw(G, weighted = False):
    plt.figure(figsize=(5,5))
    pos = nx.spring_layout(G)  # positions for all nodes
    nx.draw_networkx_nodes(G, pos, node_size=400)
    nx.draw_networkx_labels(G, pos, font_size=15, font_family='sans-serif')
    nx.draw_networkx_edges(G, pos, width=2)

    plt.axis('off')
    plt.show()

def solve(G, k):
    solve1(G, k)


def solve1(G, k):
    for n in G.nodes():
        for key, value in G.neighbors(n).iteritems():
            print(key, value)

if __name__ == "__main__":
    main()