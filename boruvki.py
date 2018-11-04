import json

from collections import defaultdict

MAX_VAL = 10**100


class BoruvkiAlgo():
    used_points = []
    free_points = []
    points_mapper = defaultdict(dict)

    boruvki_graph = []
    boruvki_count = 0

    def parse_input(self, graph):
        self._fill_points_fields(graph)
        self._fill_mapper(graph)

    def _fill_points_fields(self, graph):
        for p_str in graph:
            self.free_points += list(p_str['points'])

        self.free_points = list(set(self.free_points))

        self.used_points.append(self.free_points[0])
        del self.free_points[0]

    def _fill_mapper(self, graph):
        for p_str in graph:
            f_p, s_p = p_str['points']
            self.points_mapper[f_p][s_p] = p_str['len']
            self.points_mapper[s_p][f_p] = p_str['len']

    def start(self):
        while self.free_points:
            edge = self.get_new_edge()
            self.make_new_edge(edge)
        
        return self.boruvki_graph


    def edge_len(self, edge):
        return self.points_mapper[edge[0]].get(edge[1], MAX_VAL)

    def get_min_len_from_used_point(self, used_point):
        
        edge = None

        for f_p in self.free_points:
            
            current_edge = (f_p, used_point)
                
            if not edge:
                edge = current_edge
                continue
            
            if self.edge_len(current_edge) < self.edge_len(edge):
                edge = current_edge
        
        return edge


    def get_new_edge(self):
        edge = None

        for u_p in self.used_points:
            
            min_edge = self.get_min_len_from_used_point(u_p) 

            if not edge:
                edge = min_edge
                continue
            
            if self.edge_len(min_edge) < self.edge_len(edge):
                edge = min_edge
        
        return edge
                
    def make_new_edge(self, edge):
        for point in edge:

            if point in self.free_points:
                length = self.edge_len(edge)
                self.free_points.remove(point)
                self.used_points.append(point)
                edge = (edge[0], edge[1], length)
                self.boruvki_graph.append(edge)
                self.boruvki_count += length


if __name__ == '__main__':
    with open('example.json', 'r') as f:
        graph_input = json.load(f)
    
    boruvki = BoruvkiAlgo()
    boruvki.parse_input(graph_input)
    graph = boruvki.start()
    for line in graph:
        print(line)
    print(boruvki.boruvki_count)
