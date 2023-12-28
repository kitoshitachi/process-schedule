import pandas as pd

from .base import Process, Scheduler
from .utils import data_format
class ShortestRemainTime(Scheduler):
    
    def find_shortest_job(self, jobs:list[Process], current_time):
        shortest_job = None
        shortest_time = float('inf')
        
        for pid in self.pids:
            if jobs[pid].arrival_time <= current_time and jobs[pid].burst_time < shortest_time and jobs[pid].burst_time > 0:
                shortest_job = pid
                shortest_time = jobs[pid].burst_time
        
        return shortest_job
                
    def calculate_gantt(self):
        jobs = self.deepcopy_processes
        n = len(jobs)
        completed_jobs = []
        current = 0
        start_time = 0
        current_time = 0
        gantt_data = []
        
        while len(completed_jobs) < n:
            
            shortest = self.find_shortest_job(jobs, current_time)
            if shortest is None:
                current_time += 1
                continue

            if shortest != current:
                if start_time != current_time:
                    gantt_data.append(data_format(current, start_time, current_time))
                start_time = current_time
                current = shortest
            
            
            jobs[current].burst_time -= 1
            current_time += 1
            
            if jobs[current].burst_time == 0:
                gantt_data.append(data_format(current, start_time, current_time))
                completed_jobs.append(current)
                start_time = current_time

        gantt_df = pd.DataFrame(gantt_data).set_index(['pid']).sort_values(by=['start', 'end']).groupby(level=0).agg(list)
        return gantt_df
    

    def get_infor(self):
        infor_df = pd.concat([self.processes.stack(), self._gantt.stack()], axis=0).unstack()
        infor_df['response_time'] = infor_df['start'].str[0] - infor_df['arrival_time']
        
        # Calculate turnaround time
        infor_df['turnaround_time'] = infor_df['end'].str[-1] - infor_df['arrival_time']
        infor_df['waiting_time'] = infor_df['turnaround_time'] - infor_df['burst_time']
        infor_df = infor_df.T
        infor_df["mean"] = infor_df.iloc[-3:].mean(axis=1)
        return infor_df.T.drop(columns=['start','end'])
class SRT(ShortestRemainTime):...