import copy
import itertools
import queue
import sys
import time
from typing import Iterable, List, Tuple, Callable, Dict, Optional, Iterator


def fix_modes(modes: List[int], max_length: int) -> List[int]:
    while len(modes) < max_length:
        modes.append(0)
    return modes


def add(modes: List[int], memory: List[int], memory_ptr: int, **kwargs) -> Tuple[Optional[int], int]:
    offset = 4
    modes = fix_modes(modes=modes, max_length=offset - 1)
    operand1, operand2, result_ptr = memory[memory_ptr + 1:memory_ptr + offset]
    if modes[0] == 0:
        operand1 = memory[operand1]
    if modes[1] == 0:
        operand2 = memory[operand2]
    memory[result_ptr] = operand1 + operand2
    return None, memory_ptr + offset


def multiply(modes: List[int], memory: List[int], memory_ptr: int, **kwargs) -> Tuple[Optional[int], int]:
    offset = 4
    modes = fix_modes(modes=modes, max_length=offset - 1)
    operand1, operand2, result_ptr = memory[memory_ptr + 1:memory_ptr + offset]
    if modes[0] == 0:
        operand1 = memory[operand1]
    if modes[1] == 0:
        operand2 = memory[operand2]
    memory[result_ptr] = operand1 * operand2
    return None, memory_ptr + offset


def store(modes: List[int], memory: List[int], memory_ptr: int,
          inputs_tape: Iterator[int]) -> Tuple[Optional[int], int]:
    offset = 2
    result_ptr = memory[memory_ptr + 1]
    value = next(inputs_tape)
    memory[result_ptr] = value
    return None, memory_ptr + offset


def load(modes: List[int], memory: List[int], memory_ptr: int, **kwargs) -> Tuple[Optional[int], int]:
    offset = 2
    modes = fix_modes(modes=modes, max_length=offset - 1)
    result = memory[memory_ptr + 1]
    if modes[0] == 0:
        result = memory[memory[memory_ptr + 1]]
    return result, memory_ptr + offset


def jump_when_cond(fn: Callable) -> Callable:
    def inner(modes: List[int], memory: List[int], memory_ptr: int, **kwargs) -> Tuple[Optional[int], int]:
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
    def inner(modes: List[int], memory: List[int], memory_ptr: int, **kwargs) -> Tuple[Optional[int], int]:
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


def execute(memory: List[int], inputs_tape: Iterator[int], pid: Optional[int] = None) -> Iterator[int]:
    op_registry: Dict[int, Callable[[List[int], List[int], int, Iterator[int]], Tuple[int, int]]] = {
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
    while True:
        value = memory[code_ptr]
        if value == 99:
            raise StopIteration()
        value = str(value)
        op, modes = int(value[-2:]), [int(mode) for mode in reversed(list(value[:-2]))]
        output, code_ptr = op_registry[op](modes=modes, memory=memory, memory_ptr=code_ptr, inputs_tape=inputs_tape)
        if output is not None:
            yield output


class Amplifier(object):
    def __init__(self, software: List[int], phase_setting: int, input_generator: Iterator[int],
                 id_: Optional[int] = None) -> None:
        self.software = software
        self.phase_setting = phase_setting
        self.input_generator = input_generator
        self.id = id_
        self.executor: Optional[Iterator[int]] = None
        self.unconsumed_outputs = queue.Queue()

    def _next_on_executor(self) -> int:
        if self.executor is None:
            inputs_tape = itertools.chain([self.phase_setting], self.input_generator)
            self.executor = execute(memory=self.software, inputs_tape=inputs_tape, pid=self.id)
        return next(self.executor)

    def generate(self) -> Iterator[int]:
        while True:
            yield self.unconsumed_outputs.get() if not self.unconsumed_outputs.empty() else self._next_on_executor()

    def run_till_halt(self) -> List[int]:
        outputs = []
        try:
            while True:
                output = self._next_on_executor()
                self.unconsumed_outputs.put(output)
        except StopIteration:
            while not self.unconsumed_outputs.empty():
                outputs.append(self.unconsumed_outputs.get())
        return outputs


def compute_output(program: List[int], phase_settings: Tuple[int, ...]) -> int:
    amps: List[Amplifier] = []
    for i, phase_setting in enumerate(phase_settings):
        inp_gen = amps[-1].generate() if amps else iter([-1])
        amps.append(Amplifier(software=copy.deepcopy(program), phase_setting=phase_setting,
                              input_generator=inp_gen, id_=i))

    # patch first amplifier
    amps[0].input_generator = itertools.chain([0], amps[-1].generate())
    outputs = amps[-1].run_till_halt()
    return outputs[-1]


def solve(input_iter: Iterable[str]) -> Tuple[int, Tuple[int, ...]]:
    program_str = next(iter(input_iter))
    program = [int(x) for x in program_str.split(',')]
    num_amplifiers, min_phase_setting, max_phase_setting = 5, 5, 9
    max_output = -1
    best_phase_settings: Tuple[int, ...] = (-1,)
    for phase_settings in itertools.permutations(range(min_phase_setting, max_phase_setting + 1), r=num_amplifiers):
        output = compute_output(program=program, phase_settings=phase_settings)
        if output > max_output:
            max_output = output
            best_phase_settings = phase_settings
    return max_output, best_phase_settings


def run_tests():
    tests = [
        ["3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"],
        ["3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,"
         "54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"],
    ]

    answers = [
        (139629729, (9, 8, 7, 6, 5,)),
        (18216, (9, 7, 8, 5, 6)),
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
