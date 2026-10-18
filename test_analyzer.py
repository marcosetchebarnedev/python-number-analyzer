"""Run with: python3 -m unittest -v"""

import csv
import tempfile
import unittest
from pathlib import Path

from analyzer import calculate_statistics, export_csv, parse_numbers


class NumberAnalyzerTests(unittest.TestCase):
    def test_input_formats(self):
        self.assertEqual(parse_numbers("[8, 2; -1 3.5]"), [8, 2, -1, 3.5])

    def test_invalid_input(self):
        for text in ("", "[]", "hello, 2", "nan", "inf", "1e999"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_numbers(text)

    def test_known_statistics(self):
        summary = dict(calculate_statistics([8, 2, 5, 2, -1, 3.5]))
        self.assertEqual(summary["Average"], 3.25)
        self.assertEqual(summary["Median"], 2.75)
        self.assertEqual(summary["Minimum"], -1)
        self.assertEqual(summary["Maximum"], 8)
        self.assertEqual(summary["Mode(s)"], "2")
        self.assertEqual(summary["Population variance"], 7.8125)

    def test_single_value_and_multiple_modes(self):
        self.assertEqual(dict(calculate_statistics([7]))["Population variance"], 0)
        self.assertEqual(dict(calculate_statistics([1, 1, 2, 2]))["Mode(s)"], "1; 2")
        self.assertEqual(dict(calculate_statistics([1, 2]))["Mode(s)"],
                         "No mode (no repeated values)")

    def test_csv_output(self):
        with tempfile.TemporaryDirectory() as directory:
            path = export_csv([3, -1, 2, 2], Path(directory) / "result.csv")
            with path.open(encoding="utf-8-sig", newline="") as file:
                rows = list(csv.reader(file))
        self.assertEqual(rows[0][0], "Original input")
        self.assertEqual([float(row[1]) for row in rows[1:5]], [-1, 2, 2, 3])
        self.assertEqual(rows[2][6:8], ["2", "2"])
        self.assertTrue(all(len(row) == 8 for row in rows))


if __name__ == "__main__":
    unittest.main()
