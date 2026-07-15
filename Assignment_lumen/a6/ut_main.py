from utilities import string_ops, math_ops, file_ops

text = "Hello, Python!"

print(string_ops.remove_punctuation(text))
print("Vowels =", string_ops.count_vowels(text))

numbers = [10, 20, 30, 40, 50]
print("Mean =", math_ops.mean(numbers))
print("Median =", math_ops.median(numbers))
print("Standard Deviation =", math_ops.standard_deviation(numbers))

file_ops.write_file("sample.txt", "Python Programming")
print(file_ops.read_file("sample.txt"))
print(file_ops.search_file("sample.txt", "Python"))