import sys
from typing import List, Tuple


def get_value(x, y, serial):
    rack_id = x + 10
    power = rack_id * y
    power += serial
    power *= rack_id
    power = (power // 100) % 10
    power -= 5
    return power


def solve(input_line: str) -> str:
    serial = int(input_line.strip())

    grid_size = 300
    patch_size = 3
    grid: List[List[int]] = [[0 for __ in range(grid_size + 1)] for _ in range(grid_size + 1)]
    sum_grid: List[List[int]] = [[0 for __ in range(grid_size + 1)] for _ in range(grid_size + 1)]

    for i in range(1, grid_size + 1):
        for j in range(1, grid_size + 1):
            grid[i][j] = get_value(x=i, y=j, serial=serial)
            sum_grid[i][j] = sum_grid[i - 1][j] + sum_grid[i][j - 1] - sum_grid[i - 1][j - 1] + grid[i][j]

    max_value = int(-1e18)
    answer: Tuple[int, int] = (-1, -1)

    for i in range(1, grid_size - patch_size + 2):
        for j in range(1, grid_size - patch_size + 2):
            patch_value = (sum_grid[i + patch_size - 1][j + patch_size - 1]
                           + sum_grid[i - 1][j - 1]
                           - sum_grid[i - 1][j + patch_size - 1]
                           - sum_grid[i + patch_size - 1][j - 1])
            if patch_value >= max_value:
                max_value = patch_value
                answer = (i, j)

    return '{},{}'.format(*answer)


def run_tests():
    tests = [
        '18',
    ]

    answers = [
        '33,45',
    ]

    for test, answer in zip(tests, answers):
        computed = solve(test)
        assert computed == answer, (test, answer, computed)


if __name__ == '__main__':
    run_tests()
    print(solve(sys.stdin.readline()))
