from functools import reduce

dimensions = [2, 3, 5]

product = reduce(lambda x, y: x * y, dimensions)

print("Product =", product)