"""Read timestamp strings from a file, and convert them to datetime objects.

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


def get_ts_string_parser(line):
    """Parse string manually."""
    year, month, day = int(line[:4]), int(line[5:7]), int(line[8:10])
    hour, minute = int(line[11:13]), int(line[14:])

    return datetime(year=year, month=month, day=day, hour=hour, minute=minute)

def get_ts_regex(line, ts_pattern):
    """Parse string using a regex."""
    m = ts_pattern.match(line)
    # year, month, day = int(m.group(1)), int(m.group(2)), int(m.group(3))
    # hour, minute = int(m.group(4)), int(m.group(5))
    year, month, day, hour, minute = m.group(1, 2, 3, 4, 5)
    year, month, day = int(year), int(month), int(day)
    hour, minute = int(hour), int(minute)

    return datetime(year=year, month=month, day=day, hour=hour, minute=minute)


print("Reading data from file...")
with open('data_file.txt') as f:
    lines = f.readlines()
lines = [line.rstrip() for line in lines]
print(f"  Found {len(lines)} timestamp strings.")


print("\nProcessing timestamps...")
start = perf_counter()

if parse_method == 'strptime':
    timestamps = [datetime.strptime(line, "%Y-%m-%d %H:%M") for line in lines]
elif parse_method == 'string-parsing':
    timestamps = [get_ts_string_parser(line) for line in lines]
elif parse_method == 'regex':
    ts_pattern = re.compile(
            '([\d]{4})-([\d]{2})-([\d]{2}) ([\d]{2}):([\d]{2})')
    timestamps = [get_ts_regex(line, ts_pattern) for line in lines]
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


print("\nVerify conversion:")
for line, ts in zip(lines[:3], timestamps[:3]):
    try:
        print(f"  {line} -> {ts.isoformat()}")
    except AttributeError:
        print(f"  {line} -> {np.datetime_as_string(ts)}")