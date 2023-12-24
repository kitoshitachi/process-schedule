
import pandas as pd
from scheculer import SJF, Process

sjf = SJF([
    Process('p1', 0, 12),
    Process('p2', 2, 7),
    Process('p3', 5, 8),
    Process('p4', 9, 3),
    Process('p5', 12, 6),
])

# sjf = SJF.user_input()

print("\n============= gantt with sjf algothrim =============")
print(sjf.gantt)
print("\n============= result with sjf algothrim =============")
print(sjf.infor)





