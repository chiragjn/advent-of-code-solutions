import sys
import itertools

def add(a, b):
    return a + b


def sub(a, b):
    return a - b


ops = {'+': add, '-': sub}


def solve(input_iter):
    ans = 0
    cached = set()
    cached.add(ans)

    fixed_input = []
    for line in input_iter:
        line = line.strip()
        operator, operand = ops[line[:1]], int(line[1:])
        fixed_input.append((operator, operand))

    for operator, operand in itertools.cycle(fixed_input):
        ans = operator(ans, operand)
        if ans in cached:
            break
        cached.add(ans)
    return ans


def run_tests():
    tests = [
        "+1, -1".split(', '),
        "+3, +3, +4, -2, -4".split(', '),
        "-6, +3, +8, +5, -6".split(', '),
        "+7, +7, -2, -7, -4".split(', '),
    ]

    answers = [
        0,
        10,
        5,
        14
    ]

    for test, answer in zip(tests, answers):
        assert solve(test) == answer, (test, answer)


if __name__ == '__main__':
    run_tests()
    print(solve(sys.stdin))
