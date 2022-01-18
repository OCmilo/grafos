from statistics import mean, median
from collections import defaultdict, deque
from itertools import combinations
from io import TextIOWrapper
from typing import List, Union, DefaultDict, Set, Tuple, Callable


class Graph:
    def __init__(self, filePath: str, matrix: bool = False) -> None:
        lines = list()
        with open(filePath, "r") as file:
            lines = file.readlines()

        self.matrix = matrix
        self.graph = defaultdict(set)
        self.number_of_edges = len(lines[1:])
        self.__add_edges(lines[1:])
        self.__get_degrees()

        if matrix:
            self.convert_to_matrix()

    def convert_to_matrix(self) -> None:
        vertices = len(self.graph)
        ordered_keys = list(self.graph.keys())
        ordered_keys.sort(key=lambda key: int(key))

        matrix = [[0 for j in range(vertices)] for i in range(vertices)]

        for idx, vertice in enumerate(ordered_keys):
            for edge in self.graph[vertice]:
                matrix[idx][int(edge) - 1] = 1

        self.matrix_graph = matrix

    def report(self) -> None:
        with open("out.txt", "w") as file:
            components = self.connected_components()

            def write_line(text: str = "") -> None:
                file.write(f"{text}\n")

            if not self.matrix:
                for vertice in self.graph:
                    file.write(vertice + " ")

                    for edge in self.graph[vertice]:
                        file.write(" --> " + edge)

                    write_line()
            else:
                for i in range(len(self.matrix_graph)):
                    for j in range(len(self.matrix_graph)):
                        file.write(str(self.matrix_graph[i][j]) + " ")
                    write_line()

            write_line()

            write_line(f"Number of vertices: {len(self.graph)}")
            write_line(f"Number of edges: {self.number_of_edges}")
            write_line(f"Minimum degree: {self.min_degree}")
            write_line(f"Maximum degree: {self.max_degree}")
            write_line(f"Medium degree: {self.med_degree}")
            write_line(f"Median degree: {self.median_degree}")
            write_line(f"Number of Connected Components: {len(components)}")

            for idx, component in enumerate(components):
                write_line(
                    f"Component {idx+1} - Length: {len(component)}, Vertices: {component}"
                )

    def bfs_report(self, starting_node: str):
        self.spanning_tree(starting_node, algorithm=self.bfs)

    def dfs_report(self, starting_node: str):
        self.spanning_tree(starting_node, algorithm=self.dfs)

    def spanning_tree(self, starting_node: str, algorithm: Callable) -> str:
        tree, _ = algorithm(starting_node, tree=True)

        with open(f"{algorithm.__name__}.txt", "w") as file:
            level = 1
            file.write(f"Level 0: {starting_node}\n")
            self.__spanning_tree_helper(tree, starting_node, level, file)

    def bfs(
        self, starting_node: str, tree: bool = False
    ) -> Union[List[str], Tuple[DefaultDict[str, Set[str]], str]]:

        visited_nodes = list(starting_node)
        queue = deque([starting_node])
        tree_struct = defaultdict(set)

        while queue:
            node = queue.popleft()
            for edge in self.graph[node]:
                if edge not in visited_nodes:
                    visited_nodes.append(edge)
                    queue.append(edge)
                    tree_struct[node].add(edge)

        return (tree_struct, starting_node) if tree else visited_nodes

    def dfs(
        self, starting_node: str, tree: bool = False
    ) -> Union[List[str], Tuple[DefaultDict[str, Set[str]], str]]:
        visited = list()
        tree_struct = defaultdict(set)
        self.__dfs_helper(visited, starting_node, tree_struct, starting_node)

        return (tree_struct, starting_node) if tree else visited

    def shortest_path(self, start: str, goal: str) -> List[None]:
        explored = []
        queue = deque([[start]])

        if start == goal:
            return [start]

        while queue:
            path = queue.popleft()
            node = path[-1]

            if node not in explored:
                neighbors = self.graph[node]
                for neighbor in neighbors:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)

                    if neighbor == goal:
                        return new_path

                explored.append(node)

        return []

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

    def diameter(self) -> int:
        max_shortest_path = 0
        for vert1, vert2 in combinations(self.graph.keys(), 2):
            path_size = len(self.shortest_path(vert1, vert2))
            if path_size > max_shortest_path:
                max_shortest_path = path_size

        return max_shortest_path

    def __spanning_tree_helper(
        self,
        tree: DefaultDict[str, Set[str]],
        node: str,
        level: int,
        file: TextIOWrapper,
    ):
        if len(tree[node]) == 0:
            return

        file.write(f"Level {level}, Father {node}: ")

        for child in tree[node]:
            file.write(f"{child} ")

        file.write("\n")
        level += 1

        for child in tree[node]:
            self.__spanning_tree_helper(tree, child, level, file)

    def __dfs_helper(
        self,
        visited_list: List[str],
        node: str,
        tree: DefaultDict[str, Set[str]],
        father: str,
    ) -> List[str]:
        if node not in visited_list:
            ordered_neighbors = list(self.graph[node])
            ordered_neighbors.sort(key=lambda vertice: int(vertice))

            visited_list.append(node)
            if father != node:
                tree[father].add(node)
            for neighbor in ordered_neighbors:
                self.__dfs_helper(visited_list, neighbor, tree, node)

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
