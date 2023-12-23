
import pandas as pd

from .base import Scheduler, Process

class ShortestJobFirst(Scheduler):

    def gantt(self) -> tuple[list[Process], dict[str, dict]]:
        index = 0
        queue = [self._processes[index]]
        data = {}
        tmp_processes = sorted(self._processes[index+1:], key = lambda process: process.burst_time)
        time = self._processes[index].arrival_time
        num_of_processes = len(self._processes)
        while(index < num_of_processes):
           

            current_process = queue[index]
            data[current_process.process_name] = {'first time': time}
          

            time += current_process.burst_time
            data[current_process.process_name]['exit time'] = time

            index += 1

            for process in tmp_processes.copy():
                if process.arrival_time <= time:
                    queue.append(process)
                    tmp_processes.remove(process)
            
        return queue, data

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