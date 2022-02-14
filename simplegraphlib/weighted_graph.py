from functools import reduce
from typing import List
from sys import maxsize

# Only accepts adjacency matrix
class WeightedGraph:
    def __init__(self, filePath: str) -> None:
        lines = list()
        with open(filePath, "r") as file:
            lines = file.readlines()

        self.graph, self.vertices = self.__matrix(lines)

        print(self.graph)

    def __matrix(self, edge_strings: List[str]) -> List:
        vertices = int(edge_strings.pop(0).strip())
        print(vertices)
        matrix = [[0 for _ in range(vertices)] for _ in range(vertices)]

        for edge_string in edge_strings:
            edge_list = edge_string.strip().split(" ")
            vert1, vert2, weight = (
                int(edge_list[0]) - 1,
                int(edge_list[1]) - 1,
                float(edge_list[2]),
            )
            matrix[vert1][vert2] = weight
            matrix[vert2][vert1] = weight

        return (matrix, vertices)

    def dijkstra(self, starting_vertice: int) -> List[float]:
        distances = [maxsize] * self.vertices
        unvisited = list(range(self.vertices))
        path = dict()
        distances[starting_vertice - 1] = 0

        while unvisited:
            curr_min_node = None

            for node in unvisited:
                if curr_min_node == None or distances[node] < distances[curr_min_node]:
                    curr_min_node = node

            neighbors = list()
            for index, node in enumerate(self.graph[curr_min_node]):
                if node > 0:
                    neighbors.append(index)

            for neighbor in neighbors:
                testing_value = (
                    distances[curr_min_node] + self.graph[curr_min_node][neighbor]
                )

                if testing_value < distances[neighbor]:
                    distances[neighbor] = testing_value
                    path[neighbor + 1] = curr_min_node + 1

            unvisited.remove(curr_min_node)

        return path, distances
