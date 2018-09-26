def solve(skip, till):
    # We will just track zero's position
    zero_ind, current_index, next_to_zero = 0, 0, None
    for i in range(1, till + 1):
        current_index = (current_index + skip) % i
        if current_index == zero_ind:
            next_to_zero = i
        elif current_index < zero_ind:
            zero_ind += 1
        current_index += 1
    return next_to_zero


def main():
    n = int(input().strip())
    print(solve(n, 50000000))


if __name__ == '__main__':
    main()
