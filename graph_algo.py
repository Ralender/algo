
a1 = [(1, 2),
    (1, 3),
    (2, 5),
    (5, 4),
    (4, 3),
    (1, 4)]

a2 = [(0, 1),
    (1, 2),
    (2, 0)]

a3 = [(0, 1),
    (1, 2),
    (2, 0),
    (1, 3),
    (3, 0)]

def make_line_graph(graph:[(int, int)]):
    map = {int: []}
    edge_to_node={(int): int}
    node_id = 0
    for e in graph:
        edge_to_node[e]=node_id
        node_id = node_id + 1
        for idx in range(0, 2):
            if e[idx] in map.keys():
                map[e[idx]].append(e)
            else:
                map[e[idx]] = [e]
    res = []
    for edge in graph:
        node = edge_to_node[edge]
        for other_edge in map[edge[0]]:
            if other_edge != edge:
                t = (edge_to_node[other_edge], node)
                res.append(t)
    return res

b = make_line_graph(a1)
print(b)