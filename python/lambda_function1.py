'''
problem statement - filter and square even numbers
write a python program to filter all even numbers from a list and then find the square of each even number using lambda function.

requirements:
accept a list of numbers as input from the user.
use filter() with a lambda function to select only the even numbers.
use map() with a lambda function to find the square of each even number.
display the final list
'''

nums = list(map(int, input("Enter a list of numbers separated by spaces: ").split()))
even_nums = list(filter(lambda x: x % 2 == 0, nums))
squared_evens = list(map(lambda x: x ** 2, even_nums))
print(f"The squares of the even numbers are: {squared_evens}")  