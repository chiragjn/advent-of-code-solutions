import queue
import sys
import time
from typing import Iterable, List, Iterator


class Node(object):
    def __init__(self):
        self.value: int = 0
        self.children: List[Node] = []
        self.metadata: List[int] = []

    def calculate_value(self):
        if not self.children:
            self.value = sum(self.metadata)
        else:
            for entry in self.metadata:
                if entry == 0 or entry > len(self.children):
                    continue
                self.value += self.children[entry - 1].value


class Tree(object):
    def __init__(self, root: Node) -> None:
        self.root = root

    def accumulate_metadata(self) -> Iterable[int]:
        q: queue.Queue = queue.Queue()
        q.put(self.root)
        metadata: List[int] = []
        while not q.empty():
            node = q.get()
            metadata.extend(node.metadata)
            for child_node in node.children:
                q.put(child_node)

        return metadata


def read_node(stream: Iterator[int]) -> Node:
    num_children, num_metadata = next(stream), next(stream)
    node = Node()
    for i in range(num_children):
        node.children.append(read_node(stream))
    for i in range(num_metadata):
        node.metadata.append(next(stream))
    node.calculate_value()
    return node


def solve(input_line: str) -> int:
    numbers: Iterable[int] = map(int, input_line.strip().split())
    tree = Tree(root=read_node(stream=iter(numbers)))
    return tree.root.value


def run_tests():
    tests = [
        '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2',
    ]

    answers = [
        66,
    ]

    for i, (test, answer) in enumerate(zip(tests, answers), start=1):
        print('Running test: {}/{}'.format(i, len(tests)))
        start = time.time()
        computed = solve(test)
        end = time.time()
        assert computed == answer, (test, answer, computed)
        print('OK. Took {:.2f}'.format(end - start))


if __name__ == '__main__':
    run_tests()
    print(solve(sys.stdin.readline()))
