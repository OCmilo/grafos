# from graph import Graph
# from os import path

# file_dir = path.dirname(path.abspath(__file__))
# graph = Graph(path.join(file_dir, "../in.txt"))
# graph.report()
# graph.bfs_report("1")
# graph.dfs_report("2")

from weighted_graph import WeightedGraph
from os import path

file_dir = path.dirname(path.abspath(__file__))
graph = WeightedGraph(path.join(file_dir, "../in.txt"))
print(graph.min_distances(5))
