#function to count vowels

def count_vowel(s):
    vowels = "aeiouAEIOU"
    count = 0
    for char in s:
        if char in vowels:
            count += 1
    return count

def count_vowels(s):
    vowels = "aeiouAEIOU"
    count = 0
    for char in s:
        count += char in vowels
    return count

sentence = input("Enter a sentence: ")
vowel_count = count_vowels(sentence)
print(f"The number of vowels in the sentence is: {vowel_count}")

