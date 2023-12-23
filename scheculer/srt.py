import pandas as pd

from .base import Process, Scheduler

class ShortestRemainTime(Scheduler):

    @staticmethod
    def _get_ready_process(not_ready_processes:list[Process], current_time:int):
        '''
        return the pid is ready at current time
        '''
        for process in not_ready_processes:
            if process.arrival_time <= current_time:
                yield process
    

    def gantt(self):

        current_pid = 0 # alway lowest arrival time
        next_pid = current_pid #if it still lowest burst time => still running to end 
        ready_process = [self._processes[current_pid]]
        not_ready_processes = self._processes[current_pid + 1:].copy()
        sum_burst_time = self.sum_burst_time
        current_time = ready_process[current_pid].arrival_time
        data:dict[str,dict] = {}

        while(sum_burst_time > 0): # still have process is running 
            for process in self._get_ready_process(not_ready_processes, current_time)
                pass
            
        return pd.DataFrame(data)