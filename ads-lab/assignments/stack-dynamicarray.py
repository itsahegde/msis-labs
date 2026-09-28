class DynamicArrayStack:
    def __init__(self):
        self._capacity = 1
        self._size = 0
        self._arr = [None]*self._capacity

    def _resize(self, new_capacity):
        new_array = [None]*new_capacity
        for i in range(self._size):
            new_array[i] = self._arr[i]
        self._arr = new_array
        self._capacity = new_capacity

    def is_empty(self):
        if self._size==0:
            return True

    def push(self, item):
        if self._capacity==self._size:
            self._resize(2*self._capacity)
        self._arr[self._size] = item
        self._size+=1
        print(f"Pushed element into stack: {item}")

    def pop(self):
        if self.is_empty():
            print("Stack is empty. Stack underflow")
            return None
        popped = self._arr[self._size-1]
        self._arr[self._size-1]=None
        self._size-=1
        if 0 < self._size <= self._capacity // 4:
            self._resize(max(1, self._capacity // 2))
        return popped

    def peek(self):
        if self.is_empty():
            print("Stack is empty. Stack underflow")
            return None
        peeked = self._arr[self._size-1]
        return peeked

    def display(self):
        if self.is_empty():
            print("Stack empty, no elements to print.")
        for item in self._arr:
            print(item)

    def get_size(self):
        print(self._size)

    def get_capacity(self):
        print(self._capacity)
    
def main():
    stack = DynamicArrayStack()
    while True:
        print("\n--- Stack (Dynamic Array) Menu ---")
        print("1. Push")
        print("2. Pop")
        print("3. Peek")
        print("4. Display")
        print("5. Size & Capacity")
        print("6. Exit")

        choice = input("Enter your choice: ")
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
            stack.get_capacity()
            stack.get_size()
        elif choice == "6":
            print("Exiting program.")
            break
        else:
            print("Invalid choice! Please select 1-6.")

if __name__=="__main__":
    main()
