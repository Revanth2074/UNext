from collections import deque

dq = deque([1, 2, 3, 4, 5])

dq.append(6)
dq.appendleft(0)
print(dq)