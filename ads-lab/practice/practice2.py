# circular queue

class Q:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.front = 0
        self.rear = 0
        self.size = 0
        self.arr = [None]*capacity

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == self.capacity
    
    def push(self, val):
        if self.is_full():
            print("Que is full, cannot enque!")
            return
        self.arr[self.rear] = val
        self.rear = (self.rear+1)%self.capacity
        print(f"Enqued into que {val}")
        self.size+=1

    def pop(self):
        if self.is_empty():
            print("Que is empty, cannot deque!")
            return
        val = self.arr[self.front]
        print(f"Dequed from que: {val}")
        self.arr[self.front] = None
        self.front = (self.front+1)%self.capacity
        self.size-=1

    def get_size(self):
        print(f"Size of que: {self.size}")

    def display(self):
        if self.is_empty():
            print("Que is empty, cannot display!")
            return
        i = self.front
        print("Displaying queue - front -> rear")
        for _ in range(self.size):
            print(self.arr[i])
            i = (i+1)%self.capacity

def main():
    que = Q()
    que.display()
    que.pop()
    que.push(3)
    que.push(8)
    que.push(10)
    que.push(13)
    que.pop()
    que.display()
    que.pop()
    que.pop()
    que.get_size()
    que.pop()
    que.display()
    que.pop()
    que.get_size()

if __name__=="__main__":
    main()
        



