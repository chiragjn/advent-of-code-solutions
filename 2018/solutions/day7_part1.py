import collections
import queue
import re
import sys
from typing import Iterable, Dict, Set, List, Union

input_pattern = re.compile(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin.')


class Graph(object):
    def __init__(self):
        self.data: Dict[str, Set[str]] = collections.defaultdict(set)
        self.vertices = set()

    def add_edge(self, first: str, second: str):
        self.vertices.add(first)
        self.vertices.add(second)
        self.data[first].add(second)

    def topological_order(self) -> Iterable[str]:
        q: queue.PriorityQueue[str] = queue.PriorityQueue()
        in_degree: Dict[str, int] = {v: 0 for v in self.vertices}
        for i in self.data:
            for j in self.data[i]:
                in_degree[j] += 1

        for v in self.vertices:
            if not in_degree[v]:
                q.put(v)

        order: List[str] = []
        while not q.empty():
            u = q.get()
            order.append(u)
            for v in self.data[u]:
                in_degree[v] -= 1
                if not in_degree[v]:
                    q.put(v)

        return order


def solve(input_iter: Iterable[str]) -> str:
    graph = Graph()
    for line in input_iter:
        line = line.strip()
        match = input_pattern.search(line)
        if match:
            first, second = match.group(1), match.group(2)
            graph.add_edge(first=first, second=second)
        else:
            raise ValueError('Invalid input')

    return ''.join(graph.topological_order())


def run_tests():
    tests = [
        '''Step C must be finished before step A can begin.
        Step C must be finished before step F can begin.
        Step A must be finished before step B can begin.
        Step A must be finished before step D can begin.
        Step B must be finished before step E can begin.
        Step D must be finished before step E can begin.
        Step F must be finished before step E can begin.'''.split('\n'),

        '''Step A must be finished before step C can begin.
        Step C must be finished before step D can begin.
        Step B must be finished before step D can begin.'''.split('\n'),
    ]

    answers = [
        'CABDFE',
        'ABCD'
    ]

    for test, answer in zip(tests, answers):
        computed = solve(test)
        assert computed == answer, (test, answer, computed)


if __name__ == '__main__':
    run_tests()
    print(solve(sys.stdin))
