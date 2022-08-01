my_array = ("milk","bread","cheese","cheese","bread")
def tally(array):
 tally = dict()
 for x in my_array:
        try:
           del tally[x]
        except KeyError:
            tally[x] = 1

 for key, value in tally.items():
        return(key)
print(tally(my_array))
