import functools
import sys
import time
from typing import Iterable, List, Sequence

def csums(data: Sequence[int]) -> List[int]:
    sum_so_far = 0
    csums_ = []
    for item in data:
        sum_so_far += item
        csums_.append(sum_so_far)
    csums_.append(0)
    return csums_


def apply_filter(degree: int, cumulative_sums: Sequence[int]) -> int:
    if degree == 0:
        return 0
    N = len(cumulative_sums) - 1
    jump = 4 * degree
    pos_start = degree
    neg_start = 3 * degree
    answer = 0

    while pos_start < N and neg_start < N:
        pos_end = min(pos_start + degree - 1, N - 1)
        answer += cumulative_sums[pos_end] - cumulative_sums[pos_start - 1]
        pos_start += jump
        neg_end = min(neg_start + degree - 1, N - 1)
        answer -= cumulative_sums[neg_end] - cumulative_sums[neg_start - 1]
        neg_start += jump

    while pos_start < N:
        pos_end = min(pos_start + degree - 1, N - 1)
        answer += cumulative_sums[pos_end] - cumulative_sums[pos_start - 1]
        pos_start += jump

    while neg_start < N:
        neg_end = min(neg_start + degree - 1, N - 1)
        answer -= cumulative_sums[neg_end] - cumulative_sums[neg_start - 1]
        neg_start += jump
    return abs(answer) % 10


def convolve(digits: str, times: int) -> str:
    digits = (0,) + tuple(int(digit) for digit in digits)
    print(len(digits))
    params = tuple(range(len(digits)))
    for _ in range(times):
        cumulative_sums = tuple(csums(digits))
        fn = functools.partial(apply_filter, cumulative_sums=cumulative_sums)
        # with concurrent.futures.ProcessPoolExecutor(max_workers=None) as executor:
        #     digits = tuple(executor.map(fn, params))
        digits = [fn(j) for j in params]
    result = ''.join([str(digit) for digit in digits[1:]])
    return result


def solve(input_iter: Iterable[str]) -> str:
    line = next(iter(input_iter))
    line = line.strip()
    multiplier = 10000
    offset = int(line[:7])
    line = line * multiplier
    convolved = convolve(line, times=100)
    return convolved[offset:offset + 8]


def run_tests():
    tests = [
        ['03036732577212944063491565474664'],
        ['02935109699940807407585447034323'],
        ['03081770884921959731165446850517'],
    ]

    answers = [
        '84462026',
        '78725270',
        '53553731',
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
