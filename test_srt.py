
from scheculer import ShortestRemainTime, Process

srt = ShortestRemainTime([
    Process(1, 0, 12),
    Process(2, 2, 7),
    Process(3, 5, 8),
    Process(4, 9, 3),
    Process(5, 12, 6),
])

# srt = ShortestRemainTime.user_input()

print("============= list process =============")
print(srt.processes)

print("\n============= result with srt algothrim =============")
srt.calculate_gantt()