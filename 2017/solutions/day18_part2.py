import collections
import queue
import string
import sys
from functools import wraps

queues = {}
Register = collections.namedtuple('Register', ['name', 'value'])


def resolve(operand, memory):
    if operand in string.ascii_lowercase:
        return Register(name=operand, value=memory[operand])
    else:
        return Register(name=None, value=int(operand))


def reslove_args(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        program = args[0]
        args = [resolve(arg, program.memory) for arg in args[1:]]
        return f(program, *args, **kwargs)

    return decorated


class Program(object):
    terminated = -1
    waiting = 0
    running = 1

    def __init__(self, pid, instructions):
        self.pid = pid
        queues[self.pid] = queue.Queue()
        self.memory = collections.defaultdict(int)
        self.memory['p'] = self.pid
        self.instructions = instructions
        self.status = None
        self.execution_pointer = 0
        self.snd_counter = 0

    @reslove_args
    def snd(self, *args):
        global queues
        self.snd_counter += 1
        queues[int(not self.pid)].put(args[0].value)

    @reslove_args
    def set_register(self, *args):
        self.memory[args[0].name] = args[1].value

    @reslove_args
    def add(self, *args):
        self.memory[args[0].name] = args[0].value + args[1].value

    @reslove_args
    def mul(self, *args):
        self.memory[args[0].name] = args[0].value * args[1].value

    @reslove_args
    def mod(self, *args):
        self.memory[args[0].name] = args[0].value % args[1].value

    @reslove_args
    def rcv(self, *args):
        if queues[self.pid].empty():
            self.status = Program.waiting
            return False
        else:
            self.memory[args[0].name] = queues[self.pid].get()
            return True

    @reslove_args
    def jgz(self, *args):
        if args[0].value > 0:
            return args[1].value - 1
        return 0

    def terminate(self):
        self.status = Program.terminated

    def run(self):
        if self.status == Program.terminated:
            return Program.terminated

        if self.status == Program.running:
            raise RuntimeError('Program was already running. This should not happen')

        if self.status == Program.waiting:
            self.status = Program.running

        while 0 <= self.execution_pointer < len(self.instructions):
            instruction, operands = self.instructions[self.execution_pointer]
            if instruction == 'snd':
                self.snd(*operands)
            elif instruction == 'set':
                self.set_register(*operands)
            elif instruction == 'add':
                self.add(*operands)
            elif instruction == 'mul':
                self.mul(*operands)
            elif instruction == 'mod':
                self.mod(*operands)
            elif instruction == 'rcv':
                if not self.rcv(*operands):
                    return self.execution_pointer
            elif instruction == 'jgz':
                self.execution_pointer += self.jgz(*operands)
            self.execution_pointer += 1

        self.status = Program.terminated
        return self.status


def main():
    instructions = []
    for i, line in enumerate(sys.stdin):
        operator, operands = line.strip().split(' ', 1)
        instructions.append((operator, operands.split()))
    p0, p1 = Program(0, instructions), Program(1, instructions)
    while True:
        p0.run()
        p1.run()
        if p0.status == Program.terminated and p1.status == Program.waiting and queues[p1.pid].empty():
            break
        elif p1.status == Program.terminated and p0.status == Program.waiting and queues[p0.pid].empty():
            break
        elif p1.status == Program.terminated and p1.status == Program.terminated:
            break
        elif p0.status == Program.waiting and queues[p0.pid].empty():
            p0.terminate()

    print(p1.snd_counter)


if __name__ == '__main__':
    main()
