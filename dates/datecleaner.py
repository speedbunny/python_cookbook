import pandas as pd
import re
from contextlib import suppress

#Reusable Date Cleaner - SE
def cleanup(date):
    date = date.strip()
    #Common errors
    date = date.replace("!", "0")
    date = date.replace("//", "/")
    date = date.replace("1900", "2021")
    date = date.replace("Thu ","")
    date = date.replace("Fri ","")
    date = date.replace("Sat ","")
    date = date.replace("Sun ","")
    date = date.replace("Mon ","")
    date = date.replace("Tue ","")
    date = date.replace("Wed ","")
    date = date.replace(" June ","/06/")
    date = date.replace(" June ","/07/")
    date = date.replace("rd","")
    date = date.replace("th","")
    #Incorrect in 2021
    date = date.replace("2020", "2021")
    date = date.replace("2022", "2021")
    date = date.replace("2023", "2021")
    date = date.replace("2024", "2021")
    date = date.replace("2025", "2021")
    date = date.replace("2026", "2021")
    #Dataset specific errors
    date = date.replace("22021", "2021")
    date = date.replace("20021", "2021")
    date = date.replace("21021", "2021")
    date = date.replace("20201", "2021")
    date = date.replace("062021", "06/2021")
    date = date.replace("10 Jun","2021-06-10")
    date = date.replace("Thu","")
    date = date.replace("20217", "2021")
    date = date.replace("109/", "19")
    #An awkward one
    date = date.replace("202", "2021")
    date = date.replace("20211", "2021")
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
