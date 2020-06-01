from queue import PriorityQueue

def outer():
    q = PriorityQueue()
    q.put(20)
    q.put(40)
    q.put(1)

    def qput(num):
        q.put(num)

    def qget():
        return q.get()

    def inner():
        print(qget())
        qput(2)
        print(qget())

    inner()

outer()