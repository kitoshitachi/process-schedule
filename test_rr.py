
from scheculer import RoundRobin, Process

rr = RoundRobin([
    Process('p1', 5, 10),
    Process('p2', 2, 29),
    Process('p3', 0, 3),
    Process('p4', 1, 7),
    Process('p5', 7, 12),
], quantum_time=10)

# rr = RR.user_input()

print("============= list process =============")
print(rr.processes)

print("\n============= gantt with rr algothrim =============")
print(rr._gantt)

print("\n============= result with rr algothrim =============")
print(rr.infor)





