import pandas as pd


class Process:
    process_name:str
    burst_time:int
    arrival_time:int

    def __init__(self, process_name, arrival_time, burst_time) -> None:
        self.process_name = process_name
        self.burst_time = burst_time
        self.arrival_time = arrival_time

    @classmethod
    def from_input(cls):
        process_name = input("Enter name of process: ")
        arrival_time = int(input(f"Enter arrival time of process P[{process_name}]: "))
        burst_time = int(input(f"Enter burst time of process P[{process_name}]: "))
        return cls(process_name, arrival_time, burst_time)
    
    def __repr__(self) -> str:
        return f"(pid: {self.process_name}, at: {self.arrival_time}, bt:{self.burst_time})"

class Scheduler:
    def __init__(self, processes: list[Process]) -> None:
        self._processes = processes
        pass

    @classmethod
    def user_input(cls):
        num_of_processes = int(input("Enter the amount of process: "))
        processes = [Process.from_input() for _ in range(num_of_processes)]
        return cls(processes)

    @property
    def processes(self):
        return pd.DataFrame(process.__dict__ for process in self._processes).to_markdown(index=False)


    def gantt(self):
        raise NotImplementedError

    def infor(self):
        raise NotImplementedError 