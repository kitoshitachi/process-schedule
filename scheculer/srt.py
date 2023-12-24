import copy
import pandas as pd

from .base import Scheduler

class ShortestRemainTime(Scheduler):

    def _get_ready_pid_from(self, not_ready_pids:list[int], time):

        for pid in not_ready_pids:
            if self._processes[pid].arrival_time <= time:
                time = self._processes[pid].arrival_time
                yield pid
    

    def calculate_gantt(self):
        processes = copy.deepcopy(self._processes)
        queue = []        
        current_process = None
        time_range = {
            'start':0,
            'end':0
        } 
        data = []

        sum_burst_time = self.sum_burst_time
        index = 0
        for process in processes:
            if not current_process:
                current_process = process
                time_range['start'] = 0
                time_range['end'] = 0
                continue
            
            min_burst_time = current_process.burst_time - (process.arrival_time - current_process.arrival_time)
            while min_burst_time <= 0:
                time_range['start'] = time_range['end']
                time_range['end'] = process.arrival_time + min_burst_time
                
                data.append({'name':current_process.process_name, 'start':time_range['start'], 'end': time_range['end']})

                if not queue:
                    current_process = None
                    break

                current_process = min(queue, key=lambda x: x.burst_time)
                queue.remove(current_process)
                current_process.arrival_time = time_range['end']
                min_burst_time = current_process.burst_time + min_burst_time

            if not queue and current_process is None:
                current_process = process
                continue

            if process.burst_time < min_burst_time:
                current_process.burst_time = min_burst_time
                if current_process.arrival_time != process.arrival_time:
                    time_range['start'] = time_range['end']
                    time_range['end'] = process.arrival_time
                    data.append({'name':current_process.process_name, 'start':time_range['start'], 'end': time_range['end']})
                                
                queue.append(current_process)
                current_process = process
            else:
                queue.append(process)
            
        if current_process != None:
            time_range['start'] = time_range['end']
            time_range['end'] = time_range['end'] + current_process.burst_time
            data.append({'name':current_process.process_name, 'start': time_range['start'], 'end': time_range['end']})
        
        sorted_queue = sorted(queue, key = lambda process: process.burst_time)
        for process in sorted_queue:
            time_range['start'] = time_range['end']
            time_range['end'] = time_range['end'] + process.burst_time
            data.append({'name':process.process_name, 'start': time_range['start'], 'end': time_range['end']})

        return data

    def get_infor(self):
        return
        gantt_df = self._gantt.transpose(copy=True)
        infor_df = pd.concat([self.processes,gantt_df], axis= 1)
        infor_df['response_time'] = infor_df['start'] - infor_df['arrival_time']
        infor_df['turnaround_time'] = infor_df['end'] - infor_df['arrival_time']
        infor_df['waiting_time'] = infor_df['turnaround_time'] - infor_df['burst_time']
        infor_df = infor_df.T
        infor_df["mean"] = infor_df.iloc[-3:].mean(axis=1)
        return infor_df.T.drop(columns=['start','end'])
class SRT(ShortestRemainTime):...