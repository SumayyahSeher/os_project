class Process:
    def __init__(self, p_id, arrival_time, burst_time, priority=1):
        self.p_id = p_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority

        self.start_time=None
        self.completion_time=None
        self.wait_time=None
        self.TAT=None

    def getProcessID(self):
        return self.p_id

    def getArrivalTime(self):
        return self.arrival_time

    def getBurstTime(self):
        return self.burst_time
    
    def getStartingTime(self):
        return self.start_time

    def getCompletionTime(self):
        return self.completion_time
    
    def getWaitTime(self):
        return self.wait_time

    def getTurnaroundTime(self):
        return self.TAT

    def setArrivalTime(self, x):
        self.arrival_time = x
        return

    def setBurstTime(self, y):
        self.burst_time = y
        return

    def setStartingTime(self, a):
        self.start_time = a
        return

    def setCompletionTime(self, b):
        self.completion_time = b
        return
