import unittest

from calculate_statistics import calculate_statistics, format_summary


class CalculateStatisticsTests(unittest.TestCase):
    def test_normal(self):
        r = calculate_statistics([1, 2, 3, 4, 5])
        self.assertEqual(r["total"], 15)
        self.assertEqual(r["count"], 5)
        self.assertEqual(r["average"], 3.0)
        self.assertEqual(r["maximum"], 5)
        self.assertEqual(r["minimum"], 1)
        self.assertTrue(r["positive"])

    def test_single_and_negative(self):
        r = calculate_statistics([-4])
        self.assertEqual((r["maximum"], r["minimum"]), (-4, -4))
        self.assertFalse(r["positive"])

    def test_empty(self):
        with self.assertRaises(ValueError):
            calculate_statistics([])

    def test_bad_types(self):
        for bad in ("123", None, [1, "a"], [True], 5):
            with self.assertRaises(TypeError):
                calculate_statistics(bad)

    def test_input_unchanged(self):
        data = [3, 1, 2]
        calculate_statistics(data)
        self.assertEqual(data, [3, 1, 2])

    def test_summary(self):
        s = format_summary(calculate_statistics([1, 2, 3]))
        self.assertEqual(s, "Avg: 2.0 Max: 3 Min: 1")

    def test_enhanced_stats(self):
        r = calculate_statistics([1, 2, 2, 3, 4])
        self.assertEqual(r["range"], 3)
        self.assertEqual(r["median"], 2)
        self.assertEqual(r["mode"], [2])
        self.assertAlmostEqual(r["variance"], 1.3)
        self.assertEqual((r["q1"], r["q3"], r["iqr"]), (2, 3, 1))
        self.assertEqual(r["outliers"], [])

    def test_outlier_detected(self):
        r = calculate_statistics([10, 11, 12, 11, 10, 500])
        self.assertEqual(r["outliers"], [500])

    def test_single_value_has_no_spread(self):
        r = calculate_statistics([7])
        self.assertIsNone(r["variance"])
        self.assertIsNone(r["std_dev"])
        self.assertEqual(r["outliers"], [])
        self.assertEqual(r["mode"], [7])


if __name__ == "__main__":
    unittest.main()
