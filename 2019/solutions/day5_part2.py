import sys
import time
import copy
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
    inputs_stack = copy.deepcopy(inputs_stack)
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


def solve(input_iter: Iterable[str], inputs_stack: Optional[List[int]] = None) -> int:
    if inputs_stack is None:
        inputs_stack = [5]
    program_str = next(iter(input_iter))
    program = [int(x) for x in program_str.split(',')]
    outputs = execute(memory=program, inputs_stack=inputs_stack)
    return outputs[-1]


def run_tests():
    tests = [
        (["3,0,4,0,99"], [1]),
        (["1002,6,3,6,4,6,33"], [1]),
        (["3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9"], [0]),
        (["3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9"], [1]),
        (["3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,"
          "1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"], [7]),
        (["3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,"
          "1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"], [8]),
        (["3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,"
          "1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"], [9]),
    ]

    answers = [
        1,
        99,
        0,
        1,
        999,
        1000,
        1001,
    ]

    for i, (test, answer) in enumerate(zip(tests, answers), start=1):
        print('Running test: {}/{}'.format(i, len(tests)))
        start = time.time()
        computed = solve(*test)
        end = time.time()
        assert computed == answer, (test, answer, computed)
        print('OK. Took {:.2f}'.format(end - start))


if __name__ == '__main__':
    run_tests()
    print(solve(sys.stdin))
