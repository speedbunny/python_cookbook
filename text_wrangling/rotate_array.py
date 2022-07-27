# A = array and K = number of rotations
def rotator(A, K):
    i = 0
    if A:
     while i < K:

        last = A[-1]
        A = A[:-1]
        A.insert(0, last)
        i=i+1
 
    
    return A
