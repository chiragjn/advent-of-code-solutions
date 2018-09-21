'''
This problem can be probably be done better with ast module.
'''
import sys
import collections

memory = collections.defaultdict(int)

def eq(a, b): return a == b
def ne(a, b): return a != b
def gt(a, b): return a > b
def gte(a, b): return a >= b
def lt(a, b): return a < b
def lte(a, b): return a <= b
def add(a, b): return a + b
def sub(a, b): return a - b

ops = {
    '==': eq,
    '!=': ne,
    '>': gt,
    '>=': gte,
    '<': lt,
    '<=': lte,
}

ins = {
    'inc': add,
    'dec': sub,
}

def execute(line):
    register, instruction, value, _, check_register, op, op_val = line.strip().split()
    value, op_val = int(value), int(op_val)
    if ops[op](memory[check_register], op_val):
        memory[register] = ins[instruction](memory[register], value)

def main():
    for line in sys.stdin:
        execute(line)
    print(max(memory.values()))

if __name__ == '__main__':
    main()
