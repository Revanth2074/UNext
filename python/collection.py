'''
used to count occerrences of each element in a collection
data = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
'''

from collections import Counter
data = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
counter = Counter(data)
print(counter)  