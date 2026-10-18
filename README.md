# Number Analyzer

A simple Python 3 program with no external dependencies or Google account access.
It sorts numbers and exports statistics to a CSV that you can import into Google Sheets.

## Run in VS Code

1. Open this folder in VS Code.
2. Open `analyzer.py` and select **Run Python File in Terminal** (▶️).
3. Enter a list such as `8, 2, 5, 2, -1, 3.5` and press Enter.
4. The program creates `result.csv` next to the script. Each run overwrites that file.

Alternatively, run these commands from this folder:

```sh
python3 analyzer.py
```

Pass numbers directly and choose an output filename:

```sh
python3 analyzer.py --numbers "8, 2, 5, 2, -1, 3.5" --output my_result.csv
```

Commas, spaces, and semicolons are accepted as separators. Square brackets are optional:
`[8, 2, 5]`. **Use a period for decimals:** `3.5`. The input `3,5` means two numbers.
Negative numbers and duplicates are supported. Empty lists, text, NaN, and infinity are rejected.
The program uses Python floating-point numbers, suitable for everyday calculations;
it does not preserve arbitrary precision for very large integers or decimals.

## Open the output in Google Sheets

1. Open a spreadsheet in [Google Sheets](https://sheets.google.com).
2. Select **File > Import > Upload** and select the generated CSV.
3. Choose **Detect automatically** or **Comma** as the separator and enable number conversion.

The CSV uses decimal points. To ensure decimal values are interpreted correctly,
set **File > Settings > Locale > United States** before importing.

## File contents

- Columns A and B: original input and numbers sorted in ascending order.
- Columns D and E: count, sum, average, median, minimum, maximum, range, modes,
  distinct value count, variance, and standard deviation.
- Columns G and H: each distinct number and its frequency.

Variance and standard deviation are **population** measures (divide by N).
All modes are shown when repeated values tie for the highest frequency.
If no value repeats, the program reports no mode.
The CSV contains calculated values, not formulas. Editing numbers in Google Sheets
does not recalculate the statistics; rerun the program with the updated list.

`example.csv` contains the output for `8, 2, 5, 2, -1, 3.5`:
average **3.25**, median **2.75**, and mode **2**.

## Quick checks and debugging

```sh
python3 analyzer.py --numbers "7"
python3 analyzer.py --numbers "1, 1, 2, 2"
python3 analyzer.py --numbers ""
python3 analyzer.py --numbers "hello, 2"
```

The last two commands should report an error and exit with status 1.

Run the automated tests:

```sh
python3 -m unittest -v
```

Debug step by step:

```sh
python3 -m pdb analyzer.py --numbers "8, 2, 5, 2"
```

In `pdb`, use `n` for the next line, `s` to step into a function,
`p numbers` to inspect that variable once defined, `c` to continue, and `q` to quit.
