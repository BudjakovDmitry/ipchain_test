import os
import unittest

from main import convert_to_timestamp, get_start_finish, Call, TimeLine


class TestConvertToTimestamp(unittest.TestCase):
    input_ = '2021-01-30 22:18'

    def test_convert(self):
        required_output = 1612037880.0  # '2021-01-30 22:18' as a timestamp
        self.assertEqual(convert_to_timestamp(self.input_), required_output)

    def test_format(self):
        self.assertIsInstance(convert_to_timestamp(self.input_), float)


class TestGetStartFinish(unittest.TestCase):
    input_ = 'FROM:2021-01-30 22:18 TO:2021-01-30 22:31'

    def test_format(self):
        self.assertIsInstance(get_start_finish(self.input_), tuple)

    def test_start_format(self):
        start, _ = get_start_finish(self.input_)
        self.assertIsInstance(start, float)

    def test_finish_format(self):
        _, finish = get_start_finish(self.input_)
        self.assertIsInstance(finish, float)

    def test_start(self):
        start, _ = get_start_finish(self.input_)
        required_output = 1612037880.0  # '2021-01-30 22:18' as a timestamp
        self.assertEqual(start, required_output)

    def test_finish(self):
        _, finish = get_start_finish(self.input_)
        required_output = 1612038660.0  # '2021-01-30 22:31' as a timestamp
        self.assertEqual(finish, required_output)


class TestCall(unittest.TestCase):
    input = 'FROM:2021-01-30 22:18 TO:2021-01-30 22:31'

    def test_start(self):
        required_start = 1612037880.0  # '2021-01-30 22:18' as a timestamp
        call = Call(self.input)
        self.assertEqual(call.start, required_start)

    def test_finish(self):
        required_finish = 1612038660.0  # '2021-01-30 22:31' as a timestamp
        call = Call(self.input)
        self.assertEqual(call.finish, required_finish)


class TestTimeLine(unittest.TestCase):
    dataset_dir = os.path.join(os.getcwd(), 'test_datasets')

    def get_timeline(self, dataset: str):
        file = os.path.join(self.dataset_dir, dataset)
        tl = TimeLine()
        with open(file) as log:
            for line in log:
                tl.add_call(Call(line))
        return tl

    def test_set_1(self):
        tl = self.get_timeline('log1')
        self.assertEqual(tl.operators_required(), 1)

    def test_set_2(self):
        tl = self.get_timeline('log2')
        self.assertEqual(tl.operators_required(), 2)

    def test_set_3(self):
        tl = self.get_timeline('log3')
        self.assertEqual(tl.operators_required(), 3)


if __name__ == '__main__':
    unittest.main()
