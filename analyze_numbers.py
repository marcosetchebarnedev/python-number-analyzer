# analyze_numbers.py
import argparse
import csv
import math
import statistics
from collections import Counter


def main():
    parser = argparse.ArgumentParser(description="Analyze numbers and write the results to CSV.")
    parser.add_argument("numbers", nargs="+", help="Numbers separated by spaces or commas")
    parser.add_argument("-o", "--output", default="analysis.csv", help="Output CSV path")
    args = parser.parse_args()

    try:
        values = [float(part.strip()) for item in args.numbers for part in item.split(",")]
        if not values or not all(math.isfinite(value) for value in values):
            raise ValueError
    except ValueError:
        parser.error("Provide finite numeric values, such as: 1 2 3 or 1,2,3")

    counts = Counter(values)
    highest_count = max(counts.values())
    modes = sorted(value for value, count in counts.items() if count == highest_count)

    summary = [
        ("count", len(values)),
        ("sum", sum(values)),
        ("average", statistics.mean(values)),
        ("median", statistics.median(values)),
        ("mode", "; ".join(map(str, modes))),
        ("minimum", min(values)),
        ("maximum", max(values)),
        ("range", max(values) - min(values)),
        ("population_stddev", statistics.pstdev(values)),
        ("sample_stddev", statistics.stdev(values) if len(values) > 1 else ""),
    ]

    with open(args.output, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["type", "metric_or_value", "value", "frequency"])

        for metric, value in summary:
            writer.writerow(["summary", metric, value, ""])

        for value, frequency in sorted(counts.items()):
            writer.writerow(["frequency", "", value, frequency])


if __name__ == "__main__":
    main()