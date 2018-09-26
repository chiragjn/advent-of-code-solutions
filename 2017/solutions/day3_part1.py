def get_xy(number):
    if number == 1:
        return 0, 0
    k = 0
    x, y = 0, 0
    z = 1
    while z < number:
        k += 2
        z = (k + 1) * (k + 1)
        x += 1
        y -= 1

    ops = [lambda x, y: (x - 1, y),
           lambda x, y: (x, y + 1),
           lambda x, y: (x + 1, y),
           lambda x, y: (x, y - 1)]

    if z == number:
        return x, y

    for i in range(4):
        op = ops[i]
        for _ in range(k):
            z -= 1
            x, y = op(x, y)
            if z == number:
                return x, y
    return None, None


def main():
    n = int(input())
    x, y = get_xy(n)
    print(abs(x - 1) + abs(y - 1))


if __name__ == '__main__':
    main()
