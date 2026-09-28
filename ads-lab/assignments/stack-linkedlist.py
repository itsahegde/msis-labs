class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class StackLL:
    def __init__(self):
        self.top = None
        self.size = 0
    def push(self, val):
        node = Node(val)
        node.next = self.top
        self.top = node
        self.size+=1
        print(f"Pushed new node: {node.data}")
    def pop(self):
        if self.isEmpty():
            print("Empty Stack")
            return
        val = self.top.data
        self.top = self.top.next
        self.size-=1
        return val
    def isEmpty(self):
        return self.top is None
    def display(self):
        curr = self.top
        while curr:
            print(f"{curr.data}\t")
            curr = curr.next

def main():
    stack = StackLL()
    while True:
        print("1 - Push")
        print("2 - Pop")
        print("3 - Display")
        print("4 - Exit")

        inp = input("Enter a choice: ")
        if inp == "1":
            item = input("Enter a number to push: ")
            stack.push(item)
        elif inp == "2":
            print(f"Popped element: {stack.pop()}")
        elif inp == "3":
            stack.display()
        elif inp == "4":
            break

if __name__ == "__main__":
    main()
        
        
