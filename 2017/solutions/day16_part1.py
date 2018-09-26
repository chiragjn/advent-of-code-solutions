import string


def solve(n, instructions):
    state = list(string.ascii_lowercase[:n])
    for instruction in instructions:
        instruction, data = instruction[0], instruction[1:]
        if instruction == 's':
            data = -1 * int(data)
            state = state[data:] + state[:data]
        elif instruction == 'x':
            first, second = data.split('/')
            first, second = int(first), int(second)
            state[first], state[second] = state[second], state[first]
        elif instruction == 'p':
            first, second = data.split('/')
            first, second = state.index(first), state.index(second)
            state[first], state[second] = state[second], state[first]
    return ''.join(state)


def main():
    # naive way
    instructions = input().strip().split(',')
    print(solve(16, instructions))


assert solve(5, ['s1', 'x3/4', 'pe/b']) == 'baedc'

if __name__ == '__main__':
    main()
