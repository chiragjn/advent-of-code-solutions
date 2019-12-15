import collections
import copy
import enum
import queue
import sys
import time
from typing import Iterable, List, Tuple, Callable, Dict, Optional, Iterator, Union, Set


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


class Robot(object):
    class Direction(enum.Enum):
        NORTH = 1
        SOUTH = 2
        WEST = 3
        EAST = 4

    FORWARD = {
        Direction.NORTH.value: lambda x, y: (x, y + 1),
        Direction.EAST.value: lambda x, y: (x + 1, y),
        Direction.SOUTH.value: lambda x, y: (x, y - 1),
        Direction.WEST.value: lambda x, y: (x - 1, y),
    }

    MOVES = [
        (Direction.NORTH.value, Direction.SOUTH.value),
        (Direction.EAST.value, Direction.WEST.value),
        (Direction.SOUTH.value, Direction.NORTH.value),
        (Direction.WEST.value, Direction.EAST.value),
    ]

    def __init__(self, software: List[int]) -> None:
        self.grid: Dict[Tuple[int, int], int] = collections.defaultdict(lambda: -1)
        self.visited_coords: Set[Tuple[int, int]] = set()
        brain = IntCodeComputer(software=software, inputs_tape=self._input_generator())
        self.executor: Iterator[int] = brain.execute()
        self.inputs_queue = queue.Queue()

    def _input_generator(self) -> Iterator[int]:
        while True:
            yield self.inputs_queue.get()

    def explore(self) -> None:

        def inner(x: int, y: int) -> None:
            if (x, y) in self.visited_coords:
                return

            self.visited_coords.add((x, y))
            for move, reverse_move in Robot.MOVES:
                self.inputs_queue.put(move)
                next_x, next_y = Robot.FORWARD[move](x, y)
                self.grid[(next_x, next_y)] = next(self.executor)
                if self.grid[(next_x, next_y)] != 0:
                    # if it was not a wall
                    inner(next_x, next_y)
                    # reverse the move
                    self.inputs_queue.put(reverse_move)
                    status = next(self.executor)
                    try:
                        assert status > 0, f'Robot was not able to backtrack, something is wrong'
                    except AssertionError:
                        self.print_grid()
                        raise

        self.grid[(0, 0)] = 1
        inner(0, 0)

    def print_grid(self):
        c = ['#', '.', '*', 's', '?']
        kxs, kys = zip(*self.grid.keys())
        for j in range(max(kys), min(kys) - 1, -1):
            for i in range(min(kxs), max(kxs) + 1):
                idx = self.grid[(i, j)]
                if i == 0 and j == 0:
                    idx = -2
                print(c[idx], end='')
            print()

    def min_steps_to_oxygen(self) -> int:
        target = (0, 0)
        start = (0, 0)
        visited: Set[Tuple[int, int]] = set()
        for key in self.grid:
            if self.grid[key] == 2:
                target = key
                break
        q = queue.Queue()
        q.put((start, 0))
        visited.add(start)
        while not q.empty():
            u, steps_so_far = q.get()
            if u == target:
                return steps_so_far
            for fn in Robot.FORWARD.values():
                v = fn(*u)
                if v not in visited and self.grid[v] in {1, 2}:
                    visited.add(v)
                    q.put((v, steps_so_far + 1))
        return -1


def solve(input_iter: Iterable[str]) -> int:
    program_str = next(iter(input_iter))
    program = [int(x) for x in program_str.split(',')]
    r = Robot(software=copy.deepcopy(program))
    r.explore()
    return r.min_steps_to_oxygen()


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
