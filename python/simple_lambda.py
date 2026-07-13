from time import time


add = lambda x, y: x + y
result = add(5, 3)

find_largest_word = lambda sentence: max(sentence.split(), key=len)
sentence = input("Enter a sentence: ")
start_time = time.pref_counter()
largest_word = find_largest_word(sentence)
end_time = time.perf_counter()
print(f"The largest word in the sentence is: {largest_word}")
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.6f} seconds")

# now the without lambda function for longest word
def find_longest_word(sentence):
    words = sentence.split()
    longest_word = max(words, key=len)
    return longest_word

sentence = input("Enter a sentence: ")
start_time = time.perf_counter()
longest_word = find_longest_word(sentence)
end_time = time.perf_counter()
print(f"The longest word in the sentence is: {longest_word}")
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.6f} seconds")