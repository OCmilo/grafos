from lib import Graph
from os import path

file_dir = path.dirname(path.abspath(__file__))
graph = Graph(path.join(file_dir, "../in.txt"), matrix=True)
print(graph.bfs_report("2"))
