#Weight converter
print("-" * 30)

weight = float(input("Enter your weight"))


while weight < 0:
  print("invalid weight/n please try again")
  weight = float(input("Enter your weight"))

unit = str.upper(input("(L)bs or (K)g:"))

if unit == "K":
  weight = weight * 2.205
  print(f"Your weight is: {round(weight)} LBs")


elif unit == "L":
  weight = weight / 2.205
  print(f"Your weight is: {round(weight)} Kg")

else:
  print("Invalid")