import sys

lines = []


def is_safe(x, y):
    return 0 <= x < len(lines[0]) and 0 <= y < len(lines) and lines[x][y] != ' '


def go_down(x, y):
    return x + 1, y


def go_up(x, y):
    return x - 1, y


def go_right(x, y):
    return x, y + 1


def go_left(x, y):
    return x, y - 1


def go_forward(x, y, direction):
    if direction == 'l':
        x, y = go_left(x, y)
    elif direction == 'r':
        x, y = go_right(x, y)
    elif direction == 'u':
        x, y = go_up(x, y)
    elif direction == 'd':
        x, y = go_down(x, y)
    return x, y


def decide_direction(x, y, direction):
    fx, fy = go_forward(x, y, direction)

    if is_safe(fx, fy):
        return fx, fy, direction

    if direction == 'l' or direction == 'r':
        ux, uy = go_up(x, y)

        if is_safe(ux, uy):
            return ux, uy, 'u'

        dx, dy = go_down(x, y)
        if is_safe(dx, dy):
            return dx, dy, 'd'

    elif direction == 'u' or direction == 'd':
        lx, ly = go_left(x, y)

        if is_safe(lx, ly):
            return lx, ly, 'l'

        rx, ry = go_right(x, y)
        if is_safe(rx, ry):
            return rx, ry, 'r'

    return fx, fy, direction


def main():
    global lines
    lines = [list(line.strip('\n')) for line in sys.stdin]
    assert all(len(line) == len(lines[0]) for line in lines)
    x, y, direction = 0, lines[0].index('|'), 'd'
    answer = []
    while is_safe(x, y):
        if lines[x][y] == '+':
            x, y, direction = decide_direction(x, y, direction)
            continue
        elif lines[x][y] != '|' and lines[x][y] != '-':
            answer.append(lines[x][y])

        x, y = go_forward(x, y, direction)

    print(''.join(answer))


if __name__ == '__main__':
    main()
