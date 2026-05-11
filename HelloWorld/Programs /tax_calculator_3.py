#Tax_calculator3

import math


while True:
    income = float(input("Your total income in 2025 - 2026 finacial year:"))
    if income < 0:
        print("Invalid income")
    elif income < 18200:
        print("You don't have to pay tax")
    else:
        private_insurance = input("Do you have private insurance?(Y/N)))").upper()

        #1 Tax base
    if 18201 <= income <= 45000:
        tax_rate = (income - 18200) * 16/100
    elif 45001 <= income <= 135000:
        tax_rate = 4288 + ((income-45000) * 30/100)
    elif 135001 <= income <= 190000:
        tax_rate = 31288 + ((income-135000) * 37/100)
    elif income >= 190001:
        tax_rate = 51638 + ((income-190000) * 45/100)

        #2 Medicare levy 
    medicare_levy = income * 2/100 if private_insurance == "N" else 0
    aftertax_income = income - (tax_rate + medicare_levy)

        #3 Result
    print(f"Your income after is ${aftertax_income}")
    print(f"tax you have to pay is: ${tax_rate}")

    if medicare_levy > 0:
        print(f"Your medicare levy is: ${medicare_levy}")
    else:
        print("You are eligible for medicare levy exemption")

    next = input(f"Do you wan to continue (Y/N): ").upper()
    
    if next == "N":
        break 
    



