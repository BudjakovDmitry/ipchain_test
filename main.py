"""
Это все, что удалось придумать за 2-3 часа.
Уже перед отправкой пришла идея, что можно было бы предварительно отсортировать лог в хронологическом порядке.
После этого можем работать с очередью входящих звонков, как только звонок выходит из очереди, забываем про него.
Минимальное количество операторов = максимальная длинна очереди за время измерения.

Примечание: если это возможно, я бы поменял формат лога, чтобы обойтись без регулярных выражений.
"""

from collections import defaultdict
from datetime import datetime
import os
import re


def convert_to_timestamp(date_and_time: str) -> float:
    """
    Convert input date and time string to timestamp
    :param date_and_time: expected format: "2021-01-30 22:18"
    """
    dt_object = datetime.strptime(date_and_time, '%Y-%m-%d %H:%M')
    return dt_object.timestamp()


def get_start_finish(call_log: str) -> tuple:
    """
    Extract call start datetime and finish datetime from log record.
    :param call_log: excepted log format: 'FROM:2021-01-30 22:18 TO:2021-01-30 22:31'
    :return: (start_timestamp, finish_timestamp)
    """
    pattern = r'FROM:(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) TO:(\d{4}-\d{2}-\d{2} \d{2}:\d{2})'
    search = re.search(pattern, call_log)
    if not search:
        return None, None
    start, finish = search.groups()
    return convert_to_timestamp(start), convert_to_timestamp(finish)


class Call:
    """Single call"""
    __slots__ = ('start', 'finish')

    def __init__(self, call_log: str):
        # expected call log format: 'FROM:2021-01-30 22:18 TO:2021-01-30 22:31'
        self.start, self.finish = get_start_finish(call_log)


class TimeLine:
    """Timeline which contains calls"""

    def __init__(self):
        self.__points: dict = defaultdict(int)  # {timestamp: amount_of_parallel_calls}
        self.__max_parallels_calls = 0  # max parallels calls on timeline

    def add_call(self, call_: Call) -> None:
        """
        Add new call on timeline
        :param call_: single call object
        """
        point = call_.start
        while point <= call_.finish:
            self.__points[point] += 1  # one more parallel call (+1 operator required)
            parallel_call = self.__points[point]
            if parallel_call > self.__max_parallels_calls:
                self.__max_parallels_calls = parallel_call  # update max value
            point += 1

    def operators_required(self) -> int:
        """Minimal operators required"""
        return self.__max_parallels_calls


def main(path_to_file: str) -> int:
    """How many operators required for this call log"""
    tl = TimeLine()
    with open(path_to_file) as log:
        for line in log:
            call = Call(line)
            tl.add_call(call)
    return tl.operators_required()


if __name__ == '__main__':
    operators = main(os.path.join('test_datasets', 'log1'))
    print(f"Operators required: {operators} ")
