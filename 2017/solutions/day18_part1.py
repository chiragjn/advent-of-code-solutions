import collections
import string
import sys
from functools import wraps

last_played = 0
memory = collections.defaultdict(int)
Register = collections.namedtuple('Register', ['name', 'value'])


def resolve(operand):
    if operand in string.ascii_lowercase:
        return Register(name=operand, value=memory[operand])
    else:
        return Register(name=None, value=int(operand))


def reslove_args(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        args = [resolve(arg) for arg in args]
        return f(*args, **kwargs)

    return decorated


@reslove_args
def snd(*args):
    global memory, last_played
    last_played = args[0].value


@reslove_args
def set_register(*args):
    global memory
    memory[args[0].name] = args[1].value


@reslove_args
def add(*args):
    global memory
    memory[args[0].name] = args[0].value + args[1].value


@reslove_args
def mul(*args):
    global memory
    memory[args[0].name] = args[0].value * args[1].value


@reslove_args
def mod(*args):
    global memory
    memory[args[0].name] = args[0].value % args[1].value


@reslove_args
def rcv(*args):
    global memory, last_played
    if args[0].value != 0:
        return last_played


@reslove_args
def jgz(*args):
    global memory, last_played
    if args[0].value > 0:
        return args[1].value - 1
    return 0


def main():
    instructions = []
    for i, line in enumerate(sys.stdin):
        operator, operands = line.strip().split(' ', 1)
        instructions.append((operator, operands.split()))

    execution_pointer = 0
    while 0 <= execution_pointer < len(instructions):
        instruction, operands = instructions[execution_pointer]
        if instruction == 'snd':
            snd(*operands)
        elif instruction == 'set':
            set_register(*operands)
        elif instruction == 'add':
            add(*operands)
        elif instruction == 'mul':
            mul(*operands)
        elif instruction == 'mod':
            mod(*operands)
        elif instruction == 'rcv':
            val = rcv(*operands)
            if val != 0:
                print(val)
                break
        elif instruction == 'jgz':
            execution_pointer += jgz(*operands)
        execution_pointer += 1


if __name__ == '__main__':
    main()
