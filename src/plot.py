import igraph as ig
from matplotlib import patches
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

def translate_nodes (vertices, removed_nodes) -> set[int]:
    translated_nodes = set()
    for vertex in vertices:
        if int(vertex["name"]) in removed_nodes:
            translated_nodes.add(vertex.index)
    return translated_nodes

def forest_visualization (infected: set[int], filename : str, fig : Figure, ax, removed_nodes=()):
    '''
    function that visualize the forest of the infection
    input: forest is the forest of the infection, filename is the name of the file containing the graph
    output: it doesn't return anything, it just create a graph visualization
    '''

    # create a graph
    G = ig.Graph.Read_Ncol(filename, names=True, directed=True)

    translated_removed_nodes = translate_nodes(G.vs, removed_nodes)

    # create the visualization
    infected_patch = patches.Patch(color='red', label='Infected')
    noninfected_patch = patches.Patch(color='grey', label='Non infected')
    fig.legend(handles=[infected_patch, noninfected_patch], loc='outside upper right')
    ig.plot(
        G,
        target=ax,
        vertex_size=0.2, # size of the nodes
        vertex_color=["grey" if int(node) not in infected else "red" for node in G.vs["name"]],
        vertex_label=G.vs["name"],
        vertex_label_size=7.0,
        vertex_frame_width=4.0,
        vertex_frame_color="white",
        edge_label=G.es["weight"],
        edge_label_size=7.0,
        edge_width=0.5,
        edge_color=["grey" if int(edge.source) not in translated_removed_nodes and int(edge.target) not in translated_removed_nodes else "white" for edge in G.es],
        edge_label_color=["black" if int(edge.source) not in translated_removed_nodes and int(edge.target) not in translated_removed_nodes else "white" for edge in G.es],
    )

def plot_infection(no_prevention, prevention):
    plt.subplots(figsize=(5, 5))
    
    plt.plot(set_plot, label="No preventive measures", color="blue")
    plt.plot(data, label="Subtree algorithm", color="red")
    
    plt.legend(loc="lower right", fontsize=14)
    plt.xlabel("Time")
    plt.ylabel("Number of infected nodes")
    plt.show()