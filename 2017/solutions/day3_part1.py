import math

def main():
    n = int(input())
    if n == 1:
        print(0)
    else:
        k = int(math.sqrt(n))
        if k % 2 == 0:
            k -= 1
        if k * k == n:
            print(2 * (k // 2))
        else:
            nx = 2 * (k // 2) + 2
            st = nx - 1
            en = nx // 2
            vals = list(range(st, en - 1, -1)) + list(range(en + 1, st + 2))
            z = 0
            st = k * k + 1
            while st < n:
                st += 1
                z = (z + 1) % len(vals)
            print(vals[z])



if __name__ == '__main__':
    main()
