import csv
import re
import statistics

raw = input("Enter numbers separated by commas or spaces: ")
numbers = [float(t) for t in re.split(r"[,\s;]+", raw.strip()) if t]

stats = {
    "count":len(numbers),
    "sum":sum(numbers),
    "average": round(statistics.mean(numbers), 2),
    "median": statistics.median(numbers),
    "maximum": max(numbers),
    "minimum": min(numbers),
    "range": max(numbers) - min(numbers)
}

with open("analysis.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["metric", "value"])
    writer.writerows(stats.items())

    print("saved to analysis.csv")