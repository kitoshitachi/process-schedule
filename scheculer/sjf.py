
import pandas as pd

from .base import Scheduler

class ShortestJobFirst(Scheduler):

    def _get_ready_pid_from(self, not_ready_pids:list[int], time):
        for pid in not_ready_pids:
            if self._processes[pid].arrival_time <= time:
                yield pid
    
    def calculate_gantt(self):
        index = 0
        queue = [self.pids[index]]
        not_ready_processes = sorted(self.pids[index + 1:], key = lambda pid: self._processes[pid].burst_time)

        time_range = {
            'start':self._processes[queue[index]].arrival_time,
            'end':self._processes[queue[index]].burst_time
        } 
        data = {}
        data[queue[index]] = time_range.copy()

        sum_burst_time = self.sum_burst_time - self._processes[queue[index]].burst_time

        while(sum_burst_time > 0):
            for ready_pid in self._get_ready_pid_from(not_ready_processes.copy(), time_range['end']):
                queue.append(ready_pid)
                not_ready_processes.remove(ready_pid)
            index += 1

            time_range['start'] = time_range['end']

            current_process = self._processes[queue[index]]
            time_range['end'] += current_process.burst_time

            # data[str(time_range['start']) + "-" + str(time_range['end'])] = queue[index]
            data[queue[index]] = time_range.copy()
            
            sum_burst_time -= current_process.burst_time
        
        return pd.DataFrame(data)

    def get_infor(self):
        gantt_df = self._gantt.transpose(copy=True)
        infor_df = pd.concat([self.processes,gantt_df], axis= 1)
        infor_df['response_time'] = infor_df['start'] - infor_df['arrival_time']
        infor_df['turnaround_time'] = infor_df['end'] - infor_df['arrival_time']
        infor_df['waiting_time'] = infor_df['turnaround_time'] - infor_df['burst_time']
        infor_df = infor_df.T
        infor_df["mean"] = infor_df.iloc[-3:].mean(axis=1)
        return infor_df.T.drop(columns=['start','end'])


class SJF(ShortestJobFirst):...