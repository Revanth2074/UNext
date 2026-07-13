from collections import namedtuple

student = namedtuple('Student', ['name', 'age', 'grade'])

s1 = student(name='John', age=20, grade='A')
print(s1)
