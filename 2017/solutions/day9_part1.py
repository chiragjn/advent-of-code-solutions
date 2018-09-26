import re

reject_pattern = re.compile(r'!.')
not_brackets = re.compile(r'[^<>\{\}]+')
angle_brackets = re.compile(r'<[^>]+>')


def main():
    seq = input().strip()
    print(solve(seq))


def solve(seq):
    seq = reject_pattern.sub('', seq)
    seq = not_brackets.sub('', seq)
    seq = angle_brackets.sub('', seq)
    seq = seq.replace('<>', '')
    ans = 0
    stack = []
    for c in seq:
        if c == '{':
            stack.append(c)
        else:
            ans += len(stack)
            stack.pop()
    return ans


assert solve('{}') == 1
assert solve('{{{}}}') == 6
assert solve('{{},{}}') == 5
assert solve('{{{},{},{{}}}}') == 16
assert solve('{<a>,<a>,<a>,<a>}') == 1
assert solve('{{<ab>},{<ab>},{<ab>},{<ab>}}') == 9
assert solve('{{<!!>},{<!!>},{<!!>},{<!!>}}') == 9
assert solve('{{<a!>},{<a!>},{<a!>},{<ab>}}') == 3

if __name__ == '__main__':
    main()
