from statistics import mean, median
from typing import List, Tuple
from collections import defaultdict, deque
from itertools import combinations


class Graph:
    def __init__(self, filePath: str) -> None:
        lines = list()
        with open(filePath, "r") as file:
            lines = file.readlines()

        self.graph = defaultdict(set)
        self.number_of_edges = len(lines[1:])
        self.__add_edges(lines[1:])
        self.__get_degrees()

    def report(self) -> None:
        with open("out.txt", "w") as file:
            components = self.connected_components()

            def write_line(text: str) -> None:
                file.write(f"{text}\n")

            write_line(f"Number of vertices: {len(self.graph)}")
            write_line(f"Number of edges: {self.number_of_edges}")
            write_line(f"Minimum degree: {self.min_degree}")
            write_line(f"Maximun degree: {self.max_degree}")
            write_line(f"Medium degree: {self.med_degree}")
            write_line(f"Median degree: {self.median_degree}")
            write_line(f"Number of Connected Components: {len(components)}")

            for idx, component in enumerate(components):
                write_line(
                    f"Component {idx+1} - Length: {len(component)}, Vertices: {component}"
                )

    def bfs(self, starting_node: str) -> List[str]:
        visited_nodes = [starting_node]
        queue = deque([starting_node])

        while queue:
            node = queue.popleft()
            for edge in self.graph[node]:
                if edge not in visited_nodes:
                    visited_nodes.append(edge)
                    queue.append(edge)

        return visited_nodes

    def connected_components(self) -> List[List[str]]:
        visited = list()
        connected_vertices = []

        for vertice in self.graph:
            if vertice not in visited:
                dfs = self.dfs(vertice)

                visited.extend(dfs)
                connected_vertices.append(dfs)

        connected_vertices.sort(key=lambda component: len(component), reverse=True)

        return connected_vertices

    def dfs(self, starting_node: str):
        visited = list()
        self.__dfs_helper(visited, starting_node)

        return visited

    def shortest_path(self, start: str, goal: str) -> List[None]:
        explored = []
        queue = deque([[start]])

        if start == goal:
            return [start]

        while queue:
            path = queue.popleft()
            node = path[-1]

            if node not in explored:
                neighbours = self.graph[node]
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)

                    if neighbour == goal:
                        return new_path

                explored.append(node)

        return []

    def diameter(self) -> int:
        shortest_paths = list()
        for vert1, vert2 in combinations(self.graph.keys(), 2):
            shortest_paths.append(len(self.shortest_path(vert1, vert2)))

        return max(shortest_paths)

    def __dfs_helper(self, visited_list: List[str], node: str) -> List[str]:
        if node not in visited_list:
            visited_list.append(node)
            for neighbor in self.graph[node]:
                self.__dfs_helper(visited_list, neighbor)

    def __get_degrees(self) -> int:
        list_of_degrees = []
        for edges in self.graph.values():
            list_of_degrees.append(len(edges))

        list_of_degrees.sort()

        self.min_degree = list_of_degrees[0]
        self.max_degree = list_of_degrees[-1]
        self.med_degree = mean(list_of_degrees)
        self.median_degree = median(list_of_degrees)

    def __add_edges(self, edge_strings: List[str]) -> None:
        for edge_string in edge_strings:
            vert1, vert2 = tuple(edge_string.strip().split(" "))
            self.graph[vert1].add(vert2)
            self.graph[vert2].add(vert1)

    def __len__(self) -> int:
        return len(self.graph)

    def __getitem__(self, item) -> set:
        return self.graph[item]
