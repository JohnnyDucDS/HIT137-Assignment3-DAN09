
password = list(input("What is your password: "))
length = len(password)
has_digit = '0123456789'
#has_digit = [0,1,2,3,4,5,6,7,8,9]

#Conditon to check has digit and upper
for i in password:
    if i in has_digit:
        found_digit = True
if found_digit and 3>1:
    print('weak password')



