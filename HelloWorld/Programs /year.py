year = int(input("Enter your birth year: "))
month = int(input("Enter your birth month: "))
    
    
    #month
if month ==1 or month == 3 or month == 5 or month == 7 or month == 8  or month == 10 or month == 12:
    print("31 days")
elif month == 4 or month == 6 or month == 9 or month == 11:
    print("30 days")
else:
    pass 
if year % 4 == 0 and (year % 100 != 0) and month == 2:
  print("29days")
else:
    pass 
    #year
if year % 4 == 0 and (year % 100 != 0):
  print("Leap year")
else:
  print("This is not leap year")