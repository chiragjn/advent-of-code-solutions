"""
Tried doing some functional programming stuff
This runs much slower than I expected. I suck at this :|
"""

import functools

import itertools
import operator


def generate(seed_a, seed_b):
    prev_a, prev_b = seed_a, seed_b
    while True:
        next_a = (16807 * prev_a) % 2147483647
        next_b = (48271 * prev_b) % 2147483647
        yield next_a, next_b
        prev_a, prev_b = next_a, next_b


mask = (2 ** 16) - 1


def compare(a, b):
    return int((a & mask) == (b & mask))


def generate_comparisions(seed_a, seed_b):
    return (compare(a, b)
            for a, b in
            itertools.islice(generate(seed_a, seed_b), 40000000))


def main():
    seed_a = int(input().strip().split()[-1])
    seed_b = int(input().strip().split()[-1])
    print(functools.reduce(
        operator.add,
        generate_comparisions(seed_a, seed_b)
    ))


if __name__ == '__main__':
    main()
