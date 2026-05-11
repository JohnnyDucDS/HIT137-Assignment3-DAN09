
foods = []
prices = []
total = 0 

while True: 
    food = input('Enter food name (q to quit): ')
    if food.lower() == 'q':
        break 
    else:
        price = float(input(f'Enter the price of {food}: $'))
        foods.append(food)
        prices.append(price)


for food in foods:
    print(food)

for price in prices: 
    print(price)
    total += price

print()
print(f'Your total is : ${total}') 