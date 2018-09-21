import re

reject_pattern = re.compile(r'!.')
angle_brackets = re.compile(r'(?<=<)[^>]+(?=>)')

def main():
    seq = input().strip()
    print(solve(seq))

def solve(seq):
    seq = reject_pattern.sub('', seq)
    a = len(seq)
    seq = angle_brackets.sub('', seq)
    b = len(seq)
    return a - b

assert solve('<>') == 0
assert solve('<random characters>') == 17 
assert solve('<<<<>') == 3
assert solve('<{!>}>') == 2
assert solve('<!!>') == 0
assert solve('<!!!>>') == 0
assert solve('<{o"i!a,<{i<a>') == 10

if __name__ == '__main__':
    main()
