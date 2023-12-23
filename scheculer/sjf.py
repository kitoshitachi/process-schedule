
import pandas as pd

from .base import Scheduler, Process

class ShortestJobFirst(Scheduler):

    def gantt(self) -> tuple[list[Process], dict[str, dict]]:
        index = 0
        queue = [self._processes[index]]
        data = {}
        not_ready_processes = sorted(self._processes[index+1:], key = lambda process: process.burst_time)
        time = self._processes[index].arrival_time
        num_of_processes = len(self._processes)
        while(index < num_of_processes):           

            current_process = queue[index]
            data[current_process.process_name] = {'first time': time}
          

            time += current_process.burst_time
            data[current_process.process_name]['exit time'] = time

            index += 1

            for process in not_ready_processes.copy():
                if process.arrival_time <= time: # is ready
                    queue.append(process)
                    not_ready_processes.remove(process)
            
        return queue, data

    def _get_ready_pid_from(self, not_ready_pids:list[int], time):
        for pid in not_ready_pids:
            if self._processes[pid].arrival_time <= time:
                yield pid
    
    

    def _gantt(self):
        index = 0
        data = {}
        queue = [self.pids[index]]
        not_ready_processes = sorted(self.pids[index + 1:], key = lambda pid: self._processes[pid].burst_time)

        sum_burst_time = self.sum_burst_time
        time_range = {
            'start':queue[index].arrival_time,
            'end':queue[index].burst_time
        } 

        while(sum_burst_time > 0):
            print(data)

            for ready_pid in self._get_ready_pid_from(not_ready_processes, time_range['end']):
                queue.append(ready_pid)
                not_ready_processes.remove(ready_pid)
            
            data[str(time_range['start']) + "-" + str(time_range['end'])] = queue[index]

            sum_burst_time -= self._processes[queue[index]].burst_time

            index += 1

            time_range['start'] = time_range['end']
            time_range['end'] += queue[current_pid].burst_time
        
        return data


    def infor(self):

        first_time = 0
        queue, data = self.gantt()
        for current_process in queue:
            first_time = data[current_process.process_name]['first time']
            exit_time = data[current_process.process_name]['exit time']

            response_time = first_time - current_process.arrival_time
            turnaround_time = exit_time - current_process.arrival_time
            waiting_time = turnaround_time - current_process.burst_time


            data[current_process.process_name].update({
                "response time": response_time,
                "waiting time": waiting_time,
                "turnaround time": turnaround_time
            })
            
            first_time = exit_time

        df = pd.DataFrame(data)

        df["mean"] = df.iloc[2:].mean(axis=1)
        return df.transpose().to_markdown()


class SJF(ShortestJobFirst):...