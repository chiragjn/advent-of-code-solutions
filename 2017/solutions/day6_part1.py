def main():
    # naive strategy 
    states = set()
    state = list(map(int, input().strip().split()))
    states.add(tuple(state))
    count = 0
    while True:
        count += 1
        val = max(state)
        i = state.index(val)
        state[i] = 0
        while val > 0:
            i = (i + 1) % len(state)
            state[i] += 1
            val -= 1

        if tuple(state) in states:
            print(count)
            break

        states.add(tuple(state))


if __name__ == '__main__':
    main()
