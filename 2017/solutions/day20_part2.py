import collections
import re
import sys


class Vector(object):
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def l1_norm(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def add(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def scalar_mul(self, a):
        return Vector(a * self.x, a * self.y, a * self.z)

    def __hash__(self):
        return hash((self.x, self.y, self.z,))

    def __str__(self):
        return '[{}, {}, {}]'.format(self.x, self.y, self.z)


class Point(object):
    def __init__(self, position, velocity, acceleration):
        self.position, self.velocity, self.acceleration = position, velocity, acceleration

    def update_position(self):
        self.velocity = self.velocity.add(self.acceleration)
        self.position = self.position.add(self.velocity)
        return self

    def __hash__(self):
        return hash(self.position)

    def __str__(self):
        return str(self.position)

    def __repr__(self):
        return str(self.position)


pattern = re.compile(r'[<>=pav, ]+')


def main():
    points = []
    for line in sys.stdin:
        pva = list(map(int, pattern.sub(' ', line.strip()).strip().split()))
        points.append(
            Point(
                position=Vector(pva[0], pva[1], pva[2]),
                velocity=Vector(pva[3], pva[4], pva[5]),
                acceleration=Vector(pva[6], pva[7], pva[8]),
            )
        )

    render_next_n = 10
    for i in range(1, render_next_n + 1):
        point_positions = collections.defaultdict(int)
        for point in points:
            point.update_position()
            point_positions[point] += 1

        points = [point for point, count in point_positions.items() if count < 2]
        # print(points[:5])

    print(len(points))


if __name__ == '__main__':
    main()
