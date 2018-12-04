import collections
import datetime
import operator
import re
import sys
from typing import Iterable, NamedTuple, List, Dict

timestamp_pattern = re.compile(r'\[(\d\d\d\d)-(\d\d)-(\d\d) (\d\d):(\d\d)\]')
begin_shift = re.compile(r'Guard #(\d+) begins shift')
fall_asleep = 'falls asleep'
wake_up = 'wakes up'


def parse_datetime(line: str) -> datetime.datetime:
    match = timestamp_pattern.search(line)
    if match:
        dyy, dmm, ddd, thh, tmm = [int(x) for x in match.groups()]
    else:
        raise ValueError('invalid input')
    return datetime.datetime(year=dyy, month=dmm, day=ddd, hour=thh, minute=tmm)


class Log(NamedTuple):
    timestamp: datetime.datetime
    line: str

    @staticmethod
    def from_line(line: str):
        return Log(timestamp=parse_datetime(line), line=line)


class Span(NamedTuple):
    guard_id: int
    start_minute: int
    end_minute: int


def parse_group(logs: List[Log]) -> List[Span]:
    match = begin_shift.search(logs[0].line)

    if match:
        guard_id = int(match.group(1))
    else:
        raise ValueError('invalid input')

    spans: List[Span] = []
    for i in range(1, len(logs), 2):
        if logs[i].line.endswith(fall_asleep) and logs[i + 1].line.endswith(wake_up):
            spans.append(
                Span(guard_id=guard_id, start_minute=logs[i].timestamp.minute, end_minute=logs[i + 1].timestamp.minute)
            )
        else:
            raise ValueError('invalid input')

    return spans


def solve(input_iter: Iterable[str]) -> int:
    logs: List[Log] = []
    for line in input_iter:
        line = line.strip()
        logs.append(Log.from_line(line))

    logs.sort(key=operator.attrgetter('timestamp'))

    spans: List[Span] = []
    start = 0
    for i, log in enumerate(logs[1:], 1):
        if begin_shift.search(log.line):
            spans.extend(parse_group(logs[start: i]))
            start = i
    spans.extend(parse_group(logs[start:]))
    guards_sleep_map: Dict[int, List[int]] = collections.defaultdict(lambda: [0 for _ in range(60)])

    for span in spans:
        for i in range(span.start_minute, span.end_minute):
            guards_sleep_map[span.guard_id][i] += 1

    guard_id, guard_map = max(guards_sleep_map.items(), key=lambda pair: sum(pair[1]))
    return guard_id * guard_map.index(max(guard_map))


def run_tests():
    tests = [
        '''[1518-11-01 00:00] Guard #10 begins shift
           [1518-11-01 00:05] falls asleep
           [1518-11-01 00:25] wakes up
           [1518-11-01 00:30] falls asleep
           [1518-11-01 00:55] wakes up
           [1518-11-01 23:58] Guard #99 begins shift
           [1518-11-02 00:40] falls asleep
           [1518-11-02 00:50] wakes up
           [1518-11-03 00:05] Guard #10 begins shift
           [1518-11-03 00:24] falls asleep
           [1518-11-03 00:29] wakes up
           [1518-11-04 00:02] Guard #99 begins shift
           [1518-11-04 00:36] falls asleep
           [1518-11-04 00:46] wakes up
           [1518-11-05 00:03] Guard #99 begins shift
           [1518-11-05 00:45] falls asleep
           [1518-11-05 00:55] wakes up'''.split('\n')
    ]

    answers = [
        240
    ]

    for test, answer in zip(tests, answers):
        computed = solve(test)
        assert computed == answer, (test, answer, computed)


if __name__ == '__main__':
    run_tests()
    print(solve(sys.stdin))
