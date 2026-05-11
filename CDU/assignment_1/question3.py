n = int(input("How many students?"))

names= []
scores = []

# user input
i = 0
while i < n:
    name= input("Student " + str(i+1) + " name: ")
    score= int(input("Enter score: "))

    names.append(name)
    scores.append(score)

    i = i + 1

# individual grade
print("Individual grades:")

total = 0

h_score= scores[0]
l_score= scores[0]
h_name= names[0]
l_name= names[0]

i = 0
while i < n:

    score = scores[i]

    if score >= 85:
        print("Name:", names[i], "Grade: ", "HD")
    elif score >= 75:
        print("Name:", names[i], "Grade: ", "D")
    elif score >= 65:
        print("Name:", names[i], "Grade: ", "C")
    elif score >= 50:
        print("Name:", names[i], "Grade: ", "P")
    else:
        print("Name:", names[i], "Grade: ", "F")

    total = total + score

    if score > h_score:
        h_score = score
        h_name = names[i]

    if score < l_score:
        l_score = score
        l_name = names[i]

    i = i + 1


avg = total / n

# summary
print("Class average:", avg)
print("Highest score:", h_score, h_name)
print("Lowest score:", l_score, l_name)