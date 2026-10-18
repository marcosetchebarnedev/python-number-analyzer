import csv
import re
import statistics

raw = input("Enter the numbers separated by commas or spaces: ")
numbers = [float(t) for t in re.split(r"[,\s]+", raw.strip()) if t]

average = statistics.mean(numbers)
median = statistics.median(numbers)
maximum = max(numbers)
minimum = min(numbers)

with open("number_analysis.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    # per-number analysis
    writer.writerow(["number", "diff_from_average", "comment"])

    for n in numbers:
        if n == maximum:
            comment = "This is the maximum number."
        elif n == minimum:
            comment = "This is the minimum number."
        elif n > average:
            comment = "This number is above the average."
        elif n < average:
            comment = "This number is below the average."
        else:
            comment = "This number is equal to the average."
        writer.writerow([n, round(n - average, 2), comment])

        # list summary
        writer.writerow([])
        writer.writerow(["metric", "value"])
        writer.writerows([
            ["count", len(numbers)],
            ["sum", sum(numbers)],
            ["average", round(average, 2)],
            ["median", round(median, 2)],
            ["maximum", maximum],
            ["minimum", minimum],
            ["range", maximum - minimum],
            ["std_dev", round(statistics.pstdev(numbers), 2)]
        ])

        print("Analysis complete. Results saved to 'number_analysis.csv'.")