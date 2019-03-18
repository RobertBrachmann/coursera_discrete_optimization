import networkx as nx


def greedy_networkx(node_count, edges):

    # create graph
    graph = nx.Graph()
    graph.add_nodes_from(range(node_count))
    graph.add_edges_from(edges)

    # set of strategies
    strategies = [nx.coloring.strategy_largest_first,
                  nx.coloring.strategy_random_sequential,
                  nx.coloring.strategy_smallest_last,
                  nx.coloring.strategy_independent_set,
                  nx.coloring.strategy_connected_sequential_bfs,
                  nx.coloring.strategy_connected_sequential_dfs,
                  nx.coloring.strategy_connected_sequential,
                  nx.coloring.strategy_saturation_largest_first]

    # initial values
    best_color_count, best_coloring = node_count, {i: i for i in range(node_count)}

    # run algorithms and return best
    for strategy in strategies:
        curr_coloring = nx.coloring.greedy_color(G=graph, strategy=strategy)
        curr_color_count = max(curr_coloring.values()) + 1
        if curr_color_count < best_color_count:
            best_color_count = curr_color_count
            best_coloring = curr_coloring
    return best_color_count, 0, [best_coloring[i] for i in range(node_count)]