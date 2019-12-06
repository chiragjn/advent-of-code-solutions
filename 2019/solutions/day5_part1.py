import sys
import time
from typing import Iterable, List, Tuple, Callable, Dict, Optional


def fix_modes(modes: List[int], max_length: int) -> List[int]:
    while len(modes) < max_length:
        modes.append(0)
    return modes


def add(modes: List[int], memory: List[int], memory_ptr: int, inputs_stack: List[int]) -> Tuple[Optional[int], int]:
    offset = 4
    modes = fix_modes(modes=modes, max_length=offset - 1)
    operand1, operand2, result_ptr = memory[memory_ptr + 1:memory_ptr + offset]
    if modes[0] == 0:
        operand1 = memory[operand1]
    if modes[1] == 0:
        operand2 = memory[operand2]
    memory[result_ptr] = operand1 + operand2
    return None, memory_ptr + offset


def multiply(modes: List[int], memory: List[int], memory_ptr: int,
             inputs_stack: List[int]) -> Tuple[Optional[int], int]:
    offset = 4
    modes = fix_modes(modes=modes, max_length=offset - 1)
    operand1, operand2, result_ptr = memory[memory_ptr + 1:memory_ptr + offset]
    if modes[0] == 0:
        operand1 = memory[operand1]
    if modes[1] == 0:
        operand2 = memory[operand2]
    memory[result_ptr] = operand1 * operand2
    return None, memory_ptr + offset


def store(modes: List[int], memory: List[int], memory_ptr: int, inputs_stack: List[int]) -> Tuple[Optional[int], int]:
    offset = 2
    modes = fix_modes(modes=modes, max_length=offset - 1)
    result_ptr = memory[memory_ptr + 1]
    memory[result_ptr] = inputs_stack.pop()
    return None, memory_ptr + offset


def load(modes: List[int], memory: List[int], memory_ptr: int, inputs_stack: List[int]) -> Tuple[Optional[int], int]:
    offset = 2
    modes = fix_modes(modes=modes, max_length=offset - 1)
    result_ptr = memory[memory_ptr + 1]
    return memory[result_ptr], memory_ptr + offset


def execute(memory: List[int], inputs_stack: List[int]) -> List[int]:
    op_registry: Dict[int, Callable[[List[int], List[int], int, List[int]], Tuple[int, int]]] = {
        1: add,
        2: multiply,
        3: store,
        4: load,
    }
    code_ptr = 0
    outputs: List[int] = []
    while True:
        value = memory[code_ptr]
        if value == 99:
            break
        value = str(value)
        op, modes = int(value[-2:]), [int(mode) for mode in reversed(list(value[:-2]))]
        output, code_ptr = op_registry[op](modes=modes, memory=memory, memory_ptr=code_ptr, inputs_stack=inputs_stack)
        if output is not None:
            outputs.append(output)
    return outputs


def solve(input_iter: Iterable[str]) -> int:
    program_str = next(iter(input_iter))
    program = [int(x) for x in program_str.split(',')]
    outputs = execute(memory=program, inputs_stack=[1])
    return outputs[-1]


def run_tests():
    tests = [
        ["3,0,4,0,99"],
        ["1002,6,3,6,4,6,33"]
    ]

    answers = [
        1,
        99,
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
