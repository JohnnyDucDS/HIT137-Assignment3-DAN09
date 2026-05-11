num_students = int(input("How many students in the class? : "))
stu_name = []
stu_grade = []
 
 #user_input and check condition
while num_students < 3 or num_students > 10 :
    print("NUmber of students must more than 3 and less than 10")
    num_students = int(input("How many students in the class? : "))


for x in range(1,num_students + 1):
    name = str(input(f"Enter student {x} name: "))
    grade = int(input(f"Enter student {x} grade: "))
    while grade < 0 or grade > 100:
        print('Grade must larger than 0 and less than 100')
        grade = int(input(f"Enter student {x} grade: "))

    stu_name.append(name)
    stu_grade.append(grade)

       
#display individual grade 
total = 0 
highest_grade = stu_grade[0]
lowest_grade = stu_grade[0]
highest_name = stu_name[0]
lowest_name = stu_name[0]

    #grade conditon
for i in range(num_students):
    current_grade = stu_grade[i]

    if current_grade >= 85:
        print("Name:", stu_name[i], "Grade: ", "HD")
    elif current_grade >= 75:
        print("Name:", stu_name[i], "Grade: ", "D")
    elif current_grade >= 65:
        print("Name:", stu_name[i], "Grade: ", "C")
    elif current_grade >= 50:
        print("Name:", stu_name[i], "Grade: ", "P")
    else:
        print("Name:", stu_name[i], "Grade: ", "F")


    total += current_grade

    if current_grade > highest_grade:
        highest_grade = current_grade
        highest_name = stu_name[i]

    if current_grade < highest_grade: 
        lowest_grade = current_grade
        lowest_name = stu_name[i]

avg = total / num_students

print('Class average: ', round(avg))      
print("Highest score:", highest_grade, 'Student name:',  highest_name)
print("Lowest score:", lowest_grade,'Student name:', lowest_name)










    





