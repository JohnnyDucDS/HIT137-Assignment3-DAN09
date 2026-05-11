age = int(input('How old are you?'))

while age < 0:
    print("Age can not be negative number: ")
    age = int(input('How old are you?'))


print(f"You are {age} years old")
