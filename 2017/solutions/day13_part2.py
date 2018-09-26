import sys


def main():
    max_ans = 5000001
    # Not a generic solution that covers all possible cases
    # Trying every value from 0 to solution would taking longer time 
    # I prefer using more memory in my solution for now
    sieve = [True] * max_ans
    sieve[0] = False
    for line in sys.stdin:
        layer, depth = list(map(int, line.strip().split(': ')))
        k = 2 * depth - 2
        for i in range(k, max_ans, k):
            sieve[i - layer] = False

    for i, good in enumerate(sieve):
        if good:
            print(i)
            break


if __name__ == '__main__':
    main()
