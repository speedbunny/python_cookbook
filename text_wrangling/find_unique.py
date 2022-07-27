#Remove duplicates including duplicated values and leave uniques 
    tally = dict()

    for x in my_array:
        try:
            del tally[x]
        except KeyError:
            tally[x] = 1
#  FOR ONE UNIQUE 
#   for key, value in tally.items():
#    return(key)
