from aocd.models import Puzzle
from collections import defaultdict

import networkx as nx
import numpy as np

START, END = 'start', 'end'


def part_a(g: nx.classes.graph.Graph):
    paths = [[]]
    find_all_paths(g, START, defaultdict(lambda: 0), paths)

    # Filter out invalid paths
    paths = [path for path in paths if END in path]

    return len(paths)


def part_b(g: nx.classes.graph.Graph):
    paths = [[]]
    small_caves = [node for node in g.nodes if not node in (START, END) and node.islower()]
    for sc in small_caves:
        g.nodes[sc]['visit'] = 2
        find_all_paths(g, START, defaultdict(lambda: 0), paths)
        g.nodes[sc]['visit'] = 1

    # Filter out invalid paths
    paths = [path for path in paths if END in path]

    # Filter out duplicate paths
    paths = set([tuple(path) for path in paths])

    return len(paths)


# Recursive backtracking algorithm
def find_all_paths(g, cur: str, visited: dict, paths: list, depth=0):
    # Return when node is visited maximum allowed times
    if visited[cur] == g.nodes[cur]['visit']:
        return
    visited[cur] += 1

    # Branch out a new path when backtracked to already used position
    if len(paths[-1]) > depth:
        paths.append(paths[-1][:depth])
    paths[-1].append(cur)

    if cur == END:
        return

    for _, nxt in g.edges(cur):
        find_all_paths(g, nxt, visited, paths, depth + 1)

    # BACKTRACK: Decrease visit count when backtracking
    visited[cur] -= 1


def load(data: str):
    g = nx.Graph()
    nodes = {node for line in data.splitlines() for node in line.split('-')}
    for node in nodes:
        g.add_node(node, visit=1 if node.islower() else np.inf)
    g.nodes[END]['visit'] = np.inf
    g.add_edges_from([line.split('-') for line in data.splitlines()])
    return g


puzzle = Puzzle(year=2021, day=12)
ans_a = part_a(load(puzzle.input_data))
# puzzle.answer_a = ans_a  # 3563
ans_b = part_b(load(puzzle.input_data))
print(ans_b)
# puzzle.answer_b = ans_b  # 105453
