import itertools
import sys
import time
from typing import Iterable, Iterator


def make_iter(times) -> Iterator[int]:
    it = itertools.cycle(itertools.chain.from_iterable([itertools.repeat(i, times) for i in (0, 1, 0, -1)]))
    next(it)
    return it


def convolve(digits: str, times: int) -> str:
    digits = [int(digit) for digit in digits]
    for i in range(1, times + 1):
        digits = [(abs(sum((m * digit) for m, digit in zip(make_iter(j), digits))) % 10)
                  for j in range(1, len(digits) + 1)]
    return ''.join([str(digit) for digit in digits])


def solve(input_iter: Iterable[str]) -> str:
    line = next(iter(input_iter))
    line = line.strip()
    return convolve(line, times=100)[:8]


def run_tests():
    tests = [
        ['80871224585914546619083218645595'],
        ['19617804207202209144916044189917'],
        ['69317163492948606335995924319873'],
    ]

    answers = [
        '24176176',
        '73745418',
        '52432133',
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
