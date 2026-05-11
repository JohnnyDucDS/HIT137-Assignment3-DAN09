#Tax_calculator2
import math
income = float(input("Your total income in 2025 - 2026 finacial year:"))
private_insurance = str.upper(input("Do you have private insurance?(Y/N):"))

if  income <= 18200: 
    print("You do not have to pay tax")

elif 18201 <= income <= 45000 and (private_insurance == "N"):
    tax_rate = (income - 18200) * 16/100
    medicare_levy = income * 2/100
    aftertax_income = income - (tax_rate + medicare_levy)
    print(f"your income after tax is: ${aftertax_income}")
    print(f"tax you have to pay is: ${tax_rate}")
    print(f"you medicare levy is : ${medicare_levy}")

elif 18201 <= income <= 45000 and (private_insurance == "Y"):
    tax_rate = (income - 18200) * 16/100
    aftertax_income = income - tax_rate
    print(f"your income after tax is: ${aftertax_income}")
    print(f"tax you have to pay is: ${tax_rate}")
    print("You are eligible for medicare exemption")

elif 45001 <= income <= 135000 and (private_insurance == "N"):
    tax_rate = 4288 + ((income-45000) * 30/100)
    medicare_levy = income * 2/100
    aftertax_income = income - (tax_rate + medicare_levy)
    print(f"your income after tax is: ${aftertax_income}")
    print(f"tax you have to pay is: ${tax_rate}")
    print(f"you medicare levy is : ${medicare_levy}")

elif 45001 <= income <= 135000 and (private_insurance == "Y"):
    tax_rate = 4288 + ((income-45000) * 30/100)
    aftertax_income = income - tax_rate 
    print(f"your income after tax is: ${aftertax_income}")
    print(f"tax you have to pay is: ${tax_rate}")
    print("You are eligible for medicare exemption")

elif 135001 <= income <= 190000 and (private_insurance == "N"):
    tax_rate = 31288 + ((income-135000) * 37/100)
    medicare_levy = income * 2/100
    aftertax_income = income - (tax_rate + medicare_levy)
    print(f"your income after tax is: ${aftertax_income}")
    print(f"tax you have to pay is: ${tax_rate}")
    print(f"you medicare levy is : ${medicare_levy}")

elif 135001 <= income <= 190000 and (private_insurance == "Y"):
    tax_rate = 31288 + ((income-135000) * 37/100)
    aftertax_income = income - tax_rate
    print(f"your income after tax is: ${aftertax_income}")
    print(f"tax you have to pay is: ${tax_rate}")
    print("You are eligible for medicare exemption")


elif income >= 190001 and (private_insurance == "N"):
    tax_rate = 51638 + ((income-190000) * 45/100)
    medicare_levy = income * 2/100
    aftertax_income = income - (tax_rate + medicare_levy)
    print(f"your income after tax is: ${aftertax_income}")
    print(f"tax you have to pay is: ${tax_rate}")
    print(f"you medicare levy is : ${medicare_levy}")

elif income >= 190001 and (private_insurance == "Y"):
    tax_rate = 51638 + ((income-190000) * 45/100)
    aftertax_income = income - tax_rate
    print(f"your income after tax is: ${aftertax_income}")
    print(f"tax you have to pay is: ${tax_rate}")
    print("You are eligible for medicare exemption")

else:
    print("Invalid income")










