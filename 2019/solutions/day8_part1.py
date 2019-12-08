import sys
import time
from typing import Iterable


def solve(input_iter: Iterable[str], width: int = 25, height: int = 6) -> int:
    line = next(iter(input_iter)).strip()
    bits = [int(bit) for bit in list(line)]
    bits_per_layer = width * height
    min_num_zeros = bits_per_layer + 1
    answer = -1
    for i in range(0, len(bits), bits_per_layer):
        layer_bits = bits[i:i + bits_per_layer]
        num_zeros = layer_bits.count(0)
        if num_zeros < min_num_zeros:
            min_num_zeros = num_zeros
            answer = layer_bits.count(1) * layer_bits.count(2)
    return answer


def run_tests():
    tests = [
        (["123456789012"], 3, 2),
    ]

    answers = [
        1,
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
