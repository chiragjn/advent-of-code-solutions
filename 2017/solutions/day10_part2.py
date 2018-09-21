def main():
    print(solve(input()))


def solve(inp):
    # naive
    nums = list(range(256))
    lengths = list(map(ord, inp.strip())) + [17, 31, 73, 47, 23]
    skip = 0
    pointer = 0
    for i in range(64):
        for length in lengths:
            to_commit, z = [], 0
            for j in range(pointer + length - 1, pointer - 1,  -1):
                to_commit.append(nums[j % len(nums)])
            
            for j in range(pointer, pointer + length):
                nums[j % len(nums)] = to_commit[z]
                z += 1

            pointer = (pointer + length + skip) % len(nums)
            skip += 1

    ans = []
    for i in range(0, 256, 16):
        xor = 0
        for j in range(i, i + 16):
            xor ^= nums[j]
        ans.append('{0:x}'.format(xor).zfill(2))
    return ''.join(ans)


assert solve('') == 'a2582a3a0e66e6e86e3812dcb672a272'
assert solve('AoC 2017') == '33efeb34ea91902bb2f59c9920caa6cd'
assert solve('1,2,3') == '3efbe78a8d82f29979031a4aa0b16a9d'
assert solve('1,2,4') == '63960835bcdc130f0b66d7ff4f6a5a8e'

if __name__ == '__main__':
    main()
