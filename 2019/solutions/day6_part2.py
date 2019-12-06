import sys
import time
from typing import Iterable, Optional, List, Dict


class Entity(object):
    def __init__(self, name: str):
        self.name = name
        self.parent: Optional[Entity] = None
        self.level: int = 0
        self.orbited_by: List[Entity] = []


def set_levels(entity: Entity, level: int = 0) -> None:
    entity.level = level
    for child_entity in entity.orbited_by:
        set_levels(entity=child_entity, level=entity.level + 1)


def path_from_root(entity: Entity) -> List[str]:
    this = entity
    path = []
    while this is not None:
        path.append(this.name)
        this = this.parent
    path.reverse()
    return path


def solve(input_iter: Iterable[str]) -> int:
    tree: Dict[str, Entity] = {}

    for line in input_iter:
        line = line.strip()
        parent, child = line.split(')')
        if parent not in tree:
            tree[parent] = Entity(name=parent)
        if child not in tree:
            tree[child] = Entity(name=child)

        tree[child].parent = tree[parent]
        tree[parent].orbited_by.append(tree[child])

    set_levels(tree['COM'])
    you_path = path_from_root(entity=tree['YOU'])
    san_path = path_from_root(entity=tree['SAN'])
    answer = -2
    while you_path[-1] != san_path[-1]:
        if len(you_path) == len(san_path):
            answer += 2
            you_path.pop()
            san_path.pop()
        elif len(you_path) > len(san_path):
            answer += 1
            you_path.pop()
        else:
            answer += 1
            san_path.pop()
    return answer


def run_tests():
    tests = [
        'COM)B,B)C,C)D,D)E,E)F,B)G,G)H,D)I,E)J,J)K,K)L,K)YOU,I)SAN'.strip().split(','),
    ]

    answers = [
        4,
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
    print(solve(sys.stdin))
