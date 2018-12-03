import collections
import sys


def diff(str1, str2):
    if len(str1) == len(str2):
        return [i for i in range(len(str1)) if str1[i] != str2[i]]
    return []


def solve(input_iter):
    inp = [line.strip() for line in input_iter]
    for i in range(len(inp)):
        for j in range(i):
            positions = diff(inp[i], inp[j])
            if len(positions) == 1:
                return ''.join([c for k, c in enumerate(inp[i]) if k != positions[0]])


def run_tests():
    tests = [
        '''abcde
        fghij
        klmno
        pqrst
        fguij
        axcye
        wvxyz'''.split('\n'),
    ]

    answers = [
        'fgij'
    ]

    for test, answer in zip(tests, answers):
        assert solve(test) == answer, (test, answer)


if __name__ == '__main__':
    run_tests()
    print(solve(sys.stdin))
