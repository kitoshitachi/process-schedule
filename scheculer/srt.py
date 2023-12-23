
from .base import Scheduler

class ShortestRemainTime(Scheduler):
    def gantt(self):
        current_index = 0 # alway lowest arrival time
        queue = [self._processes[current_index]]
        sum_burst_time_in_queue = self._processes[current_index].burst_time
        time = self._processes[current_index].arrival_time
        data:dict[str,dict] = {}

        while(sum_burst_time_in_queue > 0): # still have process is running 

            if 'first time' in data[queue[current_process].process_name]:
                data[queue[current_process].process_name] = {'first time': time}
                

            for id, process in enumerate(queue):

                if process.arrival_time > time: # not ready
                    continue

                if process.burst_time < queue[current_process].burst_time - process.arrival_time:

                    #update
                    time = process.arrival_time
                    
                    queue[current_process].burst_time -= time

                    process.arrival_time = 0

                    #run this process id because has burst time lowest
                    current_process = id


            time += current_process.burst_time
            data[current_process.process_name]['exit time'] = time

            index += 1

            for process in tmp_processes.copy():
                if process.arrival_time <= time:
                    queue.append(process)
                    tmp_processes.remove(process)
        return 