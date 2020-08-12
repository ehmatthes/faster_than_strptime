"""Read timestamp strings from file, and create datetime objects from them.

Timestamp format: "2016-02-09 15:45"
"""

import re, sys
from datetime import datetime
from dateutil.parser import parse
from time import perf_counter

import numpy as np
import pandas as pd
import arrow


try:
    parse_method = sys.argv[1]
except IndexError:
    parse_method = 'strptime'

parse_methods = ['strptime', 'string-parsing', 'regex', 'fromisoformat',
        'numpy', 'pandas', 'dateutil', 'arrow']

if parse_method not in parse_methods:
    print("The parsing method must be one of the following:")
    print(parse_methods)
    sys.exit()


def get_ts_simple_string_parser(line):
    """Parse string through string slicing."""
    year, month, day = int(line[:4]), int(line[5:7]), int(line[8:10])
    hour, minute = int(line[11:13]), int(line[14:])

    ts = datetime(year=year, month=month, day=day, hour=hour, minute=minute)
    return ts

def get_ts_regex(line):
    """Parse string using a regex."""
    ts_pattern = re.compile('([\d]{4})-([\d]{2})-([\d]{2}) ([\d]{2}):([\d]{2})')
    m = ts_pattern.match(line)
    year, month, day = int(m.group(1)), int(m.group(2)), int(m.group(3))
    hour, minute = int(m.group(4)), int(m.group(5))

    ts = datetime(year=year, month=month, day=day, hour=hour, minute=minute)
    return ts


input_file = 'data_file.txt'

print("Reading data from file...")
with open(input_file) as f:
    lines = f.readlines()
lines = [line.rstrip() for line in lines]
print(f"  Found {len(lines)} timestamp strings.")


print("\nProcessing timestamps...")
start = perf_counter()

if parse_method == 'strptime':
    timestamps = [datetime.strptime(line, "%Y-%m-%d %H:%M") for line in lines]
elif parse_method == 'string-parsing':
    timestamps = [get_ts_simple_string_parser(line) for line in lines]
elif parse_method == 'regex':
    timestamps = [get_ts_regex(line) for line in lines]
elif parse_method == 'fromisoformat':
    timestamps = [datetime.fromisoformat(line) for line in lines]
elif parse_method == 'numpy':
    timestamps = [np.datetime64(line) for line in lines]
elif parse_method == 'pandas':
    timestamps = pd.to_datetime(lines)
elif parse_method == 'dateutil':
    timestamps = [parse(line) for line in lines]
elif parse_method == 'arrow':
    timestamps = [arrow.get(line) for line in lines]

end = perf_counter()
processing_time = round(end - start, 2)
print(f"  Processed {len(timestamps)} in {processing_time} seconds.")


# Verify ts objects.
print("\nVerify timestamps:")
for line, ts in zip(lines[:5], timestamps[:5]):
    try:
        print(line, ts.isoformat())
    except AttributeError:
        print(line, np.datetime_as_string(ts))