import csv
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("analyze-number-script.py")


class AnalyzeNumberScriptTests(unittest.TestCase):
    def analyze(self, input_text):
        with tempfile.TemporaryDirectory() as temporary_directory:
            result = subprocess.run(
                [sys.executable, str(SCRIPT)],
                input=input_text,
                text=True,
                capture_output=True,
                cwd=temporary_directory,
                check=True,
            )

            with Path(temporary_directory, "number_analysis.csv").open(
                newline="", encoding="utf-8"
            ) as csvfile:
                rows = list(csv.reader(csvfile))

        self.assertIn("Analysis complete.", result.stdout)
        return rows

    def test_writes_expected_summary(self):
        self.assertEqual(
            self.analyze("1 2 3 4 5 6 7 8 9\n"),
            [
                ["metric", "value"],
                ["count", "9"],
                ["sum", "45.0"],
                ["average", "5.0"],
                ["median", "5.0"],
                ["maximum", "9.0"],
                ["minimum", "1.0"],
                ["range", "8.0"],
            ],
        )

    def test_handles_negative_decimals_and_mixed_separators(self):
        self.assertEqual(
            self.analyze("-12.5, 0, 3.75; 100.25 -4\n"),
            [
                ["metric", "value"],
                ["count", "5"],
                ["sum", "87.5"],
                ["average", "17.5"],
                ["median", "0.0"],
                ["maximum", "100.25"],
                ["minimum", "-12.5"],
                ["range", "112.75"],
            ],
        )

    def test_handles_even_count_of_fractional_numbers(self):
        self.assertEqual(
            self.analyze("-10.5; -2.5, 4.25 11.75\n"),
            [
                ["metric", "value"],
                ["count", "4"],
                ["sum", "3.0"],
                ["average", "0.75"],
                ["median", "0.875"],
                ["maximum", "11.75"],
                ["minimum", "-10.5"],
                ["range", "22.25"],
            ],
        )


if __name__ == "__main__":
    unittest.main()
