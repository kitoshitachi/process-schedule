from time import sleep
import pandas as pd

from .base import Process, Scheduler

class ShortestRemainTime(Scheduler):

    def get_not_ready_pids(self, processes:list[Process]):
            for pid in self.pids:
                if processes[pid].arrival_time != 0:
                    yield pid

    def _get_ready_from(self, processes:list[Process], time:int):
        not_ready_pids = self.get_not_ready_pids(processes)
        
        for pid in not_ready_pids:
            if processes[pid].arrival_time <= time:
                yield pid
                time = processes[pid].arrival_time

    def _find_pid_lowest_burst_time(self, processes:list[Process]):
        def is_in_queue(process:Process):
            
            if process.arrival_time > 0: # not ready
                return False
            
            if process.burst_time == 0: # finished
                return False
            
            return True
        
        queue = [pid for pid in self.pids if is_in_queue(processes[pid])]
        if queue:
            return min(queue,  key=lambda pid: processes[pid].burst_time)
            

    def calculate_gantt(self):
        copy_processes = self.deepcopy_processes
        current_pid = 0
        time_range = {
            'start':self._processes[current_pid].arrival_time,
            'end':self._processes[current_pid].burst_time
        } 
        gantt_data = []

        sum_burst_time = self.sum_burst_time

        while(sum_burst_time > 0):
            print(time_range)
            print(copy_processes[current_pid])
            print(gantt_data)
            ready_pids = self._get_ready_from(copy_processes, time_range['end'])
            next_pid = next(ready_pids, None)
            if next_pid:
                time_range['end'] = copy_processes[next_pid].arrival_time
                copy_processes[current_pid].burst_time -= (copy_processes[next_pid].arrival_time - self._processes[current_pid].arrival_time) # remain time
                
                print(copy_processes)
                print('=========================')
                sum_burst_time -= copy_processes[next_pid].arrival_time # update progress bar
                copy_processes[next_pid].arrival_time = 0 # set to ignore it from "_get_ready_pid_from" method
                next_pid = None
                for pid in ready_pids: # same arrival time then set it
                    copy_processes[pid].arrival_time = 0
            else: # run until finish
                gantt_data.append({
                    'pid':current_pid,
                    'start': time_range['start'],
                    'end': time_range['end'] + copy_processes[current_pid].burst_time,
                })
                sum_burst_time -= copy_processes[current_pid].burst_time
                copy_processes[current_pid].burst_time = 0

                current_pid = self._find_pid_lowest_burst_time(copy_processes)
                
                time_range['start'] = time_range['end']
                time_range['end'] += copy_processes[current_pid].burst_time
                continue

            next_pid = self._find_pid_lowest_burst_time(copy_processes)
            if next_pid and next_pid != current_pid:
                gantt_data.append({
                    'pid':current_pid,
                    'start': time_range['start'],
                    'end': time_range['end'],
                })
                current_pid = next_pid
                time_range['start'] = time_range['end']
                time_range['end'] += copy_processes[current_pid].burst_time
            
        return gantt_data

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