import copy
import itertools
import sys
import time
from functools import lru_cache
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
    result_ptr = memory[memory_ptr + 1]
    memory[result_ptr] = inputs_stack.pop()
    return None, memory_ptr + offset


def load(modes: List[int], memory: List[int], memory_ptr: int, inputs_stack: List[int]) -> Tuple[Optional[int], int]:
    offset = 2
    modes = fix_modes(modes=modes, max_length=offset - 1)
    result = memory[memory_ptr + 1]
    if modes[0] == 0:
        result = memory[memory[memory_ptr + 1]]
    return result, memory_ptr + offset


def jump_when_cond(fn: Callable) -> Callable:
    def inner(
            modes: List[int], memory: List[int],
            memory_ptr: int, inputs_stack: List[int]) -> Tuple[Optional[int], int]:
        offset = 3
        modes = fix_modes(modes=modes, max_length=offset - 1)
        operand1, operand2 = memory[memory_ptr + 1:memory_ptr + offset]
        if modes[0] == 0:
            operand1 = memory[operand1]
        if modes[1] == 0:
            operand2 = memory[operand2]
        if fn(operand1):
            memory_ptr = operand2
        else:
            memory_ptr = memory_ptr + offset
        return None, memory_ptr

    return inner


def compare_with_op(fn: Callable) -> Callable:
    def inner(
            modes: List[int], memory: List[int],
            memory_ptr: int, inputs_stack: List[int]) -> Tuple[Optional[int], int]:
        offset = 4
        modes = fix_modes(modes=modes, max_length=offset - 1)
        operand1, operand2, result_ptr = memory[memory_ptr + 1:memory_ptr + offset]
        if modes[0] == 0:
            operand1 = memory[operand1]
        if modes[1] == 0:
            operand2 = memory[operand2]
        memory[result_ptr] = 1 if fn(operand1, operand2) else 0
        return None, memory_ptr + offset

    return inner


def execute(memory: List[int], inputs_stack: List[int]) -> List[int]:
    op_registry: Dict[int, Callable[[List[int], List[int], int, List[int]], Tuple[int, int]]] = {
        1: add,
        2: multiply,
        3: store,
        4: load,
        5: jump_when_cond(fn=lambda x: x != 0),
        6: jump_when_cond(fn=lambda x: x == 0),
        7: compare_with_op(fn=lambda x, y: x < y),
        8: compare_with_op(fn=lambda x, y: x == y),
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


def compute_output(program: List[int], phase_settings: Tuple[int, ...]) -> int:
    @lru_cache(maxsize=512)
    def _compute(phase_setting: int = 0, previous_out: int = 0) -> List[int]:
        return execute(memory=copy.deepcopy(program), inputs_stack=copy.deepcopy([previous_out, phase_setting]))

    def inner(i: int = 0, previous_out: int = 0) -> int:
        if i >= len(phase_settings):
            return previous_out
        outputs = _compute(phase_setting=phase_settings[i], previous_out=previous_out)
        return inner(i=i + 1, previous_out=outputs[-1])

    return inner()


def solve(input_iter: Iterable[str]) -> Tuple[int, Tuple[int, ...]]:
    program_str = next(iter(input_iter))
    program = [int(x) for x in program_str.split(',')]
    num_amplifiers, max_phase_setting = 5, 4
    max_output = -1
    best_phase_settings: Tuple[int, ...] = (-1,)
    for phase_settings in itertools.permutations(range(max_phase_setting + 1), r=num_amplifiers):
        output = compute_output(program=program, phase_settings=phase_settings)
        if output > max_output:
            max_output = output
            best_phase_settings = phase_settings
    return max_output, best_phase_settings


def run_tests():
    tests = [
        ["3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"],
        ["3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"],
        ["3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33, 1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"],
    ]

    answers = [
        (43210, (4, 3, 2, 1, 0,)),
        (54321, (0, 1, 2, 3, 4,)),
        (65210, (1, 0, 4, 3, 2,)),
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
