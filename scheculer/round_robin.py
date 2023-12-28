
from typing import Iterable
import pandas as pd

from pandas.core.api import DataFrame as DataFrame
from scheculer.base import Process
from scheculer.utils import data_format
from .base import Scheduler

class RoundRobin(Scheduler):

    def __init__(self, processes: Iterable[Process], quantum_time) -> None:
        self.quantum_time = quantum_time
        super().__init__(processes)

    def _pid_from(self, jobs:list[Process], queue:list[int]):
        for pid in queue:
            if jobs[pid].burst_time:
                yield pid

    def calculate_gantt(self) -> DataFrame:
        jobs = self.deepcopy_processes
        n = len(jobs)
        index = 0
        queue = [index]
        gantt_data = []
        start_time = 0
        current_time = 0
        ready_pid = 1
        sum_burst_time = self.sum_burst_time
        while sum_burst_time:
            if ready_pid < n and jobs[ready_pid].arrival_time <= current_time:
                queue.insert(index+1, ready_pid)
                ready_pid += 1
                continue

            pid = queue[index]
            
            if jobs[pid].burst_time > self.quantum_time:
                jobs[pid].burst_time -= self.quantum_time
                current_time += self.quantum_time
            else:
                current_time += jobs[pid].burst_time
                jobs[pid].burst_time = 0
                queue.remove(pid)
            
            index += 1
            if index == len(queue):
                index = 0

            gantt_data.append(data_format(pid, start_time, current_time))
            sum_burst_time -= (current_time - start_time)
            start_time = current_time
        
        gantt_df = pd.DataFrame(gantt_data).set_index(['pid']).sort_values(by=['start', 'end']).groupby(level=0).agg(list)
        return gantt_df

    def get_infor(self) -> DataFrame:
        infor_df = pd.concat([self.processes.stack(), self._gantt.stack()], axis=0).unstack()
        infor_df['response_time'] = infor_df['start'].str[0] - infor_df['arrival_time']
        
        # Calculate turnaround time
        infor_df['turnaround_time'] = infor_df['end'].str[-1] - infor_df['arrival_time']
        infor_df['waiting_time'] = infor_df['turnaround_time'] - infor_df['burst_time']
        infor_df = infor_df.T
        infor_df["mean"] = infor_df.iloc[-3:].mean(axis=1)
        return infor_df.T.drop(columns=['start','end'])

class RR(RoundRobin):...