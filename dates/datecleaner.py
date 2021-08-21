import pandas as pd
import re
from contextlib import suppress

def cleanup(date):
    with suppress(ValueError):
        return str(int(date))

    for pattern, formater in PATTERNS:
        match = pattern.match(date)
        if match is not None:
               return formater.format(*match.groups())
    return date

PATTERNS = [
    ## Dotted dates ##
    # 1) 26.03.83 => 2083-03-31
    (re.compile(r'(\d{1,2}).(\d{1,2}).(\d{2})$'), '20{2:0>2}-{1:0>2}-{0}'),
    # 2) 20.06.2021 => 2021-06-20
    (re.compile(r'(\d{1,2}).(\d{1,2}).(\d{4})$'), '{2}-{1:0>2}-{0:0>2}'),
    ## Strip time ##
    # 3) 2021-6-14 00:00 => 2021-06-14
    (re.compile(r'(\d{4})-(\d{1,2})-(\d{1,2}) 00:00:00'),
        '{0}-{1:0>2}-{2:0>2}'),
    ## Slash dates ##
    # 4) 31/03/1883 => 1883-03-31
    (re.compile(r'(\d{1,2})/(\d{1,2})/(\d{2})$'), '{0}-{1:0>2}-{2:0>2}'),
]

##USAGE

colnames = ['Date']
dates = pd.read_csv('tmp.csv', usecols=colnames)

datelist = dates.values.tolist()
cleaned = []

for date in datelist:
    clean = cleanup(date[0])
    cleaned.append(clean)
