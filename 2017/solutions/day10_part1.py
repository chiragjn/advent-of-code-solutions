def main():
    # naive
    nums = list(range(256))
    lengths = list(map(int, input().strip().split(',')))
    skip = 0
    pointer = 0
    for length in lengths:
        to_commit, z = [], 0
        for i in range(pointer + length - 1, pointer - 1, -1):
            to_commit.append(nums[i % len(nums)])

        for i in range(pointer, pointer + length):
            nums[i % len(nums)] = to_commit[z]
            z += 1

        pointer = (pointer + length + skip) % len(nums)
        skip += 1

    print(nums[0] * nums[1])


if __name__ == '__main__':
    main()
