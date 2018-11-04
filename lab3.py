from levit import levit
from collections import deque

INFINITY = 10 ** 20

class Minimize:
    
    def __init__(self, graph, sources, endpoints):
        self.graph = graph

        self.sources = sources
        self.endpoints = endpoints

        self.endpoint_sum = sum([endpoints[node] for node in endpoints])
        self.sources_sum = sum([sources[node] for node in sources])


        self.result = []
        self.cost = 0

    def find_minimized_stream(self):

        minimum_way = None

        while self.endpoint_sum != 0 or self.sources_sum != 0:
            
            for source in self.sources:
                
                if self.sources[source] == 0:
                    continue

                for endpoint in self.endpoints:
                    if self.endpoints[endpoint] == 0 or self.sources == 0:
                        continue
                    
                    self.graph_with_cost_only = [(edge[0], edge[1], edge[2]) for edge in self.graph]
                    length_from_source, way_mapping = levit(source, endpoint, self.graph_with_cost_only)

                    if not minimum_way or minimum_way['cost'] > length_from_source[endpoint]:
                        minimum_way = {
                            'cost': length_from_source[endpoint],
                            'way': way_mapping,
                            'source': source,
                            'endpoint': endpoint
                        }

            way_to_endpoint = self.extract_full_way(
                minimum_way['way'], minimum_way['source'], minimum_way['endpoint']
            )

            minimum_way = None

            if way_to_endpoint is None:
                continue

            self.fill_edges(way_to_endpoint)


    def extract_full_way(self, way_mapping, source, endpoint):
        way = deque([])
        current_node = endpoint

        while True:
            if current_node is None:
                return

            way.appendleft(current_node)
            
            if current_node == source:
                return way

            current_node = way_mapping[current_node]
    
    def fill_edges(self, way):
        edges = []
        sum_of_cost = 0
        for i in range(len(way) - 1):
            edges.append(self.find_edge_by_node(way[i], way[i + 1], self.graph))

        all_stream_capacity = [edge[3] for edge in edges]

        minimum_stream = min(all_stream_capacity + [self.sources[way[0]], self.endpoints[way[-1]]])

        self.endpoint_sum -= minimum_stream
        self.sources_sum -= minimum_stream

        self.sources[way[0]] -= minimum_stream
        self.endpoints[way[-1]] -= minimum_stream

        filled_edges = []
        for edge in edges:
            sum_of_cost += edge[2]
            new_edge = (edge[0], edge[1], edge[2], edge[3] - minimum_stream)
            filled_edges.append(new_edge)
            self.graph.remove(edge)
            if new_edge[3] != 0:
                self.graph.append(new_edge)

        self.result.append((way, minimum_stream, sum_of_cost * minimum_stream))
        self.cost += sum_of_cost * minimum_stream

    def find_edge_by_node(self, start, end, graph):
        for edge in graph:
            if edge[0] == start and edge[1] == end:
                return edge
        



if __name__ == '__main__':
    graph = [
        ('1', '2', 3, INFINITY),
        ('1', '4', 5, 35),
        ('1', '3', 7, 10),
        ('2', '3', 2, 60),
        ('2', '5', 1, 30),
        ('3', '5', 8, INFINITY),
        ('4', '5', 4, INFINITY),
    ]
    sources = {
        '1': 40,
        '2': 50
    }
    endpoints = {
        '4': 30,
        '5': 60
    }
    minim = Minimize(graph, sources, endpoints)
    
    minim.find_minimized_stream()

    print('results')
    for res in minim.result:
        print('->'.join(list(res[0])) + ' |capacity {} cost {}'.format(res[1], res[2]))

    print('full cost')
    print(minim.cost)