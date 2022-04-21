import heapq


class PriorityQueue:
    def __init__(self):
        self.data = list() 
    
    def empty(self):
        return len(self.data) == 0
    
    def push(self, item, priority):
        heapq.heappush(self.data, (priority, item))
    
    def pop(self):
        return heapq.heappop(self.data)[1]

