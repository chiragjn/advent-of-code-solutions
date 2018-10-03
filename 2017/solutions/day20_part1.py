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


class Point(object):
    def __init__(self, position, velocity, acceleration):
        self.position, self.velocity, self.acceleration = position, velocity, acceleration

    def get_position_at(self, n):
        return self.position.add(self.velocity.scalar_mul(n)).add(self.acceleration.scalar_mul((n * (n + 1)) // 2))

    def get_dist_at(self, n):
        return self.get_position_at(n).l1_norm()


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

    closest_counts = collections.defaultdict(int)
    for i in range(2, 10):
        dists = [point.get_dist_at(10 ** i) for point in points]
        closest_counts[dists.index(min(dists))] += 1

    print(list(sorted(closest_counts.items(), key=lambda item: item[1], reverse=True))[0][0])


if __name__ == '__main__':
    main()
