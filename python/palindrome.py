# function to check if a string is a palindrome
def is_palindrome(s):
    text = s.lower()
    return text == text[::-1]

word = input("Enter a word: ")
if is_palindrome(word):
    print(f"{word} is a palindrome.")
else:
    print(f"{word} is not a palindrome.")