    # dictionary = a collection of {key:value} pairs
    # ordered and changeable. No duplicates



capitals = {"USA": "Washington D.C.",
            "India": "New Delhi",
            "China": "Beijing",
            "Russia": "Moscow"}


    #print(dir(capitals))
    #print(help(capitals))

    #print(capitals.get('USA'))

'''
if capitals.get("Japan"):
    print("That capital exists")
else:
    print("That capital doesn't exist") 
'''

    #capitals.update({"Germany": "Berlin"})
    #capitals.pop("China") #drop item 
    #capitals.popitem() #drop last item on the dictionary
    #capitals.clear() #clear all 

keys = capitals.keys()

    #for key in capitals.keys():
    #print(key)

    #for vaulue in capitals.values():
    #print(vaulue)



for key, value in capitals.items():
    print(f"{key}: {value}")