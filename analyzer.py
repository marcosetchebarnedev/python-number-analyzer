"""Sort numbers and generate a CSV for Google Sheets. No external dependencies."""

import argparse
import csv
import math
import re
import statistics
from collections import Counter
from pathlib import Path


def parse_numbers(text):
    """Accept 5, 2, -1, 3.5 or [5, 2, -1, 3.5]. Use a decimal point."""
    text = text.strip()
    # Remove optional brackets so both "1, 2" and "[1, 2]" work.
    if text.startswith("[") and text.endswith("]"):
        text = text[1:-1]
    # Split on commas, semicolons, or whitespace; float() converts each piece.
    parts = re.split(r"[,;\s]+", text.strip())
    if not text.strip():
        raise ValueError("Enter at least one number.")
    try:
        numbers = [float(part) for part in parts]
    except ValueError:
        raise ValueError("Use only numbers separated by commas or spaces; use a decimal point.") from None
    # float() accepts NaN and infinity, but these are not useful input here.
    if not all(math.isfinite(n) for n in numbers):
        raise ValueError("Numbers must be finite: NaN and infinity are not allowed.")
    return numbers


def calculate_statistics(numbers):
    """Treat the list as the entire population when calculating dispersion."""
    frequencies = Counter(numbers)  # Map each number to how often it appears.
    highest_frequency = max(frequencies.values())
    # Keep every tied mode instead of choosing just one.
    modes = sorted(n for n, frequency in frequencies.items() if frequency == highest_frequency)
    mode = (
        "No mode (no repeated values)"
        if highest_frequency == 1
        else "; ".join(f"{n:g}" for n in modes)
    )
    return [
        ("Count", len(numbers)),
        ("Sum", math.fsum(numbers)),
        ("Average", statistics.mean(numbers)),
        ("Median", statistics.median(numbers)),  # Middle value, or average of the middle pair.
        ("Minimum", min(numbers)),
        ("Maximum", max(numbers)),
        ("Range (maximum - minimum)", max(numbers) - min(numbers)),
        ("Mode(s)", mode),
        ("Distinct values", len(frequencies)),
        # Population measures treat this list as the complete dataset, not a sample.
        ("Population variance", statistics.pvariance(numbers)),
        ("Population standard deviation", statistics.pstdev(numbers)),
    ]


def export_csv(numbers, destination):
    sorted_numbers = sorted(numbers)  # Create a sorted copy; preserve the original order.
    summary = calculate_statistics(numbers)
    frequencies = sorted(Counter(numbers).items())
    # Reject non-finite statistics caused by extreme input values.
    if any(isinstance(v, (float, int)) and not math.isfinite(v) for _, v in summary):
        raise ValueError("Values are too large to calculate the statistics.")
    destination = Path(destination).expanduser()
    destination.parent.mkdir(parents=True, exist_ok=True)  # Create missing output folders.
    # UTF-8 with BOM also supports opening the file in Excel.
    with destination.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        # Arrange three tables side by side, with blank columns between them.
        writer.writerow([
            "Original input", "Sorted in ascending order", "",
            "Statistic", "Value", "", "Number", "Frequency",
        ])
        # Use enough rows for both the input list and the statistics table.
        # Fill shorter tables with empty cells to keep all columns aligned.
        for i in range(max(len(numbers), len(summary))):
            original = numbers[i] if i < len(numbers) else ""
            sorted_number = sorted_numbers[i] if i < len(sorted_numbers) else ""
            metric, value = summary[i] if i < len(summary) else ("", "")
            number, frequency = frequencies[i] if i < len(frequencies) else ("", "")
            writer.writerow([original, sorted_number, "", metric, value, "", number, frequency])
    return destination.resolve()


def main():
    # argparse handles command-line options and generates the --help screen.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--numbers", help='Example: --numbers "8, 2, 5, 2, -1, 3.5"')
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "result.csv",
                        help="CSV path (default: result.csv next to the script).")
    args = parser.parse_args()
    try:
        # Use --numbers when provided; otherwise ask for input in the terminal.
        text = args.numbers if args.numbers is not None else input(
            "Enter numbers separated by commas or spaces (use a decimal point):\n> "
        )
        numbers = parse_numbers(text)
        destination = export_csv(numbers, args.output)
    # Report invalid input or file errors without displaying a Python traceback.
    except (ValueError, OverflowError, OSError) as error:
        parser.exit(1, f"Error: {error}\n")
    except (EOFError, KeyboardInterrupt):
        parser.exit(1, "\nInput canceled.\n")
    # The :g format displays values such as 2.0 as 2 for readable terminal output.
    print("\nSorted:", ", ".join(f"{n:g}" for n in sorted(numbers)))
    for name, value in calculate_statistics(numbers):
        print(f"{name}: {value}")
    print(f"\nFile created: {destination}")
    print("In Google Sheets: File > Import > Upload, then select this CSV.")


# Run the interactive program only when executed directly, not when imported by tests.
if __name__ == "__main__":
    main()
