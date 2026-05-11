grade = int(input("Enter your grade: "))
if grade > 100:
  print("Invalid")
elif 85 <= grade <= 100:
  print("HD")
elif grade >= 75:
  print("D")
elif grade >= 65:
  print("C")
elif grade >= 50:
  print("P")
else:
  print("F")