import sys
import time
from typing import Iterable, List


def execute(program: List[int]) -> int:
    op_ptr = 0
    while program[op_ptr] != 99:
        if program[op_ptr] == 1:
            operand1_ptr, operand2_ptr, result_ptr = program[op_ptr + 1: op_ptr + 4]
            program[result_ptr] = program[operand1_ptr] + program[operand2_ptr]
            op_ptr += 4
        elif program[op_ptr] == 2:
            operand1_ptr, operand2_ptr, result_ptr = program[op_ptr + 1: op_ptr + 4]
            program[result_ptr] = program[operand1_ptr] * program[operand2_ptr]
            op_ptr += 4
        else:
            raise RuntimeError(f'Unknown op code at {op_ptr}: {program[op_ptr]}')
    return program[0]


def solve(input_iter: Iterable[str], restore: bool = True) -> int:
    program = next(iter(input_iter))
    program = [int(x) for x in program.split(',')]
    if restore:
        program[1], program[2] = 12, 2
    return execute(program)


def run_tests():
    tests = [
        ["1,9,10,3,2,3,11,0,99,30,40,50"],
        ["1,0,0,0,99"],
        ["2,3,0,3,99"],
        ["2,4,4,5,99,0"],
        ["1,1,1,4,99,5,6,0,99"],
    ]

    answers = [
        3500,
        2,
        2,
        2,
        30,
    ]

    for i, (test, answer) in enumerate(zip(tests, answers), start=1):
        print('Running test: {}/{}'.format(i, len(tests)))
        start = time.time()
        computed = solve(test, restore=False)
        end = time.time()
        assert computed == answer, (test, answer, computed)
        print('OK. Took {:.2f}'.format(end - start))


if __name__ == '__main__':
    run_tests()
    print(solve(sys.stdin))
