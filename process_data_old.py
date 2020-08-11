"""Read timestamp strings from file, and create datetime objects from them.
"""

import re

from datetime import datetime
from dateutil.parser import parse

import numpy
import pandas as pd
import arrow


input_file = 'data_file.txt'

print("Reading data from file...")
with open(input_file) as f:
    lines = f.readlines()
lines = [line.rstrip() for line in lines]


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

def get_ts_fromisoformat(line):
    """Parse string using datetime.fromisoformat()."""
    return datetime.fromisoformat(line)

def get_ts_from_numpy(line):
    """Parse string using numpy.datetime64()."""
    return numpy.datetime64(line)

def get_ts_from_pandas(line):
    """Parse string using pandas.to_datetime()."""
    return pd.to_datetime(line)

def get_ts_from_arrow(line):
    """Parse string using arrow.get()."""
    return arrow.get(line)


def show_timestamps(lines, timestamps):
    """For verifying ts objects."""
    for line, ts in zip(lines[:5], timestamps[:5]):
        print(line, ts.isoformat())


print("Processing timestamps...")
# Parse strings like this: "2016-02-09 15:45"

# Using strptime:
#   6.96s at 500k; 13.93s at 1M
# timestamps = [datetime.strptime(line, "%Y-%m-%d %H:%M") for line in lines]

# Using simple string parsing:
#   1.33s at 500k; 2.68s at 1M
# timestamps = [get_ts_simple_string_parser(line) for line in lines]

# Using regex:
#   2.74s at 500k; 5.48s at 1M
# timestamps = [get_ts_regex(line) for line in lines]

# Using datetime.fromisoformat():
#   0.47s at 500k!!!
# timestamps = [get_ts_fromisoformat(line) for line in lines]

# Using numpy.datetime64():
#   0.60s at 500k
# timestamps = [get_ts_from_numpy(line) for line in lines]
# for line, ts in zip(lines[:5], timestamps[:5]):
#     print(numpy.datetime_as_string(ts))

# Using pandas.to_datetime():
#   69.28s at 500k
#   0.69s acting directly on list
# timestamps = [get_ts_from_pandas(line) for line in lines]
# timestamps = pd.to_datetime(lines)

# Using arrow.get():
#   60.76s at 500k
# timestamps = [get_ts_from_arrow(line) for line in lines]

# dateutil
#   56.57s at 500k
timestamps = [parse(line) for line in lines]


print(f"Processed {len(timestamps)} timestamps.")

# show_timestamps(lines, timestamps)