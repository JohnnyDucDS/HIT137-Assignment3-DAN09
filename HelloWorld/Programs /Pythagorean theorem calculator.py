 #Pythagorean theorem calculator
import math
'''
print("This a a program help you calculate Pythagorean theorem")
print("Assume AC is altitude")
print("Assume AB is base")
print("Assume BC is Hypotenuse" )

AC = float(input("Enter the vaule of AC:"))
AB = float(input("Enter the vaule of AB:"))
BC = round(math.sqrt(AC**2 + AB**2))

print(f"The value of BC is {BC}")
'''

#ver 2
'''
def Pythagorean_theorem_calculator():
    quit = True 
    while quit:
     
            print("Assume AC is altitude")
            print("Assume AB is base")
            print("Assume BC is Hypotenuse" )
        
            AC = float(input("Enter the vaule of AC:"))
            AB = float(input("Enter the vaule of AB:"))
            BC = round(math.sqrt(AC**2 + AB**2))
            
            print(f"The value of BC is {BC}")
            
            try_again = input(f"Do you want to continue (y to continue) (q to quit: )").lower()
            if try_again == "q":
                  quit = False
           
                  
Pythagorean_theorem_calculator()
'''

# Ver 3

def Pythagorean_theorem_calculator(AC, AB):
    quit = True 
    while quit:
                
            BC = round(math.sqrt(AC**2 + AB**2))
            
            print(f"The value of BC is {BC}")
            
            try_again = input(f"Do you want to continue (y to continue) (q to quit: )").lower()
            if try_again == "q":
                  quit = False
           
                  
Pythagorean_theorem_calculator(6, 10)