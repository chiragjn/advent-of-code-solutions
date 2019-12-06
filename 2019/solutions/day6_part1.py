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

    set_levels(tree["COM"])
    answer = 0
    for entity_name, entity in tree.items():
        answer += entity.level
    return answer


def run_tests():
    tests = [
        'COM)B,B)C,C)D,D)E,E)F,B)G,G)H,D)I,E)J,J)K,K)L'.split(','),
    ]

    answers = [
        42,
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
