import collections
import copy
import sys
import time
from typing import Iterable, List, Tuple, Callable, Dict, Optional, Iterator, Union


class Memory(object):
    def __init__(self):
        self._data: Dict[int, int] = collections.defaultdict(int)

    def __setitem__(self, key: int, value: int):
        if isinstance(key, slice):
            raise RuntimeError(f'SET: setting via slice is not supported')
        if key < 0:
            raise RuntimeError(f'SET: Negative indexing not allowed, got key: {key}')
        self._data[key] = value

    def __getitem__(self, item: int) -> Union[int, List[int]]:
        if isinstance(item, slice):
            return [self[i] for i in range(item.start or 0, item.stop, item.step or 1)]
        if item < 0:
            raise RuntimeError(f'GET: Negative indexing not allowed, got key: {item}')
        return self._data[item]


class IntCodeComputer(object):
    def __init__(self, software: List[int], inputs_tape: Iterator[int], pid: Optional[int] = None) -> None:
        self.relative_base = 0
        self.memory: Memory = Memory()
        for i, v in enumerate(software):
            self.memory[i] = v
        self.code_ptr: int = 0
        self.inputs_tape = inputs_tape
        self.pid = pid

        self._op_registry: Dict[int, Callable[[List[int], List[int], int, Iterator[int]], Tuple[int, int]]] = {
            1: self._binary_arithmetic(fn=lambda x, y: x + y),
            2: self._binary_arithmetic(fn=lambda x, y: x * y),
            3: self._store,
            4: self._load,
            5: self._jump_when_cond(fn=lambda x: x != 0),
            6: self._jump_when_cond(fn=lambda x: x == 0),
            7: self._compare_with_op(fn=lambda x, y: x < y),
            8: self._compare_with_op(fn=lambda x, y: x == y),
            9: self._move_relative_base,
        }

    def _get_value(self, operand: int, mode: int, arg_type: str) -> int:
        if arg_type == 'W':
            if mode == 0:
                return operand
            elif mode == 1:
                raise RuntimeError('Parameter to write to cannot be in immediate mode')
            elif mode == 2:
                return self.relative_base + operand
        elif arg_type == 'R':
            if mode == 0:
                return self.memory[operand]
            elif mode == 1:
                return operand
            elif mode == 2:
                return self.memory[self.relative_base + operand]

        raise RuntimeError(f'Unable to parse args: operand={operand}, mode={mode}, arg_type={arg_type}')

    def _parse_args(self, num_args: int, modes: List[int], args_type: List[str]) -> List[int]:
        while len(modes) < num_args:
            modes.append(0)
        operands = self.memory[self.code_ptr + 1:self.code_ptr + num_args + 1]
        operands = [self._get_value(operand, mode, arg_type)
                    for operand, mode, arg_type in zip(operands, modes, args_type)]
        return operands

    def _binary_arithmetic(self, fn: Callable):

        def inner():
            offset = 4
            args_type = ['R', 'R', 'W']
            modes = [int(mode) for mode in reversed(list(str(self.memory[self.code_ptr])[:-2]))]
            operands = self._parse_args(num_args=offset - 1, modes=modes, args_type=args_type)
            operand1, operand2, result_ptr = operands
            self.memory[result_ptr] = fn(operand1, operand2)
            return None, self.code_ptr + offset

        return inner

    def _store(self) -> Tuple[Optional[int], int]:
        offset = 2
        args_type = ['W']
        modes = [int(mode) for mode in reversed(list(str(self.memory[self.code_ptr])[:-2]))]
        operands = self._parse_args(num_args=offset - 1, modes=modes, args_type=args_type)
        result_ptr = operands[0]
        value = next(self.inputs_tape)
        self.memory[result_ptr] = value
        return None, self.code_ptr + offset

    def _load(self) -> Tuple[Optional[int], int]:
        offset = 2
        args_type = ['R']
        modes = [int(mode) for mode in reversed(list(str(self.memory[self.code_ptr])[:-2]))]
        operands = self._parse_args(num_args=offset - 1, modes=modes, args_type=args_type)
        result = operands[0]
        return result, self.code_ptr + offset

    def _jump_when_cond(self, fn: Callable) -> Callable:

        def inner() -> Tuple[Optional[int], int]:
            offset = 3
            args_type = ['R', 'R']
            modes = [int(mode) for mode in reversed(list(str(self.memory[self.code_ptr])[:-2]))]
            operands = self._parse_args(num_args=offset - 1, modes=modes, args_type=args_type)
            operand1, operand2 = operands
            if fn(operand1):
                code_ptr = operand2
            else:
                code_ptr = self.code_ptr + offset
            return None, code_ptr

        return inner

    def _compare_with_op(self, fn: Callable) -> Callable:

        def inner() -> Tuple[Optional[int], int]:
            offset = 4
            args_type = ['R', 'R', 'W']
            modes = [int(mode) for mode in reversed(list(str(self.memory[self.code_ptr])[:-2]))]
            operands = self._parse_args(num_args=offset - 1, modes=modes, args_type=args_type)
            operand1, operand2, result_ptr = operands
            self.memory[result_ptr] = 1 if fn(operand1, operand2) else 0
            return None, self.code_ptr + offset

        return inner

    def _move_relative_base(self):
        offset = 2
        args_type = ['R']
        modes = [int(mode) for mode in reversed(list(str(self.memory[self.code_ptr])[:-2]))]
        operands = self._parse_args(num_args=offset - 1, modes=modes, args_type=args_type)
        operand1 = operands[0]
        self.relative_base += operand1
        return None, self.code_ptr + offset

    def execute(self) -> Iterator[int]:
        while True:
            value = self.memory[self.code_ptr]
            if value == 99:
                raise StopIteration()
            value = str(value)
            op = int(value[-2:])
            output, self.code_ptr = self._op_registry[op]()
            if output is not None:
                yield output


def solve(input_iter: Iterable[str]) -> List[int]:
    program_str = next(iter(input_iter))
    program = [int(x) for x in program_str.split(',')]
    inputs_tape = iter([1])
    icc = IntCodeComputer(software=copy.deepcopy(program), inputs_tape=copy.deepcopy(inputs_tape))
    outputs = [output for output in icc.execute()]
    return outputs


def run_tests():
    tests = [
        ["109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"],
        ["1102,34915192,34915192,7,4,7,99,0"],
        ["104,1125899906842624,99"],
    ]

    answers = [
        [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99],
        [1219070632396864],
        [1125899906842624],

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
