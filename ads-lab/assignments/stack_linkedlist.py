class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Linkedlist:

    def __init__(self):
        self.top = None
        self.size = 0

    def push(self, item):
        new_node = Node(item)
        new_node.next = self.top
        self.top = new_node
        self.size+=1
        print(f"Pushed item: {item} ")

    def pop(self):
        if self.is_empty():
            print("Empty Stack. Cannot pop. ")
            return None
        popped = self.top.data
        self.top = self.top.next
        self.size-=1
        return popped

    def peek(self):
        if self.is_empty():
            print("Empty Stack. Cannot peek. ")
            return None
        popped = self.top.data
        return popped

    def display(self):
        if self.is_empty():
            print("Empty Stack. Cannot display. ")
            return
        curr = self.top
        while curr:
            print(curr.data)
            print()
            curr = curr.next 


    def is_empty(self):
        return self.top is None

def main():
    stack = Linkedlist()
    while True:
        print("\n--- Stack (Linked List) Menu ---")
        print("1. Push")
        print("2. Pop")
        print("3. Peek")
        print("4. Display")
        print("5. Size")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ").strip()
        if choice == "1":
            val = input("Enter value to push: ")
            stack.push(val)
        elif choice == "2":
            val = stack.pop()
            if val is not None:
                print(f"Popped value: {val}")
        elif choice == "3":
            val = stack.peek()
            if val is not None:
                print(f"Top element: {val}")
        elif choice == "4":
            stack.display()
        elif choice == "5":
            print(f"Current size: {stack.size}")
        elif choice == "6":
            print("Exiting program.")
            break
        else:
            print("Invalid choice! Please select 1-6.")


if __name__ == "__main__":
    main()