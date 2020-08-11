"""Read timestamp strings from file, and create datetime objects from them.

Timestamp format: "2016-02-09 15:45"
"""

import re
from datetime import datetime
from dateutil.parser import parse

import numpy as np
import pandas as pd
import arrow


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


print("Processing timestamps...")

# Using strptime:
# timestamps = [datetime.strptime(line, "%Y-%m-%d %H:%M") for line in lines]

# Using manual string parsing:
# timestamps = [get_ts_simple_string_parser(line) for line in lines]

# Using regex:
# timestamps = [get_ts_regex(line) for line in lines]

# Using datetime.fromisoformat():
# timestamps = [datetime.fromisoformat(line) for line in lines]

# Using numpy.datetime64():
# timestamps = [np.datetime64(line) for line in lines]

# Using pandas.to_datetime():
# timestamps = pd.to_datetime(lines)

# Using dateutil:
# timestamps = [parse(line) for line in lines]

# USing arrow.get()
timestamps = [arrow.get(line) for line in lines]


# Verify ts objects.
for line, ts in zip(lines[:5], timestamps[:5]):
    try:
        print(line, ts.isoformat())
    except AttributeError:
        print(line, np.datetime_as_string(ts))