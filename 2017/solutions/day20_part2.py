import collections
import itertools
import re
import sys


class Vector(object):
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def add(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def sub(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def scalar_mul(self, a):
        return Vector(a * self.x, a * self.y, a * self.z)

    def __hash__(self):
        return hash((self.x, self.y, self.z,))

    def __str__(self):
        return '[{}, {}, {}]'.format(self.x, self.y, self.z)


class Point(object):
    def __init__(self, position, velocity, acceleration):
        self.position, self.velocity, self.acceleration = position, velocity, acceleration
        # ax^2 + bx + c = 0
        self.path_coeffs = (
            self.acceleration,
            (self.velocity.scalar_mul(2).add(self.acceleration)),
            self.position.scalar_mul(2)
        )

    def get_collisions(self, other_point):
        def _get_real_postive_int_solutions(_a, _b, _c):
            # Solve quadratic equation in each dimension and if they collide at the same positive integer time solution
            # We ask at what time values are the two points in same position in say x dimension then,
            # p1.x + v1.x * t + a1.x * (t * (t + 1))/2) = p2.x + v2.x * t + a2.x * (t * (t + 1))/2)
            solutions = []
            eps = 1e-6
            bsq_4ac = (_b * _b) - (4 * _a * _c)
            two_a = 2 * _a
            minus_b = -_b
            if bsq_4ac < 0 or two_a == 0:
                return solutions

            sol1 = float(minus_b + (bsq_4ac ** 0.5)) / float(two_a)
            sol2 = float(minus_b - (bsq_4ac ** 0.5)) / float(two_a)
            if sol1 >= 0 and abs(sol1 - int(sol1)) < eps:
                solutions.append(int(sol1))

            if sol2 >= 0 and abs(sol2 - int(sol2)) < eps:
                solutions.append(int(sol2))

            return solutions

        collisions = []
        a1, b1, c1 = self.path_coeffs
        a2, b2, c2 = other_point.path_coeffs
        a, b, c = a1.sub(a2), b1.sub(b2), c1.sub(c2)
        xsols = _get_real_postive_int_solutions(a.x, b.x, c.x)
        ysols = _get_real_postive_int_solutions(a.y, b.y, c.y)
        zsols = _get_real_postive_int_solutions(a.z, b.z, c.z)

        for (tx, ty, tz) in itertools.product(xsols, ysols, zsols):
            if tx == ty and tx == tz:
                collisions.append(tx)

        return collisions

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

    all_collisions = collections.defaultdict(list)
    still_alive = [True for _ in points]
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            for t in points[i].get_collisions(points[j]):
                all_collisions[t].append((i, j,))

    times = sorted(all_collisions.keys())
    for t in times:
        kill_points = set()
        for i, j in all_collisions[t]:
            if still_alive[i] and still_alive[j]:
                kill_points.add(i)
                kill_points.add(j)

        for point_ind in kill_points:
            still_alive[point_ind] = False

    print(still_alive.count(True))


if __name__ == '__main__':
    main()
