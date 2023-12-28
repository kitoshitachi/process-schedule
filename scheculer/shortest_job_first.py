
import pandas as pd

from .utils import data_format

from .base import Scheduler

class ShortestJobFirst(Scheduler):
   
    def ready_jobs(self, pids:list[int], current_time):
        for pid in pids:
            if self._processes[pid].arrival_time < current_time:
                yield pid

    def calculate_gantt(self):
        current = 0
        sorted_by_burst_time = sorted(self.pids[1:], key= lambda pid: self._processes[pid].burst_time)
        start_time = self._processes[current].arrival_time
        end_time = self._processes[current].burst_time

        data = [data_format(current, start_time, end_time)]
        
        while(sorted_by_burst_time):
            queue_jobs = self.ready_jobs(sorted_by_burst_time, end_time)
            current = next(queue_jobs, None)

            start_time = end_time

            end_time += self._processes[current].burst_time

            data.append(data_format(current, start_time, end_time))

            sorted_by_burst_time.remove(current)
        
        return pd.DataFrame(data).set_index(['pid'])

    def get_infor(self):
        infor_df = pd.concat([self.processes.stack(),self._gantt.stack()], axis= 0).unstack()
        infor_df['response_time'] = infor_df['start'] - infor_df['arrival_time']
        infor_df['turnaround_time'] = infor_df['end'] - infor_df['arrival_time']
        infor_df['waiting_time'] = infor_df['turnaround_time'] - infor_df['burst_time']
        infor_df = infor_df.T
        infor_df["mean"] = infor_df.iloc[-3:].mean(axis=1)
        return infor_df.T.drop(columns=['start','end'])


class SJF(ShortestJobFirst):...