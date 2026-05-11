fruits =        ["apple", "orange", "banana", "coconut"]
vegetables =    ["carrot", "potato", "celery", "cabbage"]
meats =         ["chicken", "fish", "pork", "turkey"]

groceries = [fruits, vegetables, meats]


#print(groceries[0][3]) #coordinate row then column 

for collection in groceries:
    for food in collection:
        print(food, end=' ')
    print()