import re
import sys

FABRIC_SIZE = 1000
pattern = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')


def solve(input_iter):
    fabric = [[0 for __ in range(FABRIC_SIZE)] for _ in range(FABRIC_SIZE)]
    for line in input_iter:
        line = line.strip()
        claim_id, left_offset, top_offset, width, height = list(map(int, pattern.search(line.strip()).groups()))
        for i in range(left_offset, left_offset + width):
            for j in range(top_offset, top_offset + height):
                fabric[i][j] += 1

    answer = 0
    for i in range(FABRIC_SIZE):
        for j in range(FABRIC_SIZE):
            if fabric[i][j] > 1:
                answer += 1
    return answer


def run_tests():
    tests = [
        '''#1 @ 1,3: 4x4
        #2 @ 3,1: 4x4
        #3 @ 5,5: 2x2'''.split('\n')
    ]

    answers = [
        4
    ]

    for test, answer in zip(tests, answers):
        assert solve(test) == answer, (test, answer)


if __name__ == '__main__':
    run_tests()
    print(solve(sys.stdin))
