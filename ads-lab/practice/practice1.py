# que using singly linked list

class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

class Que:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def push(self, val):
        node = Node(val)
        if self.rear is None:
            self.rear = node
            self.front = node
        else:
            self.rear.next = node
            self.rear = node
        self.size+=1

    def pop(self):
        if self.front is None:
            print("Empty queue, cannot dequeue")
            return
        val = self.front.val
        print(f"Value of dequeued node: {val}")
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.size-=1

    def get_size(self):
        print(f"Size={self.size}")

    def peek(self):
        if self.front is None:
            print("Empty queue, cannot peek")
            return
        val = self.front.val
        print(f"Value of peeked node: {val}")

    def display(self):
        if self.front is None:
            print("Que is empty")
            return
        curr = self.front
        while curr!=None:
            print(f"{curr.val}-> ")
            curr = curr.next

def main():
    que = Que()
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
