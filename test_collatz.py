import unittest

from collatz import max_value, records, step, stopping_time, trajectory, verify


class CollatzTests(unittest.TestCase):
    def test_step(self):
        self.assertEqual(step(1), 4)
        self.assertEqual(step(2), 1)
        self.assertEqual(step(3), 10)

    def test_trajectory(self):
        self.assertEqual(trajectory(6), [6, 3, 10, 5, 16, 8, 4, 2, 1])

    def test_stopping_time(self):
        self.assertEqual(stopping_time(1), 0)
        self.assertEqual(stopping_time(6), 8)
        self.assertEqual(stopping_time(27), 111)

    def test_max_value(self):
        self.assertEqual(max_value(6), 16)
        self.assertEqual(max_value(27), 9232)

    def test_verify(self):
        self.assertTrue(verify(1000))

    def test_records(self):
        self.assertEqual(
            [(item.n, item.stopping_time) for item in records(10)],
            [(1, 0), (2, 1), (3, 7), (6, 8), (7, 16), (9, 19)],
        )

    def test_rejects_non_positive(self):
        for function in (step, trajectory, stopping_time, max_value, verify, records):
            with self.subTest(function=function.__name__):
                with self.assertRaises(ValueError):
                    function(0)


if __name__ == "__main__":
    unittest.main()
