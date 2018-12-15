import itertools
import re
import sys
import time
from typing import Optional


class Node(object):
    def __init__(self, value: int) -> None:
        self.value = value
        self.previous: Optional[Node] = None
        self.next: Optional[Node] = None


class DoublyCircularLinkedList(object):
    def __init__(self):
        self.pointer: Optional[Node] = None

    def skip(self, by: int = 0):
        if self.pointer and self.pointer.previous and self.pointer.next:
            for _ in range(abs(by)):
                self.pointer = self.pointer.next if by > 0 else self.pointer.previous
        return self

    def insert(self, value: int, skip: int = 0):
        self.skip(skip)
        if self.pointer and self.pointer.previous and self.pointer.next:
            new_node = Node(value=value)
            self.pointer.next.previous = new_node
            new_node.previous = self.pointer
            new_node.next = self.pointer.next
            self.pointer.next = new_node
            self.pointer = new_node
        else:
            first_node = Node(value=value)
            first_node.previous = first_node
            first_node.next = first_node
            self.pointer = first_node
        return self

    def pop(self, skip: int = 0) -> Optional[int]:
        self.skip(skip)
        value = None
        if self.pointer and self.pointer.previous and self.pointer.next:
            if self.pointer == self.pointer.previous:
                value = self.pointer.value
                self.pointer = None
            else:
                self.pointer.previous.next = self.pointer.next  # type: ignore
                value = self.pointer.value
                self.pointer = self.pointer.next

        return value


input_pattern = re.compile(r'(\d+) players; last marble is worth (\d+) points')


def solve(input_line: str, special_multiple: int = 23) -> int:
    match = input_pattern.search(input_line.strip())
    if match:
        n_players, m_marbles = [int(m) for m in match.groups()]
        m_marbles *= 100
    else:
        raise ValueError('Invalid Input')

    scores = [0 for _ in range(n_players)]

    circle = DoublyCircularLinkedList()
    circle.insert(value=0)
    for player, marble in zip(itertools.cycle(range(n_players)), range(1, m_marbles + 1)):
        if marble % special_multiple == 0:
            popped = circle.pop(skip=-7)
            if popped is None:
                raise RuntimeError('Circle is empty at marble: {}'.format(marble))
            scores[player] += popped + marble
        else:
            circle.insert(value=marble, skip=1)

    max_score = max(scores)

    return max_score


def run_tests():
    tests = [

    ]

    answers = [

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
