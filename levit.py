from collections import defaultdict
from collections import deque

INFINITY = 10 ** 20

def get_node_list(graph):
    nodes = []
    for node_1, node_2, _ in graph:
        nodes.append(node_1)
        nodes.append(node_2)
    
    return list(set(nodes))


def prepare_dict_of_len(start, graph):
    from_node_to_other = defaultdict(dict)
    for node in get_node_list(graph):
        if start == node:
            from_node_to_other[node] = 0
            continue           

        from_node_to_other[node] = INFINITY

    return from_node_to_other


def prepare_way_mapping(start, graph):
    way_dict = {}
    for node in get_node_list(graph):
        if start == node:
            continue

        way_dict[node] = None

    return way_dict
        


def levit(start, end, graph):
    from_start_to_all = prepare_dict_of_len(start, graph)
    way_mapping = prepare_way_mapping(start, graph)

    nodes_with_len = []
    node_with_processing_len = deque([start])
    node_with_undefined_len = [node for node in get_node_list(graph) if node != start]

    while node_with_processing_len:
        current_node = node_with_processing_len.popleft()
        nodes_with_len.append(current_node)

        edges = filter(lambda edge: current_node == edge[0], graph)

        for _, end, length in edges:

            if end in node_with_undefined_len:
                node_with_undefined_len.remove(end)
                node_with_processing_len.append(end)

                from_start_to_all[end] = from_start_to_all[current_node] + length
                way_mapping[end] = current_node

            if end in node_with_processing_len:
                if from_start_to_all[current_node] + length < from_start_to_all[end]:
                    from_start_to_all[end] = from_start_to_all[current_node] + length
                    way_mapping[end] = current_node
            
            if end in nodes_with_len:
                if from_start_to_all[current_node] + length < from_start_to_all[end]:
                    from_start_to_all[end] = from_start_to_all[current_node] + length
                    way_mapping[end] = current_node

                    nodes_with_len.remove(end)
                    node_with_processing_len.appendleft(end)
    
    return from_start_to_all,  way_mapping

            

            
