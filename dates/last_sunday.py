import datetime

#LAST SUNDAY FUNCTION - REUSABLE
def lastsun(input):
    d = input.toordinal()
    last = d - 6
    sunday = last - (last % 7)
    sunday_date = datetime.date.fromordinal(sunday) + datetime.timedelta(days=7)
    return(sunday_date)

today = datetime.date.today()
end_date = lastsun(today)
print(end_date)
