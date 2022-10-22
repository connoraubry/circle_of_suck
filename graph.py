from collections import defaultdict
from itertools import cycle
from logging import Filterer
from pprint import pprint as pp
from unittest import skip 
class Graph():
    def __init__(self, connections=[], directed=False):
        self._graph = defaultdict(set)
        self.directed = directed
        self.add_connections(connections)

    def add_connections(self, connections):
        for node1, node2 in connections:

            self.add(node1, node2)

    def add(self, node1, node2):
        self._graph[node1].add(node2)
        self._graph[node2].update({}) #init if empty
        if not self.directed:
            self._graph[node2].add(node1)

    def find_longest_cycle(self):
        cycles = self.find_all_cycles()
        max_cycle = []
        for c in cycles:
            if len(c) > len(max_cycle):
                max_cycle = c
        return max_cycle


    def find_all_cycles(self):
        list_of_cycles = [] 
        already_in_cycle = set()

        for node in self._graph:
            if node not in already_in_cycle:
                cycle = self.find_longest_cycle_recursive(node, {}, already_in_cycle)
                if len(cycle) > 0:
                    list_of_cycles.append(cycle)
                    already_in_cycle.update(cycle)

        self.cycles = list_of_cycles
        return list_of_cycles

    def find_longest_cycle_recursive(self, node, visited, skip_nodes):
        n = len(visited)
        if node in visited:
            if visited[node] == 0:
                return get_keys(visited, visited[node])
            else:
                return []
        visited[node] = n

        max_cycle = []

        for next_node in self._graph[node]:
            if next_node not in skip_nodes:
                max_cycle_next = self.find_longest_cycle_recursive(next_node, visited, skip_nodes)
                if len(max_cycle_next) > len(max_cycle):
                    max_cycle = max_cycle_next

        del visited[node]
        return max_cycle

def get_keys(visited, min_val):
    filtered = {k: v for k, v in visited.items() if v >= min_val}
    return [x[0] for x in sorted(filtered.items(), key= lambda value: value[1])]
