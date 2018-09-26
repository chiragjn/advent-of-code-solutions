"""
Tried doing some functional programming stuff
This runs much slower than I expected. I suck at this :|
"""

import functools

import itertools
import operator


def generate(seed, multiplier, mod, must_be_mutiple_of):
    prev = seed
    while True:
        next_v = (multiplier * prev) % mod
        if next_v % must_be_mutiple_of == 0:
            yield next_v
        prev = next_v


def generate_pairs(seed_a, seed_b):
    return zip(generate(seed_a, 16807, 2147483647, 4),
               generate(seed_b, 48271, 2147483647, 8))


mask = (2 ** 16) - 1


def compare(a, b):
    return int((a & mask) == (b & mask))


def generate_comparisions(seed_a, seed_b):
    return (compare(a, b)
            for a, b in
            itertools.islice(generate_pairs(seed_a, seed_b), 5000000))


def main():
    seed_a = int(input().strip().split()[-1])
    seed_b = int(input().strip().split()[-1])
    print(functools.reduce(
        operator.add,
        generate_comparisions(seed_a, seed_b)
    ))


if __name__ == '__main__':
    main()
