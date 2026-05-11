import random
import string 

'''
This is a program let user input a string and add 4 random characters to the end of each word in the string.
The random characters are generated using the random module, 
    and the final output is a modified version of the original string with the random characters added to each word.

“I am a dog lover” -> /‘I’ ‘am’ ‘a’ ‘dog’ ‘lover’/

-> Iabvdgamasrgyadefghdogatvxslover

'''

#input text from user
text = input("Enter a string to hide: ").split()
random_chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '@', '$', '/', '&', '*', '!', '?']
result_final = []


for word in text:
    # pick random characters 
    random_word = random.choices(random_chars, k=4)
    result = "".join(random_word)

    #format the word to hide
    formatted_word = f"{word}{result}"
    result_final.append(formatted_word)

    final_string = "".join(result_final)

print(f"This is the original string: {" ".join(text)}")
print(final_string)




    
'''
import random
import string

def add_random_chars_to_words(input_string):
    # 1. Split the input string into a list of words
    words = input_string.split()
    
    result_parts = []
    
    for word in words:
        # 2. Generate 4 random lowercase characters
        # random.choices picks 4 characters from the lowercase alphabet
        random_suffix = ''.join(random.choices(string.ascii_lowercase, k=4))
        
        # 3. Format the word and the suffix with quotes
        # We wrap the suffix in quotes and attach it to the word
        result_parts.append(f'{word}{random_suffix}')
    
    # 4. Join everything together into one string
    # We add a leading quote to match your example's format
    final_string = "".join(result_parts)
    
    return final_string

# --- Testing the code ---
user_input = input("Enter a string: ")
output = add_random_chars_to_words(user_input)

print("Original:", user_input)
print("Modified:", output)
'''