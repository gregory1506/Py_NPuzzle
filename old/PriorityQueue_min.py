from queue import PriorityQueue

class Node:
    def __init__(self, number=None):
        self.number = number

    def __eq__(self,other):
        return self.number == other.number

    def __lt__(self,other):
        return self.number < other.number

    def __repr__(self):
        return str(self.number)

    def __hash__(self):
        return self.number.__hash__()

p = PriorityQueue()
p.put(Node(24))
p.put(Node(54))
p.put(Node(54))
p.put(Node(1))
p.put(Node(1))
print(p.get())
print(p.get())
a = set()
a.add(Node(24))