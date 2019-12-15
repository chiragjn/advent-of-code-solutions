import collections
import queue
import sys
import time
from typing import Iterable, Dict, Tuple, List, Set


class Chemical(object):
    def __init__(self, name: str, quantity: int):
        self.name = name
        self.quantity = quantity
        self.topological_rank: int = 0
        self.made_from: List[Tuple['Chemical', int]] = []

    def requires_dict(self, desired_quantity: int = 1) -> Dict[str, int]:
        multiplier = (desired_quantity // self.quantity)
        if desired_quantity % self.quantity != 0:
            multiplier += 1
        requires = {reactant.name: (quantity * multiplier) for reactant, quantity in self.made_from}
        return requires


def topological_sort(graph: Dict[str, Chemical]) -> None:
    makes_graph: Dict[str, Set[str]] = collections.defaultdict(set)
    for chemical in graph.values():
        for reactant, _ in chemical.made_from:
            makes_graph[reactant.name].add(chemical.name)

    q = queue.Queue()
    chemical_in_degrees: Dict[str, int] = {}
    for chemical in graph.values():
        if not chemical.made_from:
            q.put(chemical.name)
        else:
            chemical_in_degrees[chemical.name] = len(chemical.made_from)

    topologically_sorted = []
    while not q.empty():
        chemical_name = q.get()
        topologically_sorted.append(chemical_name)
        for reactant_name in makes_graph[chemical_name]:
            chemical_in_degrees[reactant_name] -= 1
            if chemical_in_degrees[reactant_name] == 0:
                chemical_in_degrees.pop(reactant_name)
                q.put(reactant_name)
    for i, chemical_name in enumerate(topologically_sorted):
        graph[chemical_name].topological_rank = i


def ore_required(graph: Dict[str, Chemical], name: str, desired_quantity: int = 1) -> int:
    required: Dict[str, int] = collections.defaultdict(int)
    required[name] += desired_quantity
    while list(required.keys()) != ['ORE']:
        next_chemical = max(list(required.keys()), key=lambda cname: graph[cname].topological_rank)
        next_chemical_quantity = required.pop(next_chemical)
        next_chemical_requires = graph[next_chemical].requires_dict(desired_quantity=next_chemical_quantity)
        for chemical_name, quantity in next_chemical_requires.items():
            required[chemical_name] += quantity
    return required['ORE']


def solve(input_iter: Iterable[str]) -> int:
    graph: Dict[str, Chemical] = {}
    for line in input_iter:
        line = line.strip()
        line = line.replace(' => ', ', ')
        parts = []
        for part in line.strip().split(', '):
            quantity, chemical = part.split(' ')
            quantity = int(quantity)
            parts.append((chemical, quantity))
        product_name, product_quantity = parts[-1]
        if product_name not in graph:
            graph[product_name] = Chemical(name=product_name, quantity=product_quantity)
        graph[product_name].quantity = product_quantity
        for reactant_name, reactant_quantity in parts[:-1]:
            if reactant_name not in graph:
                graph[reactant_name] = Chemical(name=reactant_name, quantity=-1)
            graph[product_name].made_from.append((graph[reactant_name], reactant_quantity))
    assert all(chemical.quantity > 0 for chemical in graph.values() if chemical.name != 'ORE')
    topological_sort(graph)
    return ore_required(graph=graph, name='FUEL', desired_quantity=1)


def run_tests():
    tests = [
        """9 ORE => 2 A
        8 ORE => 3 B
        7 ORE => 5 C
        3 A, 4 B => 1 AB
        5 B, 7 C => 1 BC
        4 C, 1 A => 1 CA
        2 AB, 3 BC, 4 CA => 1 FUEL""".split('\n'),

        """157 ORE => 5 NZVS
        165 ORE => 6 DCFZ
        44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
        12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
        179 ORE => 7 PSHF
        177 ORE => 5 HKGWZ
        7 DCFZ, 7 PSHF => 2 XJWVT
        165 ORE => 2 GPVTF
        3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT""".split('\n'),

        """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
        17 NVRVD, 3 JNWZP => 8 VPVL
        53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
        22 VJHF, 37 MNCFX => 5 FWMGM
        139 ORE => 4 NVRVD
        144 ORE => 7 JNWZP
        5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
        5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
        145 ORE => 6 MNCFX
        1 NVRVD => 8 CXFTF
        1 VJHF, 6 MNCFX => 4 RFSQX
        176 ORE => 6 VJHF""".split('\n'),

        """171 ORE => 8 CNZTR
        7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
        114 ORE => 4 BHXH
        14 VRPVC => 6 BMBT
        6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
        6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
        15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
        13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
        5 BMBT => 4 WPTQ
        189 ORE => 9 KTJDG
        1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
        12 VRPVC, 27 CNZTR => 2 XDBXC
        15 KTJDG, 12 BHXH => 5 XCVML
        3 BHXH, 2 VRPVC => 7 MZWV
        121 ORE => 7 VRPVC
        7 XCVML => 6 RJRHP
        5 BHXH, 4 VRPVC => 5 LTCX""".split('\n'),

    ]

    answers = [
        165,
        13312,
        180697,
        2210736,
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
