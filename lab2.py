from collections import Counter

test_data = [
    'ab',
    'ea',
    'cf',
    'fg',
    'bc',
    'cd',
    'de',
    'gh',
    'hc',
]


class EylerAlgo():
    free_edges = []
    included_points = []
    existed_points = []
    eiler_cycle_path = []
    cycles = []

    def __init__(self, graph_data):
        self.check_if_eyler_cycle_exists(graph_data)
        self.free_edges = graph_data
        self.existed_points = [i for i in ''.join(graph_data)]
        self.existed_points = list(set(self.existed_points))        

    def check_if_eyler_cycle_exists(self, graph_data):
        all_points_in_edges = [i for i in ''.join(graph_data)]
        counts_points_edges = Counter(all_points_in_edges)
        for point, counts in counts_points_edges.items():
            if counts % 2 != 0:
                msg = 'This point {} is not pair '.format(point)
                in_edges = [edge for edge in graph_data if point in edge]
                msg += 'Used in such edges {}'.format(in_edges)
                raise Exception(msg)
            
    def build_eyler_cycle(self):
        while self.free_edges:
            self._build_inner_cycle()
        cycle = self.merge_cycles(self.cycles)
        return cycle

    def _is_point_has_free_edges(self, point):
        edges = [edge for edge in self.free_edges if point in edge]
        return len(edges)

    def _build_inner_cycle(self):
        current_point = self.existed_points[0]
        cycle = [current_point]

        while self.free_edges:
            edge = self.get_free_edge(current_point)
            point_of_edge_end = edge.replace(current_point, '')
            cycle.append(point_of_edge_end)
            self.free_edges.remove(edge)
        
            if not self._is_point_has_free_edges(current_point):
                self.existed_points.remove(current_point)
        
            if point_of_edge_end == cycle[0]:
                self.cycles.append(cycle)    
                return
        
            current_point = point_of_edge_end

    def get_free_edge(self, current_point):
        allowed_edges = [edge for edge in self.free_edges if current_point in edge]
        return allowed_edges[0]
    
    def merge_cycles(self, cycles):
        # print(cycles)
        # print()
        while len(cycles) > 1:
            last_cycle = cycles[-1]
            pre_last_cycle = cycles[-2]
            del cycles[-1]
            cycles[-1] = self.merge_two_cycle(pre_last_cycle, last_cycle)
        return cycles[0]

    def merge_two_cycle(self, pre_last_cycle, last_cycle):
        point = list(set(pre_last_cycle) & set(last_cycle))[0]
        last_cycle = self.shift_cycle_to_point(point, last_cycle)
        string_pre_last = ''.join(pre_last_cycle)
        string_last = ''.join(last_cycle)
        merged_cycle = string_pre_last.replace(point, string_last, 1)
        merged_cycle = [i for i in merged_cycle]
        return merged_cycle

    def shift_cycle_to_point(self, point, cycle):
        new_cycle = cycle[:-1]
        shift_value = new_cycle.index(point)
        new_cycle = new_cycle[shift_value:] + new_cycle[:shift_value]
        new_cycle.append(point)
        return new_cycle

if __name__ == '__main__':
    eyler = EylerAlgo(test_data)
    eyler_cycle = eyler.build_eyler_cycle()
    print()
    print('->'.join(eyler_cycle))
    print()