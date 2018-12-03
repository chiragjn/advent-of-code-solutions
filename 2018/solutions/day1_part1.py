import sys


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


ops = {'+': add, '-': sub}


def solve(input_iter):
    ans = 0
    for line in input_iter:
        line = line.strip()
        operator, operand = ops[line[:1]], int(line[1:])
        ans = operator(ans, operand)
    return ans


if __name__ == '__main__':
    print(solve(sys.stdin))
