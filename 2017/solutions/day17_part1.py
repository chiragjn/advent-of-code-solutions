def solve(n, till):
    # Naive solution
    state = [0]
    current_index = 0
    for i in range(1, till + 1):
        split_at = ((current_index + n) % len(state)) + 1
        state = state[:split_at] + [i] + state[split_at:]
        current_index = split_at
    answer = state[(state.index(till) + 1) % len(state)]
    return answer


def main():
    n = int(input().strip())
    print(solve(n, 2017))


assert solve(3, 2017) == 638

if __name__ == '__main__':
    main()
