#sensitivity and specificity of test results
#test_A is the set of results
#test_B is the set of outcomes

test_A = [0,1,1,1,0,0,0,1,1]
test_B = [1,1,0,0,0,0,1,0,1]
q = True


true_positive = 0
false_positive = 0
false_negative = 0
true_negative = 0
number_of_elements = len(test_A)
counter = 0

while counter < number_of_elements:
    x=test_A[counter]
    y=test_B[counter]
    if y == 1:
       
            if x == 1:
             true_positive = true_positive + 1
            else:
             false_positive = false_positive + 1
    else:
            if x == 0:
             true_negative =  true_negative + 1
            else:
             false_negative = false_negative + 1  

    counter = counter + 1
     
sensitivity = true_positive / (true_positive + false_negative)
specificity = true_negative / (false_positive + true_negative)

if q == False:
    print(sensitivity)
else:
    print(specificity)
