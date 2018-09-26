import collections

import queue
import sys


def main():
    graph = collections.defaultdict(set)
    visited = collections.defaultdict(int)
    for line in sys.stdin:
        parts = line.strip().split(' <-> ')
        parent = int(parts[0].strip())
        if len(parts) > 1:
            for child in map(int, map(str.strip, parts[1].strip().split(', '))):
                graph[parent].add(child)
                graph[child].add(parent)

    ans = 0
    for rnode in graph:
        if not visited[rnode]:
            ans += 1
            q = queue.Queue()
            q.put(rnode)
            while not q.empty():
                node = q.get()
                visited[node] = 1
                for child in graph[node]:
                    if not visited[child]:
                        q.put(child)
    print(ans)


if __name__ == '__main__':
    main()
