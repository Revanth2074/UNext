import string

def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

def count_vowels(text):
    vowels = "aeiouAEIOU"
    count = 0
    for ch in text:
        if ch in vowels:
            count += 1
    return count