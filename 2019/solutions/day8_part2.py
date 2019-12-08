import sys
import time
from typing import Iterable


def solve(input_iter: Iterable[str], width: int = 25, height: int = 6) -> str:
    line = next(iter(input_iter)).strip()
    bits = list(line)
    bits_per_layer = width * height
    image = [['2' for _ in range(width)] for __ in range(height)]
    for l in range(0, len(bits), bits_per_layer):
        layer_bits = bits[l:l + bits_per_layer]
        for i in range(height):
            for j in range(width):
                if image[i][j] == '2':
                    image[i][j] = layer_bits[(i * width) + j]

    return '\n'.join([''.join(['.' if pixel == '1' else ' ' for pixel in image_row]) for image_row in image])


def run_tests():
    tests = [
        (["0222112222120000"], 2, 2),
    ]

    answers = [
        " .\n. ",
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
