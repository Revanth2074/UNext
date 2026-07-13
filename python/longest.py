'''
write a python program to find the longest word in a sentence using a function.
Requirements:
Create a function named find_longest_word().
Appect a sentence as input from the user.
split the sentence into words.
find the word with the maximum length.
return the longest word.
display the result.
'''

def find_longest_word(sentence):#using for loop
    words = sentence.split()
    longest_word = ""
    for word in words:
        if len(word) > len(longest_word):
            longest_word = word
    return longest_word

def find_longest_word(sentence):
    words = sentence.split()
    longest_word = max(words, key=len)
    return longest_word

sentence = input("Enter a sentence: ")
longest_word = find_longest_word(sentence)
print(f"The longest word in the sentence is: {longest_word}")