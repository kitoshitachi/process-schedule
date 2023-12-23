
from scheculer import SJF, Process

sjf = SJF([
    Process(1, 0, 12),
    Process(2, 2, 7),
    Process(3, 5, 8),
    Process(4, 9, 3),
    Process(5, 12, 6),
])

# sjf = SJF.user_input()

print("============= list process =============")
print(sjf.processes)

print("\n============= result with sjf algothrim =============")
print(sjf._gantt())