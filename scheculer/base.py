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
        return f"(process name: {self.process_name}, at: {self.arrival_time}, bt:{self.burst_time})"

class Scheduler:
    def __init__(self, processes: list[Process]) -> None:
        self._processes = sorted(processes, key = lambda process: process.arrival_time)
        self._sum_burst_time = None
        self._gantt = self.calculate_gantt()
        self._infor = self.get_infor()
        pass

    @classmethod
    def user_input(cls):
        num_of_processes = int(input("Enter the amount of process: "))
        processes = [Process.from_input() for _ in range(num_of_processes)]
        return cls(processes)

    @property
    def pids(self):
        return tuple(range(len(self._processes)))

    @property
    def processes(self):
        df = pd.DataFrame(process.__dict__ for process in self._processes)
        df.index.rename('pid', inplace=True)
        return df

    @property
    def sum_burst_time(self):
        if self._sum_burst_time is None:
            self._sum_burst_time = sum(process.burst_time for process in self._processes)
        
        return self._sum_burst_time

    @property
    def gantt(self):
        return self._gantt.to_markdown(index=False)

    @property
    def infor(self):
        return self._infor.to_markdown() 
    
    def calculate_gantt(self) -> pd.DataFrame:
        raise NotImplementedError
    
    def get_infor(self) -> pd.DataFrame:
        raise NotImplementedError