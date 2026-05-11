    #input sentence
sentence = input('Enter a sentence: ')

    #define how many words in a sentence
words = sentence.split()

    #words count
total_words = len(words)

    #longest word
longest_word = max(words, key=len)

    #uppercase 
uppper_word = sentence.upper()

    #result
print(f"Input: '{sentence}'")
print(f"Total words: {len(words)} letters")
print(f'Longest word: {longest_word.capitalize()}')
print(f"Uppercase: {uppper_word}")