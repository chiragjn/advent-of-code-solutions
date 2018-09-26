import string

times = 1000000000
memory = []


def solve(n, instructions):
    global memory
    state = list(string.ascii_lowercase[:n])
    memory = [''.join(state)]
    for i in range(1, times + 1):
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

        to_cache = ''.join(state)
        if to_cache in memory:
            cycle_start = memory.index(to_cache)
            memory = memory[cycle_start:]
            state = memory[(times - i) % len(memory)]
            break
        else:
            memory.append(to_cache)

    return ''.join(state)


def main():
    # naive way
    instructions = input().strip().split(',')
    print(solve(16, instructions))


if __name__ == '__main__':
    main()
