import re
import sys

FABRIC_SIZE = 1000
pattern = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')


def solve(input_iter):
    claims = {}
    fabric = [[[0, None] for __ in range(FABRIC_SIZE)] for _ in range(FABRIC_SIZE)]
    for line in input_iter:
        line = line.strip()
        claim_id, left_offset, top_offset, width, height = list(map(int, pattern.search(line.strip()).groups()))
        claims[claim_id] = True
        for i in range(left_offset, left_offset + width):
            for j in range(top_offset, top_offset + height):
                fabric[i][j][0] += 1
                if fabric[i][j][1] is not None:
                    claims[fabric[i][j][1]] = False
                    claims[claim_id] = False
                fabric[i][j][1] = claim_id

    for claim_id in claims:
        if claims[claim_id]:
            return claim_id

    return -1


def run_tests():
    tests = [
        '''#1 @ 1,3: 4x4
        #2 @ 3,1: 4x4
        #3 @ 5,5: 2x2'''.split('\n')
    ]

    answers = [
        3
    ]

    for test, answer in zip(tests, answers):
        computed = solve(test)
        assert computed == answer, (test, answer, computed)


if __name__ == '__main__':
    run_tests()
    print(solve(sys.stdin))
