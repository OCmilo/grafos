from functools import reduce
from typing import List, Tuple, Dict
from sys import maxsize

# Only accepts adjacency matrix
class WeightedGraph:
    def __init__(self, filePath: str) -> None:
        lines = list()
        with open(filePath, "r") as file:
            lines = file.readlines()

        self.graph, self.vertices = self.__matrix(lines)
        self.distances = self.__floyd_warshall()

    def __matrix(self, edge_strings: List[str]) -> Tuple[List[List[float]], int]:
        vertices = int(edge_strings.pop(0).strip())
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

    def __dijkstra(self, starting_vertice: int) -> Tuple[List[float]]:
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
                    distances[neighbor] = round(testing_value, 1)
                    path[neighbor + 1] = curr_min_node + 1

            unvisited.remove(curr_min_node)

        return path, distances

    # TODO verificar porque dá erro com pesos negativos
    def __floyd_warshall(self) -> List[List[float]]:
        distances = [
            [maxsize if jx != ix and j == 0 else j for jx, j in enumerate(i)]
            for ix, i in enumerate(self.graph)
        ]

        for k in range(self.vertices):
            for i in range(self.vertices):
                for j in range(self.vertices):
                    distances[i][j] = round(
                        min(distances[i][j], distances[i][k] + distances[k][j]), 1
                    )
                    # if i == j and distances[i][j] < 0:
                    #     distances = None
                    #     return distances

        return distances

    def bellman_ford(self, node: int) -> List[float]:
        distances = [maxsize] * self.vertices
        distances[node - 1] = 0

        for _ in range(self.vertices - 1):
            for node in range(self.vertices):
                for neighbor in range(self.vertices):
                    if (
                        self.graph[node][neighbor] != 0
                        and distances[neighbor]
                        > distances[node] + self.graph[node][neighbor]
                    ):
                        distances[neighbor] = round(
                            distances[node] + self.graph[node][neighbor], 1
                        )

        for i in range(self.vertices):
            if distances[i][i] < 0:
                return None

        return distances
