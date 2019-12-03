import copy
import sys
import time
from typing import Iterable, List, Any


def execute(program: List[int], noun: int, verb: int) -> int:
    program[1], program[2] = noun, verb
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


def solve(input_iter: Iterable[str]) -> Any:
    program = next(iter(input_iter))
    program = [int(x) for x in program.split(',')]
    for noun in range(100):
        for verb in range(100):
            if execute(copy.deepcopy(program), noun=noun, verb=verb) == 19690720:
                return 100 * noun + verb


def run_tests():
    tests = [
    ]

    answers = [
    ]

    for i, (test, answer) in enumerate(zip(tests, answers), start=1):
        print('Running test: {}/{}'.format(i, len(tests)))
        start = time.time()
        computed = solve(test)
        end = time.time()
        assert computed == answer, (test, answer, computed)
        print('OK. Took {:.2f}'.format(end - start))


if __name__ == '__main__':
    run_tests()
    print(solve(sys.stdin))
