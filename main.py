def srt(processes, burst_time):
    n = len(processes)
    remaining_time = burst_time.copy()
    waiting_time = [0] * n
    turnaround_time = [0] * n
    total_waiting_time = 0
    total_turnaround_time = 0
    completed = 0
    current_time = 0
    min_burst_time = float('inf')
    shortest_job = 0
    is_completed = [False] * n
    gantt_chart = []

    while completed != n:
        for i in range(n):
            if remaining_time[i] > 0 and remaining_time[i] < min_burst_time and current_time >= processes[i][1]:
                min_burst_time = remaining_time[i]
                shortest_job = i

        remaining_time[shortest_job] -= 1
        min_burst_time = remaining_time[shortest_job]

        if min_burst_time == 0:
            min_burst_time = float('inf')

        if remaining_time[shortest_job] == 0:
            completed += 1
            is_completed[shortest_job] = True
            turnaround_time[shortest_job] = current_time - processes[shortest_job][1] + 1
            waiting_time[shortest_job] = turnaround_time[shortest_job] - burst_time[shortest_job]
            total_waiting_time += waiting_time[shortest_job]
            total_turnaround_time += turnaround_time[shortest_job]

        current_time += 1
        gantt_chart.append(("P" + str(shortest_job), current_time - 1))

    avg_waiting_time = total_waiting_time / n
    avg_turnaround_time = total_turnaround_time / n

    print("Process\tBurst Time\tWaiting Time\tTurnaround Time")
    for i in range(n):
        print(f"P{i}\t\t{burst_time[i]}\t\t{waiting_time[i]}\t\t{turnaround_time[i]}")

    print(f"\nAverage Waiting Time: {avg_waiting_time}")
    print(f"Average Turnaround Time: {avg_turnaround_time}")

    print("\nGantt Chart:")
    for i in range(len(gantt_chart) - 1):
        print(gantt_chart[i][0], gantt_chart[i][1], "->", gantt_chart[i + 1][1])

# Test the algorithm
processes = [("P0", 0), ("P1", 2), ("P2", 4), ("P3", 5)]
burst_time = [7, 5, 2, 1]

srt(processes, burst_time)