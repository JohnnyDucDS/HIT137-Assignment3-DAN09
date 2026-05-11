password = list(input("What is your password: "))
length = len(password)
has_digit = {'0','1','2','3','4','5','6','7','8','9'}
has_upper = {'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'}

#Conditon to check has digit and upper
for i in password:
    if i in has_digit:
        found_digit = True
    if i in has_upper:
        found_upper = True

#Result
if length > 10 and found_digit and found_upper:
    print('strong password')
elif length >= 6 and length <= 10 and found_digit: # Fixed the 6 and 10 gap here!
    print('medium password')
else:
    print('weak password')