from functools import reduce
from typing import List, Tuple, Union
from sys import maxsize

# Only accepts adjacency matrix
class WeightedGraph:
    def __init__(self, filePath: str) -> None:
        lines = list()
        with open(filePath, "r") as file:
            lines = file.readlines()

        self.graph, self.vertices = self.__matrix(lines)
        self.__has_negative_weights = any(
            weight < 0 for line in self.graph for weight in line
        )

    def mst(self) -> None:
        with open("mst.txt", "w") as file:

            def write_line(text: str = "") -> None:
                file.write(f"{text}\n")

            mst = self.__prims()
            print(mst)
            print(self.graph)

            for i in range(1, self.vertices):
                write_line(f"{mst[i] + 1} {i + 1}")

    def min_distance(self, start: int, end: int) -> float:
        if self.__has_negative_weights:
            distances, _ = self.__bellman_ford(start)
            return distances[end - 1]

        distances, _ = self.__dijkstra(start)
        return distances[end - 1]

    def min_distances(self, start: int) -> List[float]:
        if self.__has_negative_weights:
            distances, _ = self.__bellman_ford(start)
            return distances

        distances, _ = self.__dijkstra(start)
        return distances

    def shortest_path(self, start: int, end: int) -> List[int]:
        path = [end]
        predecessor = None

        if self.__has_negative_weights:
            _, predecessor = self.__bellman_ford(start)
        else:
            _, predecessor = self.__dijkstra(start)

        if predecessor == None:
            return []

        while True:
            next_vertex = predecessor[path[-1] - 1]
            if next_vertex == None:
                break

            path.append(next_vertex)

        path.reverse()

        return path

    def shortest_paths(self, start: int) -> List[List[int]]:
        paths = list()

        if self.__has_negative_weights:
            _, predecessor = self.__bellman_ford(start)
        else:
            _, predecessor = self.__dijkstra(start)

        if predecessor == None:
            return []

        for i in range(1, self.vertices + 1):
            if start == i:
                paths.append([])
                continue

            paths.append([i])
            curr_vertex_path = paths[-1]

            while True:
                next_vertex = predecessor[curr_vertex_path[-1] - 1]
                if next_vertex == None:
                    break

                curr_vertex_path.append(next_vertex)

            curr_vertex_path.reverse()

        return paths

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

    def __dijkstra(self, start: int) -> Tuple[List[float]]:
        distances = [maxsize] * self.vertices
        unvisited = list(range(self.vertices))
        predecessor = [None] * self.vertices
        distances[start - 1] = 0

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
                    predecessor[neighbor] = curr_min_node + 1

            unvisited.remove(curr_min_node)

        return distances, predecessor

    # TODO parar ciclos de 2 vértices
    def __bellman_ford(self, start: int) -> Tuple[List[float], List[int]]:
        distances = [maxsize] * self.vertices
        predecessor = [None] * self.vertices
        distances[start - 1] = 0

        for _ in range(self.vertices - 1):
            for node in range(self.vertices):
                for neighbor in range(self.vertices):
                    if (
                        self.graph[node][neighbor] != 0
                        and (
                            distances[neighbor]
                            > round(distances[node] + self.graph[node][neighbor], 1)
                        )
                        and predecessor[node] != neighbor + 1
                    ):
                        distances[neighbor] = round(
                            distances[node] + self.graph[node][neighbor], 1
                        )
                        predecessor[neighbor] = node + 1

        for node in range(self.vertices):
            for neighbor in range(self.vertices):
                if (
                    self.graph[node][neighbor] != 0
                    and (
                        distances[neighbor]
                        > round(distances[node] + self.graph[node][neighbor], 1)
                    )
                    and predecessor[node] != neighbor + 1
                ):
                    raise NegativeCicleError

        return distances, predecessor

    def __prims(self):
        graph = [
            [maxsize if jx != ix and j == 0 else j for jx, j in enumerate(i)]
            for ix, i in enumerate(self.graph)
        ]
        weight = [maxsize] * self.vertices
        weight[0] = 0
        mst = [None] * self.vertices
        mst[0] = -1
        visited = [False] * self.vertices

        for _ in range(self.vertices):
            minIndex = self.__get_minimum_key(weight, visited)
            visited[minIndex] = True

            for vertex in range(1, self.vertices):
                if (
                    visited[vertex] == False
                    and weight[vertex] > graph[minIndex][vertex]
                ):
                    weight[vertex] = graph[minIndex][vertex]
                    mst[vertex] = minIndex

        return mst

    def __get_minimum_key(self, weight, visited):
        min = maxsize

        for i in range(self.vertices):
            if weight[i] < min and visited[i] == False:
                min = weight[i]
                minIndex = i

        return minIndex

    # TODO remover
    def printMST(self, MST):
        print("Edge \tWeight")
        for i in range(1, self.vertices):
            print(MST[i], "-", i, "\t", self.graph[i][MST[i]])


class NegativeCicleError(Exception):
    pass
