

def data_format(pid, start, end):
    return {
        'pid': pid,
        'start': start,
        'end': end
    } 

def difference_time(start, end):
    return end - start