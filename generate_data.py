"""Generate the specified number of timestamp strings."""

import sys

from random import choice


try:
    num_data_points = int(sys.argv[1])
except IndexError:
    num_data_points = 100_000

# Generate strings in this format: "2016-02-09 15:45"

# Keep everything two digits except year.
years = range(1900, 2020)
months = range(10, 13)
days = range(10, 29)
hours = range(10, 24)
seconds = range(10, 60)

def get_ts_string():
    year, month, day = choice(years), choice(months), choice(days)
    hour, second = choice(hours), choice(seconds)
    ts = f"{year}-{month}-{day} {hour}:{second}\n"
    return ts

print("Building strings...")
ts_strings = [get_ts_string() for _ in range(num_data_points)]

print("Writing strings to file...")
with open('data_file.txt', 'w') as f:
    f.writelines(ts_strings)

print(f"Wrote {len(ts_strings)} to file.")