#python quiz game

questions = ("Which planet in our solar system is known as the Red Planet?",
             "What is the capital city of France?",
             "Which element has the chemical symbol 'O'?",
             "How many continents are there on Earth?",
             "Who wrote the famous play Romeo and Juliet?")

options = ( ("A. Venus", "B. Mars", "C. Jupiter", "D. Saturn"),
            ("A. Rome", "B. Madrid", "C. Paris", "D. Berlin"),
            ("A. Gold", "B. Silver", "C. Iron", "D. Oxygen"),
            ("A. 5", "B. 6", "C. 7", "D. 8"),
            ("A. Charles Dickens", "B. William Shakespeare", "C. Mark Twain", "D. Jane Austen"))
           

answers = ("B", "C", "D", "C", "B")
score = 0 
question_num = 0 
correct_answer_list = []
    
    #print ques and answers 
for question in questions:
    print('-------------------------------------------------')
    print(question)
    for option in options[question_num]:
        print(option)

    guess = input("Enter (A, B, C, D): ").upper()
   
    if guess == answers[question_num]:
        print('Answer is correct')
        score += 1
        correct_answer_list.append(guess)
        
    else:
        print("Your answer is not correct!")
        print(f"{answers[question_num]} is the correct answer")
    
    question_num += 1 
    

score = int((score / len(correct_answer_list) * 100))


print()

print("result".upper())
print()
print(f"Your total correct answer is {len(correct_answer_list)}")
print(f"Your score is {score}%")


    