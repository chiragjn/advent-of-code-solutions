def main():
    # naive strategy 
    states = {}
    state = list(map(int, input().strip().split()))
    cycle = 0
    states[tuple(state)] = cycle
    count = 0
    while True:
        count += 1
        cycle += 1
        val = max(state)
        i = state.index(val)
        state[i] = 0
        while val > 0:
            i = (i + 1) % len(state)
            state[i] += 1
            val -= 1

        if tuple(state) in states:
            print(cycle - states[tuple(state)])
            break

        states[tuple(state)] = cycle


if __name__ == '__main__':
    main()
