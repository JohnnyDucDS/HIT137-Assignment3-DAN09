import random
import time
options = ("rock", "paper", "scissor")

playing = True

while playing:
    
    computer = random.choice(options)
    player = input("Enter a choice (rock, paper, scissor): ")

    while player not in options:
        print("please try again")
        player = input("Enter a choice (rock, paper, scissor): ")
 
    print(f"Computer: {computer}")
    print(f"Player: {player}")

    if player == computer:
        print("Draw")
    elif player == "rock" and computer == "scissor":
        print("You win")
    elif player == "paper" and computer == "rock":
        print("You win")
    elif player == "scissor" and computer == "paper":
        print("You win")
    else:
        print("You lose")
    
    play_again = input(f"Do you want to play again(Y/N): ").upper()
    if not play_again == 'Y':
        playing = False

print("Bye")
    



            
        


