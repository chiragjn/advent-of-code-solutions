import itertools
import sys
import time
from typing import Iterable, Any, List, Iterator, Tuple


class Moon(object):
    def __init__(self, coords: List[int]):
        self.coords = coords
        self.velocity = [0 for _ in coords]

    def step(self) -> None:
        self.coords = [coord + velocity for coord, velocity in zip(self.coords, self.velocity)]

    def adjust_velocity(self, other_moon: 'Moon') -> None:
        for i in range(len(self.coords)):
            if self.coords[i] > other_moon.coords[i]:
                self.velocity[i] -= 1
                other_moon.velocity[i] += 1
            elif self.coords[i] < other_moon.coords[i]:
                self.velocity[i] += 1
                other_moon.velocity[i] -= 1


class MoonSystem(object):
    def __init__(self, moons: List[Moon]) -> None:
        self.moons = moons

    def step(self, num_steps: int = 1) -> 'MoonSystem':
        for i in range(num_steps):
            pairs: Iterator[Tuple[Moon, ...]] = itertools.combinations(self.moons, r=2)
            for (moon1, moon2) in pairs:
                moon1.adjust_velocity(moon2)
            for moon in self.moons:
                moon.step()
        return self

    @property
    def energy(self) -> int:
        answer = 0
        for moon in self.moons:
            answer += sum(abs(x) for x in moon.coords) * sum(abs(x) for x in moon.velocity)
        return answer


def solve(input_iter: Iterable[str], num_steps: int = 1000) -> int:
    moons = []
    for line in input_iter:
        coords = line.strip().strip('<>').split(', ')
        coords = [int(coord.split('=')[1]) for coord in coords]
        moons.append(Moon(coords))
    return MoonSystem(moons=moons).step(num_steps=num_steps).energy


def run_tests():
    tests = [
        (["<x=-1, y=0, z=2>", "<x=2, y=-10, z=-7>", "<x=4, y=-8, z=8>", "<x=3, y=5, z=-1>"], 10),
        (["<x=-8, y=-10, z=0>", "<x=5, y=5, z=10>", "<x=2, y=-7, z=3>", "<x=9, y=-8, z=-3>"], 100)
    ]

    answers = [
        179,
        1940,
    ]

    for i, (test, answer) in enumerate(zip(tests, answers), start=1):
        print('Running test: {}/{}'.format(i, len(tests)))
        start = time.time()
        computed = solve(*test)
        end = time.time()
        assert computed == answer, (test, answer, computed)
        print('OK. Took {:.2f}'.format(end - start))


if __name__ == '__main__':
    run_tests()
    print(solve(sys.stdin))
