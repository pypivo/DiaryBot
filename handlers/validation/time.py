from .errors import IncorrectTime

def check_correctness_time(time: str):
    time = time.replace(" ", "")
    time_list = time.split("-")
    h_start, m_start = 0, 0
    if len(time_list) != 2:
        raise IncorrectTime
    for t in time_list:
        t = t.split(":")
        h, m = int(t[0]), int(t[1])
        if h_start > h:
            raise IncorrectTime
        elif h_start == h and m_start > m:
            raise IncorrectTime
        m_start = m
        h_start = h
        if h >= 24 or m >= 60 or h < 0 or m < 0:
            raise IncorrectTime