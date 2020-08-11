"""Read timestamp strings from file, and create datetime objects from them.

Timestamp format: "2016-02-09 15:45"
"""

from datetime import datetime


input_file = 'data_file.txt'

print("Reading data from file...")
with open(input_file) as f:
    lines = f.readlines()
lines = [line.rstrip() for line in lines]

print("Processing timestamps...")


# Using strptime:
timestamps = [datetime.strptime(line, "%Y-%m-%d %H:%M") for line in lines]


"""Verify ts objects."""
for line, ts in zip(lines[:5], timestamps[:5]):
    print(line, ts.isoformat())