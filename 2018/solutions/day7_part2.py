import collections
import queue
import re
import sys
import time
from typing import Iterable, Dict, Set, List, Optional, NamedTuple, Tuple

input_pattern = re.compile(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin.')


class Job(NamedTuple):
    name: str
    timeout: int


class Thread(object):
    def __init__(self):
        self.available: bool = True
        self.job: Optional[Job] = None
        self._timeout: int = 0
        self._time = 0

    def assign(self, job: Job):
        self.job = job
        self._timeout = job.timeout
        self.available = False

    def tick(self) -> Tuple[Optional[Job], bool]:
        self._time += 1
        if self._timeout > 0:
            self._timeout -= 1
            if self._timeout == 0:
                self.available = True
                last_job = self.job
                self.job = None
                return last_job, self.available

        return self.job, self.available


class ThreadPoolExecutor(object):
    def __init__(self, num_threads):
        self.time = 0
        self.threads: List[Thread] = [Thread() for _ in range(num_threads)]

    def threads_available_status(self) -> Iterable[bool]:
        return [thread.available for thread in self.threads]

    def tick(self, jobs_queue: queue.PriorityQueue) -> List[Job]:
        self.time += 1
        for thread in self.threads:
            if thread.available:
                if not jobs_queue.empty():
                    job = jobs_queue.get()
                    thread.assign(job=job)

        finished_jobs = []
        for thread in self.threads:
            previous_job_on_thread, thread_is_free = thread.tick()

            if thread_is_free and previous_job_on_thread:
                finished_jobs.append(previous_job_on_thread)
        return finished_jobs


class Graph(object):
    def __init__(self):
        self.data: Dict[str, Set[str]] = collections.defaultdict(set)
        self.vertices = set()

    def add_edge(self, first: str, second: str):
        self.vertices.add(first)
        self.vertices.add(second)
        self.data[first].add(second)

    def execute_topological_order(self, num_threads: int, job_prefix_time: int = 60) -> int:
        q: queue.PriorityQueue = queue.PriorityQueue()
        in_degree: Dict[str, int] = {v: 0 for v in self.vertices}
        for i in self.data:
            for j in self.data[i]:
                in_degree[j] += 1

        for v in self.vertices:
            if not in_degree[v]:
                job = Job(name=v, timeout=job_prefix_time + ord(v) - ord('A') + 1)
                q.put(job)

        executor = ThreadPoolExecutor(num_threads=num_threads)
        while True:
            finished_jobs = executor.tick(jobs_queue=q)
            for job in finished_jobs:
                u = job.name
                for v in self.data[u]:
                    in_degree[v] -= 1
                    if not in_degree[v]:
                        q.put(Job(name=v, timeout=job_prefix_time + ord(v) - ord('A') + 1))

            if q.empty() and all(executor.threads_available_status()):
                break

        return executor.time


def solve(input_iter: Iterable[str], num_threads: int = 5, job_prefix_time: int = 60) -> int:
    graph = Graph()
    for line in input_iter:
        line = line.strip()
        match = input_pattern.search(line)
        if match:
            first, second = match.group(1), match.group(2)
            graph.add_edge(first=first, second=second)
        else:
            raise ValueError('Invalid input')

    return graph.execute_topological_order(num_threads=num_threads, job_prefix_time=job_prefix_time)


def run_tests():
    tests = [
        '''Step C must be finished before step A can begin.
        Step C must be finished before step F can begin.
        Step A must be finished before step B can begin.
        Step A must be finished before step D can begin.
        Step B must be finished before step E can begin.
        Step D must be finished before step E can begin.
        Step F must be finished before step E can begin.'''.split('\n'),

    ]

    answers = [
        15,
    ]

    for i, (test, answer) in enumerate(zip(tests, answers), start=1):
        print('Running test: {}/{}'.format(i, len(tests)))
        start = time.time()
        computed = solve(test, num_threads=2, job_prefix_time=0)
        end = time.time()
        assert computed == answer, (test, answer, computed)
        print('OK. Took {:.2f}'.format(end - start))


if __name__ == '__main__':
    run_tests()
    print(solve(sys.stdin))
